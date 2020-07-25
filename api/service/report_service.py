class ReportService:

    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get_report(self, product_type=None):
        """
        10.1.1. Fetch a report for all products

        :param product_type: Filter by one or more of ACCOUNT, CARD, DEPOT, LOAN, SAVINGS
            (list or comma-separated string)
            Defaults to None (all product types without filter)
        :return: Response object
        """
        url = '{0}/reports/participants/user/v1/allbalances'.format(self.api_url)
        params = {
            'productType': ','.join(product_type) if type(product_type) is list else product_type
        }
        response = self.session.get(url, params=params).json()
        return response
