class AccountService:

    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get_all_balances(self, without_account=False):
        """
        4.1.1. Fetch balances from all accounts.

        :param without_account: Don't include account object in response
        :return: Response object
        """
        url = '{0}/banking/clients/user/v2/accounts/balances'.format(self.api_url)
        params = {'without-attr': 'account'} if without_account else None
        response = self.session.get(url, params=params).json()
        return response

    def get_balance(self, account_uuid):
        """
        4.1.2. Fetch balance for a specific account.

        :param account_uuid: Account-ID
        :return: Response object
        """
        url = '{0}/banking/v2/accounts/{1}/balances'.format(self.api_url, account_uuid)
        response = self.session.get(url).json()
        return response

    def get_account_transactions(self, account_uuid, with_account=False, transaction_state='BOTH', paging_count=20,
                                 paging_first=0, min_booking_date=None, max_booking_date=None):
        """
        4.1.3. Fetch transactions for a specific account. Not setting a min_booking_date currently limits the result to
        the last 180 days.

        :param account_uuid:  Account-ID
        :param with_account: Include account information in the response. Defaults to False
        :param transaction_state: 'BOOKED' or 'NOTBOOKED'. Defaults to 'BOTH'
        :param paging_count: Number of transactions
        :param paging_first: Index of first returned transaction. Only possible for booked transactions
        (transaction_state='BOOKED').
        :param max_booking_date: max booking date in format YYYY-MM-DD
        :param min_booking_date: min booking date in format YYYY-MM-DD
        :return: Response object
        """
        url = '{0}/banking/v1/accounts/{1}/transactions'.format(self.api_url, account_uuid)
        params = {
            'transactionState': transaction_state,
            'paging-count': paging_count,
            'paging-first': paging_first,
            'min-bookingDate': min_booking_date,
            'max-bookingDate': max_booking_date,
        }
        if with_account:
            params['with-attr'] = 'account'

        response = self.session.get(url, params=params).json()
        return response
