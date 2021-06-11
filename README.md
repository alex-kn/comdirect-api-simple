# Comdirect API

This is an unofficial python wrapper for the comdirect API for private consumers (April 2020).

This package currently only supports read operations, which include:

* Read balances and transactions
* Read depot information
* Read and download Documents
* Read and update orders
* Export and import the session

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

The the client is now ready for use, for example:

```python
balances = client.get_all_balances()
print(balances['values'])
```

It is also possible to send a GET request to a self defined endpoint, for example:

```python
client.get('reports/participants/user/v1/allbalances', productType='ACCOUNT')
```

List all the complete order-book and filter for OPEN orders:

```python
data = client.get_all_orders(depotId, order_status='OPEN')
print(data)
```

You can change an OPEN order as follows:

```python
orderId='XXYYYAA...'
order = client.get_order(orderId)
order['triggerLimit']['value'] = '16.6'
[challange_id, challange]=client.set_order_change_validation(orderId,order)
orderChanged=client.set_order_change(orderId,data,challange_id)
```

To export the session you can use

```python
client.activate_session()
...
client.session_export()
```

To import it in another instance call:

```python
client = ComdirectClient('client_id', 'client_secret','session.pkl')
```

More information about the official API can be found at https://developer.comdirect.de
