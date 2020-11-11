class DepotService:

    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get_all_depots(self):
        """
        5.1.2. Fetch information for all depots.

        :return: Response object
        """
        url = '{0}/brokerage/clients/user/v3/depots'.format(self.api_url)
        response = self.session.get(url).json()
        return response

    def get_depot_positions(self, depot_id, with_depot=True, with_positions=True, with_instrument=False,
                            instrument_id=None):
        """
        5.1.2. Fetch information for a specific depot.

        :param depot_id: Depot-ID
        :param with_depot: Include depot information in response. Defaults to True.
        :param with_positions: Include positions in response. Defaults to True.
        :param with_instrument: Include instrument information for positions, ignored if with_positions is False.
            Defaults to False.
        :param instrument_id: Optional Instrument ID.
        :return: Response object
        """
        url = '{0}/brokerage/v3/depots/{1}/positions'.format(self.api_url, depot_id)
        params = {}
        if not with_depot and not with_positions:
            params['without_attr'] = 'depot,positions'
        elif with_depot and not with_positions:
            params['without_attr'] = 'positions'
        elif not with_depot and with_positions:
            params['without_attr'] = 'depot'

        if with_instrument and with_positions:
            params['with_attr'] = 'instrument'

        if instrument_id:
            params['instrumentId'] = instrument_id

        response = self.session.get(url, params=params).json()
        return response

    def get_position(self, depot_id, position_id, with_instrument=False):
        """
        5.1.3. Fetch a specific position.

        :param depot_id: Depot-ID
        :param position_id: Position-ID
        :param with_instrument: Include instrument information. Defaults to False.
        :return: Response object
        """
        url = '{0}/brokerage/v3/depots/{1}/positions/{2}'.format(self.api_url, depot_id, position_id)
        params = {'with-attr': 'instrument'} if with_instrument else None
        response = self.session.get(url, params=params).json()
        return response

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
        kwargs_mapping = {
            "wkn": "WKN",
            "isin": "ISIN",
            "instrument_id": "instrumentId",
            "max_booking_date": "max-bookingDate",
            "transaction_direction": "transactionDirection",
            "transaction_type": "transactionType",
            "booking_status": "bookingStatus",
            "min_transaction_value": "min-transactionValue",
            "max_transaction_value": "max-transactionValue"
        }

        url = '{0}/brokerage/v3/depots/{1}/transactions'.format(self.api_url, depot_id)
        params = {'without-attr': 'instrument'} if not with_instrument else {}

        for arg, val in kwargs.items():
            api_arg = kwargs_mapping.get(arg)
            if api_arg is None:
                raise ValueError('Keyword argument {} is invalid'.format(arg))
            else:
                params[api_arg] = val

        response = self.session.get(url, params=params).json()
        return response
