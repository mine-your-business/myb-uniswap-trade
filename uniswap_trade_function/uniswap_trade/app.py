import os
import datetime

from .configuration import Configuration
from uniswap import Uniswap
from web3 import Web3
from web3.middleware import geth_poa_middleware
from .recorder import Recorder


def lambda_handler(event, context):
    """Lambda function reacting to EventBridge events

    Parameters
    ----------
    event: dict, required
        Event Bridge Scheduled Events Format

        Event doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html#schedule-event-type

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    """

    dry_run = os.environ.get('RUN_MODE') == 'test'
    print(f'Running in {"dry run" if dry_run else "production"} mode')

    config = Configuration()

    inp_symbol = config.trades.currency_symbol
    inp_currency_addr = config.trades.currency_contract
    out_symbol = config.trades.target_currency_symbol
    out_currency_addr = config.trades.target_currency_contract
    version = config.uniswap.version
    rpc = config.uniswap.network_provider

    polygon = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 60}))
    polygon.middleware_onion.inject(geth_poa_middleware, layer=0)

    uniswap = Uniswap(
        address=config.wallet.address,
        private_key=config.wallet.private_key,
        version=version,
        maximum_gas=50 * 1_000_000_000,
        provider=rpc,
        web3=polygon
    )

    def to_quantity(amount: int, token_addr: str):
        return amount * 10 ** uniswap.get_token(token_addr).decimals

    def from_quantity(amount: int, token_addr: str):
        return amount / 10 ** uniswap.get_token(token_addr).decimals

    # 0.05% fee pool
    fee_pool_pct = 0.05
    fee_pool_val = int(fee_pool_pct * 10000)

    price = uniswap.get_raw_price(
        inp_currency_addr,
        out_currency_addr,
        fee_pool_val
    )
    print(f"Current price of 1 {inp_symbol} to {out_symbol}: {price}")
    quantity = to_quantity(1, inp_currency_addr)
    impact = uniswap.estimate_price_impact(
        inp_currency_addr,
        out_currency_addr,
        quantity,
        fee_pool_val,
    )
    print(f"Price impact of swapping 1 {inp_symbol} to {out_symbol} @ V{version} ({fee_pool_pct}pct fee pool): {impact}")

    # Make sure price impact is minimal
    if impact >= 0.001:
        print("Price impact too high to make a swap.")
        return

    token_bal_raw = uniswap.get_token_balance(inp_currency_addr)
    token_bal = from_quantity(token_bal_raw, inp_currency_addr)
    trade_value = token_bal * price

    print(f'Current balance: {token_bal} {inp_symbol} worth {trade_value} {out_currency_addr}')

    expected_real_impact = uniswap.estimate_price_impact(
        inp_currency_addr,
        out_currency_addr,
        token_bal_raw,
        fee_pool_val,
    )

    print(
        f"Price impact of swapping {token_bal} {inp_symbol} to {out_symbol} @ V{version} ({fee_pool_pct}pct fee pool): {expected_real_impact}")

    if dry_run:
        print(f'This was a dry run; Would have made trade of {token_bal} {inp_symbol} for {trade_value} {out_symbol}')
        # To allow record functionality to be leveraged during a dry run, write a fake transaction ID
        transaction_id = "fakeTx"
    else:
        print(f'Submitting trade transaction of {token_bal} {inp_symbol} for {trade_value} {out_symbol}')
        result = uniswap.make_trade(
            inp_currency_addr,
            out_currency_addr,
            token_bal_raw,
            recipient=config.withdrawals.wallet_address,
            fee=fee_pool_val
        )
        transaction_id = result.hex()
        print(f'Trade issued: {transaction_id}')

    if config.sheets is None:
        print('Trade will not be recorded')
        return

    print('Trade will be recorded')
    recorder = Recorder(config.sheets)
    recorder.record(
        exchange=config.uniswap.exchange,
        network=config.uniswap.network,
        input_symbol=inp_symbol,
        output_symbol=out_symbol,
        price=price,
        price_impact=expected_real_impact,
        input_amount=token_bal,
        output_amount=trade_value,
        transaction_id=transaction_id,
        transactions_explorer_prefix=config.uniswap.transactions_explorer_prefix
    )

    # We got here successfully!
    return True
