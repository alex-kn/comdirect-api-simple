from typing import Any, List, Union


class ReportService:
    def get_report(self, product_type: Union[str, List[str]] = None) -> Any:
        """10.1.1. List of all balances for a client's own and connected products.

        Args:
            product_type (Union[str, List[str]], optional):
                Filter by one or more of "ACCOUNT", "CARD", "DEPOT", "LOAN", "SAVINGS"
                (list or comma-separated string). Defaults to None.

        Returns:
            Any: Response object
        """
        url = "{0}/reports/participants/user/v1/allbalances".format(self.api_url)
        params = {
            "productType": ",".join(product_type)
            if type(product_type) is list
            else product_type
        }
        response = self.session.get(url, params=params).json()
        return response
