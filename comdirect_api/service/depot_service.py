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

    def get_depot_positions(self, depot_id, with_depot=True, with_positions=True, with_instrument=False, instrument_id=None):
        """
        5.1.2. Fetch information for a specific depot.

        :param depot_id: Depot-ID
        :param with_depot: Include depot information in response. Defaults to True.
        :param with_positions: Include positions in reponse. Defaults to True.
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

    def get_depot_transactions(self):
        """
        5.1.4. NOT YET IMPLEMENTED
        """
        raise NotImplementedError()
