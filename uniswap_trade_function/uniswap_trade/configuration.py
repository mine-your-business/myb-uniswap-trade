import os


class Configuration:

    def __init__(self):
        self.uniswap = Uniswap()
        self.trades = Trades()
        self.wallet = Wallet()
        self.withdrawals = Withdrawals()
        self.sheets = Sheets() if os.environ.get('RECORD_TRADES') else None


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
        self.network = os.environ.get('NETWORK')
        self.exchange = os.environ.get('EXCHANGE')
        self.network_provider = os.environ.get('NETWORK_PROVIDER')
        self.transactions_explorer_prefix = os.environ.get('NETWORK_TRANSACTIONS_EXPLORER_PREFIX')


class SheetsCredentials:

    def __init__(self):
        self.type = os.environ.get('SHEETS_CREDENTIALS_TYPE')
        self.project_id = os.environ.get('SHEETS_CREDENTIALS_PROJECT_ID')
        self.private_key_id = os.environ.get('SHEETS_CREDENTIALS_PRIVATE_KEY_ID')
        self.private_key = os.environ.get('SHEETS_CREDENTIALS_PRIVATE_KEY').replace(r'\n', '\n')
        self.client_email = os.environ.get('SHEETS_CREDENTIALS_CLIENT_EMAIL')
        self.client_id = os.environ.get('SHEETS_CREDENTIALS_CLIENT_ID')
        self.token_uri = os.environ.get('SHEETS_CREDENTILS_TOKEN_URI')
        self.auth_provider_x509_cert_url = os.environ.get('SHEETS_CREDENTIALS_AUTH_PROVIDER_X509_CERT_URL')
        self.client_x509_cert_url = os.environ.get('SHEETS_CREDENTIALS_CLIENT_X509_CERT_URL')


class SheetsTradesSpreadsheet:

    def __init__(self):
        self.id = os.environ.get('SHEETS_TRADES_SPREADSHEET_ID')
        self.sheet_id = os.environ.get('SHEETS_TRADES_SPREADSHEET_SHEET_ID')
        self.data_start_column = os.environ.get('SHEETS_TRADES_SPREADSHEET_DATA_START_COLUMN')
        self.data_exclusive_end_column = os.environ.get('SHEETS_TRADES_SPREADSHEET_DATA_EXCLUSIVE_END_COLUMN')


class Sheets:

    def __init__(self):
        self.credentials = SheetsCredentials()
        self.trades_spreadsheet = SheetsTradesSpreadsheet()
