class DocumentService:

    def __init__(self, session, api_url):
        self.session = session
        self.api_url = api_url

    def get_documents(self, first_index=0, count=1000):
        """
        9.1.1. Fetch all documents in the PostBox

        :param first_index: Index of the first document, starting with 0. Defaults to 0
        :param count: Number of documents to be fetched. Max 1000. Defaults to 1000.
        :return: Response object
        """
        url = '{0}/messages/clients/user/v2/documents'.format(self.api_url)
        params = {
            'paging-first': first_index,
            'paging-count': count,
        }
        response = self.session.get(url, params=params).json()
        return response

    def get_document(self, document_id):
        """
        9.1.2. Fetch a specific document. The document will be marked as read when fetched.

        :param document_id: Document-ID
        :return: Document and the content type of the document
        """
        url = '{0}/messages/v2/documents/{1}'.format(self.api_url, document_id)
        response = self.session.get(url, headers={'Accept': 'application/pdf'})
        content_type = response.headers['content-type']
        return response.content, content_type
