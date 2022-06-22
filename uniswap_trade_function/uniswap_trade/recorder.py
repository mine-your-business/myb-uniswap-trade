import datetime

from .configuration import Sheets
from sheets import SheetsApi


class Recorder:

    def __init__(self, config: Sheets):
        self.config = config

    def record(
        self,
        exchange: str,
        network: str,
        input_symbol: str,
        output_symbol: str,
        price: float,
        price_impact: float,
        input_amount: float,
        output_amount,
        transaction_id: str,
        transactions_explorer_prefix: str
    ):
        sheets_api = SheetsApi(
            vars(self.config.credentials)
        )
        trades_spreadsheet = self.config.trades_spreadsheet

        existing_trades = sheets_api.read_from_sheet(
            trades_spreadsheet.id,
            {
                'grid_range': {
                    'sheet_id': trades_spreadsheet.sheet_id,
                    'start_row_index': 0,
                    'end_row_index': 999999,
                    'start_column_index': trades_spreadsheet.data_start_column,
                    'end_column_index': trades_spreadsheet.data_exclusive_end_column
                }
            }
        )
        values = existing_trades[0]['valueRange']['values']
        next_row_to_write = len(values)
        last_recorded_trade = values[-1]
        last_recorded_timestamp = last_recorded_trade[0]
        print(f'Last trade entry found on row {next_row_to_write}: {last_recorded_trade}')

        # Record the trade, adding the following data
        # Timestamp, Exchange, Network, Input Token, Output Token
        # Swap Price, LP Price Impact, Input Amount, Output Amount
        # Transaction ID, Tx Link
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        transaction_link = f'{transactions_explorer_prefix}{transaction_id}'
        sheets_api.write_to_sheet(
            trades_spreadsheet.id,
            {
                'data_filter': {
                    'grid_range': {
                        'sheet_id': trades_spreadsheet.sheet_id,
                        'start_row_index': next_row_to_write,
                        'end_row_index': next_row_to_write + 1,
                        'start_column_index': trades_spreadsheet.data_start_column,
                        'end_column_index': trades_spreadsheet.data_exclusive_end_column
                    }
                },
                'major_dimension': 'ROWS',
                'values': [
                    [timestamp, exchange, network, input_symbol, output_symbol, price,
                        price_impact, input_amount, output_amount, transaction_id, transaction_link]
                ]
            }
        )
        print('Trade recording completed')
