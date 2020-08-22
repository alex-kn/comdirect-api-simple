# Comdirect API

This is an unofficial python wrapper for the comdirect API for private consumers (April 2020).

This package currently only supports read operations, which include:

* Read balances and transactions
* Read depot information
* Read and download Documents

## Install

Install the package using `pip`

```shell script
pip install comdirect-api-simple
```

## Usage

Initialize the client:

```python
from comdirect_api.comdirect_client import ComdirectClient

client_id = '<your_client_id>'
client_secret = '<your_client_secret>'
client = ComdirectClient(client_id, client_secret)
```


Login with your credentials like so:

```python
user = 'your_zugangsnummer'
password = 'your_pin'
client.fetch_tan(user, password)
```
After confirming the login on your photoTAN app you can activate your session.

```python
client.activate_session()
```
You can refresh your token with:

```python
client.refresh_token()
```

The API is now ready for use, for example:

```python
balances = client.get_all_balances()
print(balances['values'])
```

More information about the API can be found at https://developer.comdirect.de
