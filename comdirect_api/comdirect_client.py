import requests
import pickle

from comdirect_api.auth.auth_service import AuthService
from comdirect_api.service.account_service import AccountService
from comdirect_api.service.depot_service import DepotService
from comdirect_api.service.document_service import DocumentService
from comdirect_api.service.report_service import ReportService
from comdirect_api.service.order_service import OrderService
from comdirect_api.service.instrument_service import InstrumentService


class ComdirectClient(AccountService, DepotService):

    def __init__(self, client_id, client_secret, import_session=False):
        self.api_url = 'https://api.comdirect.de/api'
        self.oauth_url = 'https://api.comdirect.de'
        
        if not import_session:
            self.session = requests.Session()
            self.session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            })
            self.auth_service = AuthService(client_id, client_secret, self.session, self.api_url, self.oauth_url)
        else:
            if import_session == True:
                import_session = 'session.pkl'
            with open(import_session, 'rb') as input:
                self.session = pickle.load(input)
                self.auth_service = pickle.load(input)

        self.document_service = DocumentService(self.session, self.api_url)
        self.report_service = ReportService(self.session, self.api_url)
        self.order_service = OrderService(self.session, self.api_url)
        self.instrument_service = InstrumentService(self.session, self.api_url)

    def session_export(self, filename = 'session.pkl'):
        with open(filename, 'wb') as output:
            pickle.dump(self.session, output, pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.auth_service, output, pickle.HIGHEST_PROTOCOL)

    def fetch_tan(self, zugangsnummer, pin, tan_type=None):
        return self.auth_service.fetch_tan(zugangsnummer, pin, tan_type)

    def activate_session(self, tan=None):
        self.auth_service.activate_session(tan)

    def refresh_token(self):
        self.auth_service.refresh_token()

    def revoke_token(self):
        self.auth_service.revoke()

    def get_instrument(self, instrument_id, order_dimensions=False, fund_distribution=False, derivative_data=False, static_data = True):
        """
        6.1.1 Abruf Instrument
        order_dimensions: es wird das OrderDimension-Objekt befüllt
        fund_distribution: es   wird das FundDistribution-Objekt befüllt,   wenn  es  sich  bei   dem Wertpapier um einen Fonds handelt
        derivative_data: es wird das DerivativeData-Objekt befüllt, wenn es sich bei dem Wertpapier um ein Derivat handelt
        static_data: gibt das StaticData -Objekt nicht zurück
        :return: Response object
        """
        return self.instrument_service.get_instrument(instrument_id, order_dimensions=False, fund_distribution=False, derivative_data=False, static_data = True)
        
    def get_order_dimensions(self, **kwargs):
        """
        7.1.1 Abruf Order Dimensionen
        :key instrument_id: fiters instrumentId
        :key wkn: fiters WKN
        :key isin: fiters ISIN
        :key mneomic: fiters mneomic
        :key venue_id: fiters venueId: Mit Hilfe der venueId, welche als UUID eingegeben werden muss, kann auf einen Handelsplatz gefiltert werden
        :key side: Entspricht der Geschäftsart. Filtermöglichkeiten sind BUY oder SELL
        :key order_type: fiters orderType: Enspricht dem Ordertypen (bspw. LIMIT, MARKET oder ONE_CANCELS_OTHER)
        :key type: filters type: Mittels EXCHANGE oder OFF kann unterschieden werden, ob nach einem Börsenplatz (EXCHANGE) oder einem LiveTrading Handelsplatz (OFF) gefiltert werden soll
        :return: Response object
        """
        return self.order_service.get_dimensions(**kwargs)

    def get_all_orders(self, depot_id, with_instrument=False, with_executions=True, **kwargs):
        """
        7.1.2 Abruf Orders (Orderbuch)

        :param depot_id: Depot-ID
        :param with_instrument: Include instrument information. Defaults to False.
        :param with_executions: Include execution information. Defaults to True.
        :key order_status: filter by orderStatus: {"OPEN ", "EXECUTED", "SETTLED"...}
        :key venue_id: filter by venueId
        :key side: filter by side: {"BUY", "SELL"}
        :key order_type: filter by orderType
        :return: Response object
        """
        return self.order_service.get_all_orders(depot_id, with_instrument, with_executions, **kwargs)

    def get_order(self, order_id):
        """
        7.1.3 Abruf Order (Einzelorder)

        :param depot_id: Depot-ID
        :return: Response object
        """
        return self.order_service.get_order(order_id)

    def set_order_change_validation(self, order_id, changed_order):
        """
        7.1.5 Anlage Validation Orderanlage

        :param order_id: Order-ID
        :param changed_order: Altered order from get_order
        :return: [challenge_id, challenge] (if challenge not neccessary: None)
        """
        return self.order_service.set_change_validation(order_id, changed_order)

    def set_order_change(self, order_id, changed_order, challenge_id, tan=None):
        """
        7.1.11Änderung der Orde

        :param order_id: Order-ID
        :param changed_order: same altered order as for set_change_validation
        :param challenge_id: first return value from set_change_validation
        :param tan: tan if neccessary
        :return: Response object
        """
        return self.order_service.set_change(order_id, changed_order, challenge_id, tan)


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
