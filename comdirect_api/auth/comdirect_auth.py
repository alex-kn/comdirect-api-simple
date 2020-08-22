from requests.auth import AuthBase
import uuid
import time


class ComdirectAuth(AuthBase):
    def __init__(self, access_token, refresh_token):
        self.session_id = str(uuid.uuid4())
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __call__(self, request):
        request.headers.update(
            {
                'Authorization': 'Bearer {0}'.format(self.access_token),
                'x-http-request-info': str(
                    {'clientRequestId': {'sessionId': self.session_id, 'requestId': generate_request_id()}}),
            }
        )
        return request

    def session_tan_created(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


def generate_request_id():
    return str(round(time.time() * 1000))[-9:]
