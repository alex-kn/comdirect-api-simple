import requests

from api.auth.auth_service import AuthService
from api.service.account_service import AccountService
from api.service.depot_service import DepotService
from api.service.document_service import DocumentService
from api.service.report_service import ReportService


class ComdirectClient:

    def __init__(self):
        self.api_url = 'https://api.comdirect.de/api'
        self.oauth_url = 'https://api.comdirect.de'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

        self.auth_service = AuthService(self.session, self.api_url, self.oauth_url)
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

    def get_account_transactions(self, account_uuid, with_account=False, transaction_state='BOTH'):
        """
        4.1.3. Fetch transactions for a specific account.

        :param account_uuid:  Account-ID
        :param with_account: Include account information in the response. Defaults to False
        :param transaction_state: 'BOOKED' or 'NOTBOOKED'. Defaults to 'BOTH'
        :return: Response object
        """
        return self.account_service.get_account_transactions(account_uuid, with_account, transaction_state)

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
        :param with_positions: Include positions in reponse. Defaults to True.
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

    def get_depot_transactions(self):
        """
        5.1.4. NOT YET IMPLEMENTED
        """
        return self.depot_service.get_depot_transactions()

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
