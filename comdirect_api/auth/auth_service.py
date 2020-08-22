import json

from comdirect_api.auth.comdirect_auth import ComdirectAuth


class AuthService:

    def __init__(self, client_id, client_secret, session, api_url, oauth_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url
        self.oauth_url = oauth_url
        self.session = session
        self.auth = None
        self.session_identifier = None
        self.challenge_id = None

    def fetch_tan(self, zugangsnummer, pin, tan_type=None):
        access_token, refresh_token = self.__oauth_resource_owner_password_credentials_flow(zugangsnummer, pin)
        self.auth = ComdirectAuth(access_token, refresh_token)
        self.session.auth = self.auth

        self.session_identifier = self.__get_session_status()
        self.challenge_id, challenge = self.__post_session_tan(self.session_identifier, tan_type)
        return challenge

    def activate_session(self, tan=None):
        self.__activate_session_tan(self.session_identifier, self.challenge_id, tan)
        access_token, refresh_token = self.__oauth_cd_secondary_flow()
        self.auth.session_tan_created(access_token, refresh_token)

    def refresh_token(self):
        url = '{0}/oauth/token'.format(self.oauth_url)
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": 'refresh_token',
            "refresh_token": self.auth.refresh_token,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response_json = response.json()
            self.auth.access_token = response_json['access_token']
            self.auth.refresh_token = response_json['refresh_token']
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])

    def revoke(self):
        url = "{0}/oauth/revoke".format(self.oauth_url)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = self.session.delete(url, headers=headers)
        if response.status_code == 204:
            print('Token revoked')
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])

    def __oauth_resource_owner_password_credentials_flow(self, zugangsnummer, pin):
        url = '{0}/oauth/token'.format(self.oauth_url)
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": 'password',
            "username": str(zugangsnummer),
            "password": str(pin),
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response_json = response.json()
            return response_json['access_token'], response_json['refresh_token']
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])

    def __get_session_status(self):
        url = '{0}/session/clients/user/v1/sessions'.format(self.api_url)

        response = self.session.get(url)
        if response.status_code == 200:
            response_json = response.json()[0]
            return response_json['identifier']
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])

    def __post_session_tan(self, session_identifier, tan_type=None):

        headers = None
        if tan_type is not None:
            headers = {'x-once-authentication-info': json.dumps({"typ": tan_type})}

        url = "{0}/session/clients/user/v1/sessions/{1}/validate".format(self.api_url, session_identifier)
        payload = '{\"identifier\" : \"' + session_identifier + '\",\"sessionTanActive\": true,\"activated2FA\": true}'
        response = self.session.post(url, data=payload, headers=headers)
        if response.status_code == 201:
            response_json = json.loads(response.headers['x-once-authentication-info'])
            typ = response_json['typ']
            print("TAN-TYP: {}".format(typ))
            if typ == 'P_TAN' or typ == 'M_TAN':
                return response_json['id'], response_json['challenge']
            else:
                return response_json['id'], None
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])

    def __activate_session_tan(self, session_identifier, challenge_id, tan=None):
        url = "{0}/session/clients/user/v1/sessions/{1}".format(self.api_url, session_identifier)
        payload = '{\"identifier\" : \"' + session_identifier + '\",\"sessionTanActive\": true,\"activated2FA\": true}'
        headers = {
            'x-once-authentication-info': json.dumps({
                "id": challenge_id
            })
        }
        if tan is not None:
            headers['x-once-authentication'] = str(tan)

        response = self.session.patch(url, headers=headers, data=payload)
        if response.status_code == 200:
            print('Session TAN activated')
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])

    def __oauth_cd_secondary_flow(self):
        url = "{0}/oauth/token".format(self.oauth_url)

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": 'cd_secondary',
            "token": self.auth.access_token,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = self.session.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response_json = response.json()
            return response_json['access_token'], response_json['refresh_token']
        else:
            raise AuthenticationException(response.headers['x-http-response-info'])


class AuthenticationException(Exception):
    def __init__(self, response_info):
        self.response_info = response_info
        super().__init__(self.response_info)
