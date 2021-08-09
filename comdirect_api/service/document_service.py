from typing import Any, Tuple


class DocumentService:
    def get_documents(self, first_index: int = 0, count: int = 1000) -> Any:
        """9.1.1. Delivers a list of documents for the customer.

        Args:
            first_index (int, optional): Index of the first document. Defaults to 0.
            count (int, optional): The maximum number of documents that will be returned. Defaults to 1000.

        Returns:
            Any: Response object
        """
        url = "{0}/messages/clients/user/v2/documents".format(self.api_url)
        params = {
            "paging-first": first_index,
            "paging-count": count,
        }
        response = self.session.get(url, params=params).json()
        return response

    def get_document(self, document_id: str) -> Tuple[Any, str]:
        """9.1.2. Download a document for the given UUID.

        Args:
            document_id (str): The unique ID of the document.

        Returns:
            Tuple[Any, str]: Tuple of (Document, Content type)
        """
        url = "{0}/messages/v2/documents/{1}".format(self.api_url, document_id)
        response = self.session.get(url, headers={"Accept": "application/pdf"})
        content_type = response.headers["content-type"]
        return response.content, content_type
