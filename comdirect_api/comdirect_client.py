import requests

from comdirect_api.auth.auth_service import AuthService
from comdirect_api.service.account_service import AccountService
from comdirect_api.service.depot_service import DepotService
from comdirect_api.service.document_service import DocumentService
from comdirect_api.service.report_service import ReportService


class ComdirectClient:

    def __init__(self, client_id, client_secret):
        self.api_url = 'https://api.comdirect.de/api'
        self.oauth_url = 'https://api.comdirect.de'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

        self.auth_service = AuthService(client_id, client_secret, self.session, self.api_url, self.oauth_url)
        self.account_service = AccountService(self.session, self.api_url)
        self.depot_service = DepotService(self.session, self.api_url)
        self.document_service = DocumentService(self.session, self.api_url)
        self.report_service = ReportService(self.session, self.api_url)

    def fetch_tan(self, zugangsnummer, pin, tan_type=None):
        return self.auth_service.fetch_tan(zugangsnummer, pin, tan_type)

    def activate_session(self, tan=None):
        self.auth_service.activate_session(tan)

    def refresh_token(self):
        self.auth_service.refresh_token()

    def revoke_token(self):
        self.auth_service.revoke()

    def get_all_balances(self, without_account=False):
        """
        4.1.1. Fetch balances from all accounts.

        :param without_account: Don't include account object in response
        :return: Response object
        """
        return self.account_service.get_all_balances(without_account)

    def get_balance(self, account_uuid):
        """
        4.1.2. Fetch balance for a specific account.

        :param account_uuid: Account-ID
        :return: Response object
        """
        return self.account_service.get_balance(account_uuid)

    def get_account_transactions(self, account_uuid, with_account=False, transaction_state='BOTH', paging_count=20,
                                 paging_first=0, min_booking_date=None, max_booking_date=None):
        """
        4.1.3. Fetch transactions for a specific account. Not setting a min_booking_date currently limits the result to
        the last 180 days.

        :param account_uuid:  Account-ID
        :param with_account: Include account information in the response. Defaults to False
        :param transaction_state: 'BOOKED' or 'NOTBOOKED'. Defaults to 'BOTH'
        :param paging_count: Number of transactions
        :param paging_first: Index of first returned transaction. Only possible for booked transactions
        (transaction_state='BOOKED').
        :param max_booking_date: max booking date in format YYYY-MM-DD
        :param min_booking_date: min booking date in format YYYY-MM-DD
        :return: Response object
        """
        return self.account_service.get_account_transactions(account_uuid, with_account, transaction_state,
                                                             paging_count, paging_first, min_booking_date,
                                                             max_booking_date)

    def get_all_depots(self):
        """
        5.1.2. Fetch information for all depots.

        :return: Response object
        """
        return self.depot_service.get_all_depots()

    def get_depot_positions(self, depot_id, with_depot=True, with_positions=True, with_instrument=False):
        """
        5.1.2. Fetch information for a specific depot.

        :param depot_id: Depot-ID
        :param with_depot: Include depot information in response. Defaults to True.
        :param with_positions: Include positions in response. Defaults to True.
        :param with_instrument: Include instrument information for positions, ignored if with_positions is False.
            Defaults to False.
        :return: Response object
        """
        return self.depot_service.get_depot_positions(depot_id, with_depot, with_positions, with_instrument)

    def get_position(self, depot_id, position_id, with_instrument=False):
        """
        5.1.3. Fetch a specific position.

        :param depot_id: Depot-ID
        :param position_id: Position-ID
        :param with_instrument: Include instrument information. Defaults to False.
        :return: Response object
        """
        return self.depot_service.get_position(depot_id, position_id, with_instrument)

    def get_depot_transactions(self, depot_id, with_instrument=False, **kwargs):
        """
        5.1.4. Fetch depot transactions, filter parameters can be applied via kwargs

        :param depot_id: Depot-ID
        :param with_instrument: Include instrument information. Defaults to False.
        :key wkn: filter by WKN
        :key isin: filter by ISIN
        :key instrument_id: filter by instrumentId
        :key max_booking_date: filter by booking date, Format "JJJJ-MM-TT"
        :key transaction_direction: filter by transactionDirection: {"IN", "OUT"}
        :key transaction_type: filter by transactionType: {"BUY", "SELL", "TRANSFER_IN", "TRANSFER_OUT"}
        :key booking_status: filter by  bookingStatus: {"BOOKED", "NOTBOOKED", "BOTH"}
        :key min_transaction_value: filter by min-transactionValue
        :key max_transaction_value: filter by max-transactionValue
        :return: Response object
        """
        return self.depot_service.get_depot_transactions(depot_id, with_instrument, **kwargs)

    def get_documents(self, first_index=0, count=1000):
        """
        9.1.1. Fetch all documents in the PostBox

        :param first_index: Index of the first document, starting with 0. Defaults to 0
        :param count: Number of documents to be fetched. Max 1000. Defaults to 1000.
        :return: Response object
        """
        return self.document_service.get_documents(first_index, count)

    def get_document(self, document_id):
        """
        9.1.2. Fetch a specific document. The document will be marked as read when fetched.

        :param document_id: Document-ID
        :return: Document and the content type of the document
        """
        return self.document_service.get_document(document_id)

    def get_report(self, product_type=None):
        """
        10.1.1. Fetch a report for all products

        :param product_type: Filter by one or more of ACCOUNT, CARD, DEPOT, LOAN, SAVINGS
            (list or comma-separated string)
            Defaults to None (all product types without filter)
        :return: Response object
        """
        return self.report_service.get_report(product_type)

    def get(self, endpoint, base_url='https://api.comdirect.de/api', **kwargs):
        """
        Sends a generic GET-request to a given endpoint with given parameters

        :param endpoint: endpoint without leading slash, e.g. 'banking/clients/clientId/v2/accounts/balances'
        :param base_url: base url. Defaults to 'https://api.comdirect.de/api'
        :param kwargs: query parameters
        :return: Response object
        """
        url = '{0}/{1}'.format(base_url, endpoint)
        return self.session.get(url, params=kwargs).json()
