import os

from comdirect_api.comdirect_client import ComdirectClient


def test_comdirect_client_fresh_init():
    client_id = "dummy_id"
    client_secret = "dummy_secret"
    api_url = "https://api.comdirect.de/api"
    oauth_url = "https://api.comdirect.de"

    client = ComdirectClient(client_id, client_secret)

    headers = client.session.headers
    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert client.api_url == api_url
    assert client.oauth_url == oauth_url

    assert client.auth_service.api_url == api_url
    assert client.auth_service.oauth_url == oauth_url
    assert client.auth_service.client_id == client_id
    assert client.auth_service.client_secret == client_secret


def test_comdirect_client_import_session(tmp_path):
    client_id = "dummy_id"
    client_secret = "dummy_secret"
    client = ComdirectClient(client_id, client_secret)

    client.session_export(os.path.join(tmp_path, "session.pkl"))

    new_client = ComdirectClient(client_id,
                                 client_secret,
                                 import_session=os.path.join(
                                     tmp_path, "session.pkl"))

    assert new_client.auth_service.client_id == client_id
    assert new_client.auth_service.client_secret == client_secret
