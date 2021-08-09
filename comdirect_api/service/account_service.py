from typing import Any


class AccountService:
    def get_all_balances(self, without_account: bool = False) -> Any:
        """4.1.1. Request for account information, including cash balance and buying power, for all accounts.

        Args:
            without_account (bool, optional): Suppresses the master data of the accounts. Defaults to False.

        Returns:
            Any: Response object
        """
        url = "{0}/banking/clients/user/v2/accounts/balances".format(self.api_url)
        params = {"without-attr": "account"} if without_account else None
        response = self.session.get(url, params=params).json()
        return response

    def get_balance(self, account_uuid: str) -> Any:
        """4.1.2. Request for account information, including cash balance and buying power.

        Args:
            account_uuid (str): Account identifier

        Returns:
            Any: Response object
        """
        url = "{0}/banking/v2/accounts/{1}/balances".format(self.api_url, account_uuid)
        response = self.session.get(url).json()
        return response

    def get_account_transactions(
        self,
        account_uuid: str,
        with_account: bool = False,
        transaction_state: str = "BOTH",
        paging_count: int = 20,
        paging_first: int = 0,
        min_booking_date: str = None,
        max_booking_date: str = None,
    ) -> Any:
        """4.1.3 .Requests and returns a list of transactions for the given account.

        Fetches transactions for a specific account. Not setting a min_booking_date currently limits the result to
        the last 180 days due to an API limitation.

        Args:
            account_uuid (str): Account identifier
            with_account (bool, optional): Include account master data in the response. Defaults to False.
            transaction_state (str, optional): "BOTH", "BOOKED", or "NOTBOOKED". Defaults to "BOTH".
            paging_count (int, optional): [description]. Defaults to 20.
            paging_first (int, optional): Index of first returned transaction. Only possible for booked transactions
                (transaction_state='BOOKED'). Defaults to 0.
            min_booking_date (str, optional): min booking date in format YYYY-MM-DD. Defaults to None.
            max_booking_date (str, optional): max booking date in format YYYY-MM-DD. Defaults to None.

        Returns:
            Any: Response object
        """
        url = "{0}/banking/v1/accounts/{1}/transactions".format(
            self.api_url, account_uuid
        )
        params = {
            "transactionState": transaction_state,
            "paging-count": paging_count,
            "paging-first": paging_first,
            "min-bookingDate": min_booking_date,
            "max-bookingDate": max_booking_date,
        }
        if with_account:
            params["with-attr"] = "account"

        response = self.session.get(url, params=params).json()
        return response
