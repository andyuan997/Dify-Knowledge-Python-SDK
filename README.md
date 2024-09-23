# Dify-Knowledge-Python-SDK

A Python SDK for interacting with the Dify Knowledge Base API. This library provides convenient methods for creating, updating, and managing documents and datasets within the Dify Knowledge Base system.

## Features
- Create, update, and delete datasets (knowledge bases)
- Create, update, and delete documents (text and files)
- Query document indexing status
- Manage document segments (add, update, delete)

## Installation

To install the SDK, clone this repository and install the required `requests` package:

```bash
git clone https://github.com/your-username/dify-knowledge-sdk-python.git
cd dify-knowledge-sdk-python
pip install requests
```

## Exsample
### Initialize the SDK
```python
# Initialize the client with your API key
api_key = 'your_api_key'
api_url = 'your_api_url'

client = DifySdkClient(api_key, your_api_url)
```
### Create a Dataset
```python
dataset_id = client.create_dataset('My New Dataset')
print(f"Created dataset with ID: {dataset_id}")
```

### Create a Document from Text
```python
document = client.create_document_from_text(dataset_id, 'Document Title', 'This is the content of the document.')
print(f"Created document: {document}")
```

### Check Document Index Status
```python
status = client.index_status(dataset_id, 'batch_id')
print(f"Document index status: {status}")
```

### Add a Document Segment
```python
segment = {
    "content": "This is the segment content.",
    "answer": "This is the segment answer.",
    "keywords": ["keyword1", "keyword2"]
}
client.add_segment(dataset_id, document_id, [segment])
print("Added segment to document.")
```

### Contributing
Feel free to submit issues or pull requests. All contributions are welcome!

### License
This project is licensed under the MIT License.
