import requests
import json

class OrderService:

    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

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
        kwargs_mapping = {
            "order_status": "orderStatus",
            "venue_id": "venueId",
            "side": "side",
            "order_type": "orderType"
        }

        url = '{0}/brokerage/depots/{1}/v3/orders'.format(self.api_url, depot_id)
        params = {}

        if with_instrument:
            params['with-attr'] = 'instrument'
        if not with_executions:
            params['without-attr'] = 'executions'

        for arg, val in kwargs.items():
            api_arg = kwargs_mapping.get(arg)
            if api_arg is None:
                raise ValueError('Keyword argument {} is invalid'.format(arg))
            else:
                params[api_arg] = val

        response = self.session.get(url, params=params).json()
        return response

    def get_order(self, order_id):
        """
        7.1.3 Abruf Order (Einzelorder)

        :param depot_id: Depot-ID
        :return: Response object
        """
        url = '{0}/brokerage/v3/orders/{1}'.format(self.api_url, order_id)
        params = {}
        
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise OrderException(response.headers['x-http-response-info'])

    def set_change_validation(self, order_id, changed_order):

        url = '{0}/brokerage/v3/orders/{1}/validation'.format(self.api_url, order_id)
        response = self.session.post(url, json=changed_order)
        if response.status_code == 201:
            response_json = json.loads(response.headers['x-once-authentication-info'])
            typ = response_json['typ']
            print("TAN-TYP: {}".format(typ))
            if typ == 'P_TAN' or typ == 'M_TAN':
                return response_json['id'], response_json['challenge']
            else:
                return response_json['id'], None
        else:
            raise OrderException(response.headers['x-http-response-info'])

    def set_change(self, order_id, changed_order, challenge_id, tan=None):

        url = '{0}/brokerage/v3/orders/{1}'.format(self.api_url, order_id)
        headers = {
            'x-once-authentication-info': json.dumps({
                "id": challenge_id
            })
        }
        if tan is not None:
            headers['x-once-authentication'] = str(tan)

        response = self.session.patch(url, headers=headers, json=changed_order)
        if response.status_code == 200:
            return response.json()
        else:
            raise OrderException(response.headers['x-http-response-info'])


class OrderException(Exception):
    def __init__(self, response_info):
        self.response_info = response_info
        super().__init__(self.response_info)