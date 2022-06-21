import os


class Configuration:

    def __init__(self):
        self.uniswap = Uniswap()
        self.trades = Trades()
        self.wallet = Wallet()
        self.withdrawals = Withdrawals()


class Wallet:

    def __init__(self):
        self.address = os.environ.get('WALLET_ADDRESS')
        self.private_key = os.environ.get('WALLET_PRIVATE_KEY')


class Withdrawals:

    def __init__(self):
        self.wallet_address = os.environ.get('WITHDRAWAL_WALLET_ADDRESS')


class Trades:

    def __init__(self):
        self.currency_symbol = os.environ.get('TRADES_CURRENCY_SYMBOL')
        self.currency_contract = os.environ.get('TRADES_CURRENCY_CONTRACT')
        self.target_currency_symbol = os.environ.get('TRADES_TARGET_CURRENCY_SYMBOL')
        self.target_currency_contract = os.environ.get('TRADES_TARGET_CURRENCY_CONTRACT')


class Uniswap:

    def __init__(self):
        self.version = int(os.environ.get('UNISWAP_VERSION'))
        self.network_provider = os.environ.get('NETWORK_PROVIDER')
