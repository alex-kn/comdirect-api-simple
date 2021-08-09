from typing import Any, Union
import requests
import pickle

from comdirect_api.auth.auth_service import AuthService
from comdirect_api.service.account_service import AccountService
from comdirect_api.service.depot_service import DepotService
from comdirect_api.service.document_service import DocumentService
from comdirect_api.service.report_service import ReportService
from comdirect_api.service.order_service import OrderService
from comdirect_api.service.instrument_service import InstrumentService


class ComdirectClient(
    AccountService,
    DepotService,
    DocumentService,
    InstrumentService,
    OrderService,
    ReportService,
):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        import_session: Union[str, bool] = False,
    ):
        self.api_url = "https://api.comdirect.de/api"
        self.oauth_url = "https://api.comdirect.de"

        if not import_session:
            self.session = requests.Session()
            self.session.headers.update(
                {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                }
            )
            self.auth_service = AuthService(
                client_id, client_secret, self.session, self.api_url, self.oauth_url
            )
        else:
            if import_session is True:
                import_session = "session.pkl"
            with open(import_session, "rb") as input:
                self.session = pickle.load(input)
                self.auth_service = pickle.load(input)

    def session_export(self, filename: str = "session.pkl"):
        with open(filename, "wb") as output:
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

    def get(
        self, endpoint: str, base_url: str = "https://api.comdirect.de/api", **kwargs
    ) -> Any:
        """Sends a generic GET-request to a given endpoint with given parameters

        Args:
            endpoint (str): endpoint without leading slash, e.g. 'banking/clients/clientId/v2/accounts/balances'
            base_url (str, optional): Base URL. Defaults to 'https://api.comdirect.de/api'.

        Kwargs: Request parameters

        Returns:
            Any: Response object
        """
        url = "{0}/{1}".format(base_url, endpoint)
        return self.session.get(url, params=kwargs).json()
