from typing import Any
import requests


class InstrumentService:
    def __init__(self, session: requests.Session, api_url: str):
        self.session = session
        self.api_url = api_url

    def get_instrument(
        self,
        instrument_id: str,
        order_dimensions: bool = False,
        fund_distribution: bool = False,
        derivative_data: bool = False,
        static_data: bool = True,
    ) -> Any:
        """6.1.1. Request for an intrument's information

        Args:
            instrument_id (str): Instrument identification - can be either the WKN, the ISIN or the symbol.
            order_dimensions (bool, optional): Include the order dimension object. Defaults to False.
            fund_distribution (bool, optional): Include the fund distribution object if the instrument is a fund.
                Defaults to False.
            derivative_data (bool, optional): include the derivative data object if the instrument is a derivative.
                Defaults to False.
            static_data (bool, optional): Include the static data object. Defaults to True.

        Returns:
            Any: Reponse object
        """
        url = "{0}/brokerage/v1/instruments/{1}".format(self.api_url, instrument_id)
        params = {}

        if order_dimensions:
            params["with-attr"] = "orderDimensions"
        if fund_distribution:
            if "with-attr" in params.keys():
                params["with-attr"] = params["with-attr"] + ",fundDistribution“"
            else:
                params["with-attr"] = "fundDistribution“"
        if derivative_data:
            if "with-attr" in params.keys():
                params["with-attr"] = params["with-attr"] + ",derivativeData“"
            else:
                params["with-attr"] = "derivativeData“"
        if static_data is False:
            params["without-attr"] = "staticData"

        response = self.session.get(url, params=params).json()
        return response
