from typing import Any


class DepotService:
    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get_all_depots(self) -> Any:
        """5.1.1. Request for a list of the master data for the securities accounts of the registered user

        Returns:
            Any: Response object
        """

        url = "{0}/brokerage/clients/user/v3/depots".format(self.api_url)
        response = self.session.get(url).json()
        return response

    def get_depot_positions(
        self,
        depot_id: str,
        with_depot: bool = True,
        with_positions: bool = True,
        with_instrument: bool = False,
        instrument_id: bool = None,
    ) -> Any:
        """5.1.2. Request for securities positions.

        Request for securities positions, optionally including only the total balance with securities account
        information.

        Args:
            depot_id (str): Reference to securities account number
            with_depot (bool, optional): Include depot information in response. Defaults to True.
            with_positions (bool, optional): Include position information in response. Defaults to True.
            with_instrument (bool, optional): Include instrument information for positions.
                Ignored if with_positions is False. Defaults to False.
            instrument_id (bool, optional): [description]. Defaults to None.

        Returns:
            Any: Response object
        """
        url = "{0}/brokerage/v3/depots/{1}/positions".format(self.api_url, depot_id)
        params = {}
        if not with_depot and not with_positions:
            params["without_attr"] = "depot,positions"
        elif with_depot and not with_positions:
            params["without_attr"] = "positions"
        elif not with_depot and with_positions:
            params["without_attr"] = "depot"

        if with_instrument and with_positions:
            params["with_attr"] = "instrument"

        if instrument_id:
            params["instrumentId"] = instrument_id

        response = self.session.get(url, params=params).json()
        return response

    def get_position(
        self, depot_id: str, position_id: str, with_instrument: bool = False
    ) -> Any:
        """5.1.3. Request for retrieving a single position of specific depot.

        Args:
            depot_id (str): Reference to securities account number
            position_id (str): Position identification number in securities account
            with_instrument (bool, optional): Include instrument information for position. Defaults to False.

        Returns:
            Any: Response object
        """
        url = "{0}/brokerage/v3/depots/{1}/positions/{2}".format(
            self.api_url, depot_id, position_id
        )
        params = {"with-attr": "instrument"} if with_instrument else None
        response = self.session.get(url, params=params).json()
        return response

    def get_depot_transactions(
        self, depot_id: str, with_instrument: bool = False, **kwargs
    ):
        """5.1.4. Depot transactions.

        Args:
            depot_id (str): Reference to securities account number
            with_instrument (bool, optional): Include instrument information for positions. Defaults to False.

        Kwargs:
            wkn (str):
                filter by WKN
            isin (str):
                filter by ISIN
            instrument_id (str):
                filter by instrumentId
            max_booking_date (str):
                filter by booking date, Format YYYY-MM-TT
            transaction_direction (str):
                filter by transactionDirection: "IN", "OUT"
            transaction_type (str):
                filter by transactionType: "BUY", "SELL", "TRANSFER_IN", "TRANSFER_OUT"
            booking_status (str):
                filter by bookingStatus: "BOOKED", "NOTBOOKED", "BOTH"
            min_transaction_value (str):
                filter by min-transactionValue
            max_transaction_value (str):
                filter by max-transactionValue

        Raises:
            ValueError: If a keyword arg is invalid.

        Returns:
            Any: Response object
        """
        kwargs_mapping = {
            "wkn": "WKN",
            "isin": "ISIN",
            "instrument_id": "instrumentId",
            "max_booking_date": "max-bookingDate",
            "transaction_direction": "transactionDirection",
            "transaction_type": "transactionType",
            "booking_status": "bookingStatus",
            "min_transaction_value": "min-transactionValue",
            "max_transaction_value": "max-transactionValue",
        }

        url = "{0}/brokerage/v3/depots/{1}/transactions".format(self.api_url, depot_id)
        params = {"without-attr": "instrument"} if not with_instrument else {}

        for arg, val in kwargs.items():
            api_arg = kwargs_mapping.get(arg)
            if api_arg is None:
                raise ValueError("Keyword argument {} is invalid".format(arg))
            else:
                params[api_arg] = val

        response = self.session.get(url, params=params).json()
        return response
