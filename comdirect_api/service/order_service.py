from typing import Any
import json


class OrderService:
    def get_dimensions(self, **kwargs) -> Any:
        """7.1.1. Request for the trading venue and order options for a particular instrument.

        Kwargs: Filter Parameter
            instrument_id: Instrument id (UUID), unique identification of an instrument (security, derivative, etc.).
            wkn: WKN
            isin: ISIN
            mneomic: Mneomic
            venue_id: Venue id (UUID), unique identification of a venue.
            side: Possible transaction types. Available values:
                BUY, SELL
            order_type: The order type. Available values:
                MARKET, LIMIT, QUOTE, STOP_MARKET, STOP_LIMIT, TRAILING_STOP_MARKET,
                TRAILING_STOP_LIMIT, ONE_CANCELS_OTHER, NEXT_ORDER
            type: Type of venue. Available values : EXCHANGE, FUND, OFF

        Raises:
            ValueError: If a keyword argument is invalid.

        Returns:
            Any: Response object
        """
        kwargs_mapping = {
            "instrument_id": "instrumentId",
            "wkn": "WKN",
            "isin": "ISIN",
            "mneomic": "mneomic",
            "venue_id": "venueId",
            "side": "side",
            "order_type": "orderType",
            "type": "type",
        }

        url = "{0}/brokerage/v3/orders/dimensions".format(self.api_url)
        params = {}

        for arg, val in kwargs.items():
            api_arg = kwargs_mapping.get(arg)
            if api_arg is None:
                raise ValueError("Keyword argument {} is invalid".format(arg))
            else:
                params[api_arg] = val
        response = self.session.get(url, json=params).json()
        return response

    def get_all_orders(
        self,
        depot_id: str,
        with_instrument: bool = False,
        with_executions: bool = True,
        **kwargs
    ) -> Any:
        """7.1.2 Delivers a list fo all orders for the given depotId.

        Args:
            depot_id (str): Reference to securities account number (as UUID).
            with_instrument (bool, optional): Enables attribute: instrument. Defaults to False.
            with_executions (bool, optional): Enables attribute: executions. Defaults to True.

        Kwargs: Filter Parameter
            order_status: Status of the order. Available values:
                PENDING, OPEN, EXECUTED, SETTLED, CANCELLED_USER, EXPIRED, CANCELLED_SYSTEM, CANCELLED_TRADE, UNKNOWN
            venue_id: Venue id (UUID), unique identification of a venue.
            side: Possible transaction types. Available values:
                BUY, SELL
            order_type: The order type. Available values:
                MARKET, LIMIT, QUOTE, STOP_MARKET, STOP_LIMIT, TRAILING_STOP_MARKET, TRAILING_STOP_LIMIT,
                ONE_CANCELS_OTHER, NEXT_ORDER

        Raises:
            ValueError: If a keyword argument is invalid.

        Returns:
            Any: Response object
        """
        kwargs_mapping = {
            "order_status": "orderStatus",
            "venue_id": "venueId",
            "side": "side",
            "order_type": "orderType",
        }

        url = "{0}/brokerage/depots/{1}/v3/orders".format(self.api_url, depot_id)
        params = {}

        if with_instrument:
            params["with-attr"] = "instrument"
        if not with_executions:
            params["without-attr"] = "executions"

        for arg, val in kwargs.items():
            api_arg = kwargs_mapping.get(arg)
            if api_arg is None:
                raise ValueError("Keyword argument {} is invalid".format(arg))
            else:
                params[api_arg] = val

        response = self.session.get(url, params=params).json()
        return response

    def get_order(self, order_id: str) -> Any:
        """7.1.3. Delivers an order for the given orderId.

        Args:
            order_id (str): Unique orderId (UUID).

        Raises:
            OrderException: If an error occurred.

        Returns:
            Any: Reponse object
        """
        url = "{0}/brokerage/v3/orders/{1}".format(self.api_url, order_id)
        params = {}

        response = self.session.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise OrderException(response.headers["x-http-response-info"])

    def set_change_validation(self, order_id: str, changed_order: Any) -> Any:
        """7.1.5. Validation of an order modification or order cancellation and triggering of a TAN Challenge in a non-usage
        case of a Session-TAN

        Args:
            order_id (str): Reference to order identifier (as UUID).
            changed_order (Any): Altered order from get_order

        Raises:
            OrderException: If an error occurred

        Returns:
            Any: [challenge_id, challenge | None] (if challenge not neccessary: None)
        """
        url = "{0}/brokerage/v3/orders/{1}/validation".format(self.api_url, order_id)
        response = self.session.post(url, json=changed_order)
        if response.status_code == 201:
            response_json = json.loads(response.headers["x-once-authentication-info"])
            typ = response_json["typ"]
            print("TAN-TYP: {}".format(typ))
            if typ == "P_TAN" or typ == "M_TAN":
                return response_json["id"], response_json["challenge"]
            else:
                return response_json["id"], None
        else:
            raise OrderException(response.headers["x-http-response-info"])

    def set_change(
        self, order_id: str, changed_order: Any, challenge_id: str, tan: int = None
    ) -> Any:
        """7.1.11. Order modification.

        Args:
            order_id (str): Reference to order identifier (as UUID).
            changed_order (Any): same altered order as for set_change_validation
            challenge_id (str): challenge id from set_change_validation
            tan (int, optional): TAN if necessary. Defaults to None.

        Raises:
            OrderException: If an error occurred

        Returns:
            Any: Response object
        """
        url = "{0}/brokerage/v3/orders/{1}".format(self.api_url, order_id)
        headers = {"x-once-authentication-info": json.dumps({"id": challenge_id})}
        if tan is not None:
            headers["x-once-authentication"] = str(tan)

        response = self.session.patch(url, headers=headers, json=changed_order)
        if response.status_code == 200:
            return response.json()
        else:
            raise OrderException(response.headers["x-http-response-info"])


class OrderException(Exception):
    def __init__(self, response_info):
        self.response_info = response_info
        super().__init__(self.response_info)
