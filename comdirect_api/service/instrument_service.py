import requests
import json

class InstrumentService:

    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get_instrument(self, instrument_id, order_dimensions=False, fund_distribution=False, derivative_data=False, static_data = True):
        """
        6.1.1 Abruf Instrument
        order_dimensions: es wird das OrderDimension-Objekt befüllt
        fund_distribution: es   wird das FundDistribution-Objekt befüllt,   wenn  es  sich  bei   dem Wertpapier um einen Fonds handelt
        derivative_data: es wird das DerivativeData-Objekt befüllt, wenn es sich bei dem Wertpapier um ein Derivat handelt
        static_data: gibt das StaticData -Objekt nicht zurück
        :return: Response object
        """

        url = '{0}/brokerage/v1/instruments/{1}'.format(self.api_url,instrument_id)
        params = {}

        if order_dimensions:
            params['with-attr'] = 'orderDimensions'
        if fund_distribution:
            if 'with-attr' in params.keys():
                params['with-attr'] = params['with-attr'] + ',fundDistribution“'
            else:
                params['with-attr'] = 'fundDistribution“'
        if derivative_data:
            if 'with-attr' in params.keys():
                params['with-attr'] = params['with-attr'] + ',derivativeData“'
            else:
                params['with-attr'] = 'derivativeData“'
        if static_data == False:
            params['without-attr'] = 'staticData'

        response = self.session.get(url, params=params).json()
        return response

class InstrumentException(Exception):
    def __init__(self, response_info):
        self.response_info = response_info
        super().__init__(self.response_info)