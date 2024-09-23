import json
import requests

class DifySdkClient:
    def __init__(self, api_key, api_url='http://10.231.17.35/v1'):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_document_from_text(self, dataset_id, document_name, document_text, indexing_technique='high_quality',
                                  process_rule=None):
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
        url = f"{self.api_url}/datasets?page={page}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('data', [])

    def create_dataset(self, name, permission='all_team_members'):
        url = f"{self.api_url}/datasets"
        data = {
            "name": name,
            "permission": permission
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete_dataset(self, dataset_id):
        url = f"{self.api_url}/datasets/{dataset_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    def update_document_via_text(self, dataset_id, document_id, document_name=None, document_text=None, process_rule=None):
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
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{batch}/indexing-status"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_document(self, dataset_id, document_id):
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    def get_docs(self, dataset_id, page=1, limit=20):
        url = f"{self.api_url}/datasets/{dataset_id}/documents?page={page}&limit={limit}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('data', [])

    def add_segment(self, dataset_id, document_id, segments):
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/segments"
        data = {"segments": segments}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_document_segments(self, dataset_id, document_id, keyword=None, status=None):
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
        url = f"{self.api_url}/datasets/{dataset_id}/documents/{document_id}/segments/{segment_id}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    def update_document_segment(self, dataset_id, document_id, segment_id, content, answer=None, keywords=None, enabled=True):
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
