import json
import requests

import json
import requests

class DifySdkClient:
    def __init__(self, api_key, api_url):
        """
        Initialize the SDK client with API key and base URL.
        
        :param api_key: Your API key for authentication.
        :param api_url: Base URL of the Dify API.
        """
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_document_from_text(self, dataset_id, document_name, document_text, indexing_technique='high_quality',
                                  process_rule=None):
        """
        Create a document from text content.
        
        :param dataset_id: ID of the knowledge base (dataset).
        :param document_name: Name of the document.
        :param document_text: Content of the document.
        :param indexing_technique: Indexing method (high_quality or economy).
        :param process_rule: Processing rules for document creation.
        :return: Response containing document creation result.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/document/create_by_text"
        if process_rule is None:
            process_rule = {"mode": "automatic"}
        data = {
            "name": document_name,
            "text": document_text,
            "indexing_technique": indexing_technique,
            "process_rule": process_rule
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_document_from_file(self, dataset_id, file_path, process_rule=None, original_document_id=None,
                                  indexing_technique='high_quality'):
        """
        Create a document by uploading a file.
        
        :param dataset_id: ID of the knowledge base (dataset).
        :param file_path: Path to the file to be uploaded.
        :param process_rule: Processing rules for document creation.
        :param original_document_id: ID of the original document (for updates).
        :param indexing_technique: Indexing method (high_quality or economy).
        :return: Response containing document creation result.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/document/create_by_file"
        if process_rule is None:
            process_rule = {"mode": "automatic"}
        data = {
            "indexing_technique": indexing_technique,
            "process_rule": process_rule
        }
        if original_document_id:
            data['original_document_id'] = original_document_id
        data_string = json.dumps(data)
        files = {
            "data": (None, data_string, 'text/plain'),
            "file": open(file_path, "rb")
        }
        response = requests.post(url, headers=self.headers, files=files)
        response.raise_for_status()
        return response.json()

    def get_datasets(self, page=1, limit=20):
        """
        Retrieve a list of knowledge bases (datasets).
        
        :param page: Page number for pagination.
        :param limit: Number of results per page (default: 20).
        :return: List of datasets.
        """
        url = f"{self.api_url}/datasets?page={page}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('data', [])

    def create_dataset(self, name, permission='all_team_members'):
        """
        Create a new dataset (knowledge base).
        
        :param name: Name of the new dataset.
        :param permission: Permission level (default: all_team_members).
        :return: Response containing dataset creation result.
        """
        url = f"{self.api_url}/datasets"
        data = {
            "name": name,
            "permission": permission
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_dataset(self, dataset_id):
        """
        Delete a dataset (knowledge base).
        
        :param dataset_id: ID of the dataset to delete.
        :return: Response confirming deletion.
        """
        url = f"{self.api_url}/datasets/{dataset_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    def update_document_via_text(self, dataset_id, document_id, document_name=None, document_text=None, process_rule=None):
        """
        Update a document using text content.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document to update.
        :param document_name: New name for the document (optional).
        :param document_text: New text content for the document (optional).
        :param process_rule: Processing rules (optional).
        :return: Response containing document update result.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/update_by_text"
        data = {}
        if document_name:
            data["name"] = document_name
        if document_text:
            data["text"] = document_text
        if process_rule:
            data["process_rule"] = process_rule
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def update_document_from_file(self, dataset_id, document_id, file_path, document_name=None, process_rule=None):
        """
        Update a document by uploading a new file.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document to update.
        :param file_path: Path to the new file.
        :param document_name: New name for the document (optional).
        :param process_rule: Processing rules (optional).
        :return: Response containing document update result.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/update_by_file"
        data = {}
        if document_name:
            data["name"] = document_name
        if process_rule is None:
            process_rule = {"mode": "automatic"}
        data["process_rule"] = process_rule
        data_string = json.dumps(data)
        files = {
            "data": (None, data_string, 'text/plain'),
            "file": open(file_path, "rb")
        }
        response = requests.post(url, headers=self.headers, files=files)
        response.raise_for_status()
        return response.json()

    def index_status(self, dataset_id, batch):
        """
        Get the indexing status of a document batch.
        
        :param dataset_id: ID of the knowledge base.
        :param batch: Batch ID of the document.
        :return: Indexing status of the document.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{batch}/indexing-status"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_document(self, dataset_id, document_id):
        """
        Delete a document from a dataset.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document to delete.
        :return: Response confirming deletion.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    def get_docs(self, dataset_id, page=1, limit=20):
        """
        Retrieve a list of documents in a dataset.
        
        :param dataset_id: ID of the knowledge base.
        :param page: Page number for pagination.
        :param limit: Number of documents per page (default: 20).
        :return: List of documents.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents?page={page}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('data', [])

    def add_segment(self, dataset_id, document_id, segments):
        """
        Add segments to a document.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document to add segments to.
        :param segments: List of segment data (content, answer, keywords).
        :return: Response confirming the segments were added.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/segments"
        data = {"segments": segments}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_document_segments(self, dataset_id, document_id, keyword=None, status=None):
        """
        Retrieve segments of a document.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document.
        :param keyword: Keyword for filtering (optional).
        :param status: Status for filtering (optional).
        :return: List of document segments.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/segments"
        params = {}
        if keyword:
            params['keyword'] = keyword
        if status:
            params['status'] = status
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def delete_document_segment(self, dataset_id, document_id, segment_id):
        """
        Delete a segment from a document.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document.
        :param segment_id: ID of the segment to delete.
        :return: Response confirming the segment was deleted.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    def update_document_segment(self, dataset_id, document_id, segment_id, content, answer=None, keywords=None, enabled=True):
        """
        Update a segment of a document.
        
        :param dataset_id: ID of the knowledge base.
        :param document_id: ID of the document.
        :param segment_id: ID of the segment to update.
        :param content: New content for the segment.
        :param answer: New answer for the segment (optional).
        :param keywords: New keywords for the segment (optional).
        :param enabled: Whether the segment is enabled (default: True).
        :return: Response confirming the update.
        """
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}"
        segment_data = {"content": content, "enabled": enabled}
        if answer:
            segment_data["answer"] = answer
        if keywords:
            segment_data["keywords"] = keywords
        data = {"segment": segment_data}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    api_key = 'your_api_key'
    api_url = 'your_api_url'
    
    client = DifySdkClient(api_key, your_api_url)  
