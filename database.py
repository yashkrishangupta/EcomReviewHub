import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

DATA_DIR = 'data'

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_collection_path(collection_name: str) -> str:
    return os.path.join(DATA_DIR, f'{collection_name}.json')

def load_collection(collection_name: str) -> List[Dict]:
    ensure_data_dir()
    path = get_collection_path(collection_name)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_collection(collection_name: str, data: List[Dict]):
    ensure_data_dir()
    path = get_collection_path(collection_name)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

class Collection:
    def __init__(self, name: str):
        self.name = name
    
    def find(self, query: Dict = None) -> List[Dict]:
        data = load_collection(self.name)
        if not query:
            return data
        
        results = []
        for doc in data:
            if self._matches(doc, query):
                results.append(doc)
        return results
    
    def find_one(self, query: Dict) -> Optional[Dict]:
        results = self.find(query)
        return results[0] if results else None
    
    def insert_one(self, document: Dict) -> Dict:
        data = load_collection(self.name)
        if '_id' not in document:
            document['_id'] = str(uuid.uuid4())
        data.append(document)
        save_collection(self.name, data)
        return {'inserted_id': document['_id']}
    
    def insert_many(self, documents: List[Dict]) -> Dict:
        data = load_collection(self.name)
        inserted_ids = []
        for doc in documents:
            if '_id' not in doc:
                doc['_id'] = str(uuid.uuid4())
            data.append(doc)
            inserted_ids.append(doc['_id'])
        save_collection(self.name, data)
        return {'inserted_ids': inserted_ids}
    
    def update_one(self, query: Dict, update: Dict) -> Dict:
        data = load_collection(self.name)
        modified = 0
        for i, doc in enumerate(data):
            if self._matches(doc, query):
                if '$set' in update:
                    data[i].update(update['$set'])
                else:
                    data[i].update(update)
                modified = 1
                break
        save_collection(self.name, data)
        return {'modified_count': modified}
    
    def delete_one(self, query: Dict) -> Dict:
        data = load_collection(self.name)
        deleted = 0
        for i, doc in enumerate(data):
            if self._matches(doc, query):
                del data[i]
                deleted = 1
                break
        save_collection(self.name, data)
        return {'deleted_count': deleted}
    
    def delete_many(self, query: Dict) -> Dict:
        data = load_collection(self.name)
        original_count = len(data)
        data = [doc for doc in data if not self._matches(doc, query)]
        deleted = original_count - len(data)
        save_collection(self.name, data)
        return {'deleted_count': deleted}
    
    def drop(self):
        save_collection(self.name, [])
    
    def count_documents(self, query: Dict = None) -> int:
        return len(self.find(query if query else {}))
    
    def distinct(self, field: str) -> List:
        data = load_collection(self.name)
        values = set()
        for doc in data:
            if field in doc:
                values.add(doc[field])
        return list(values)
    
    def _matches(self, doc: Dict, query: Dict) -> bool:
        for key, value in query.items():
            if key not in doc:
                return False
            if doc[key] != value:
                return False
        return True

class Database:
    def __init__(self, name: str):
        self.name = name
        self._collections = {}
    
    def __getitem__(self, collection_name: str) -> Collection:
        if collection_name not in self._collections:
            self._collections[collection_name] = Collection(collection_name)
        return self._collections[collection_name]
    
    def __getattr__(self, collection_name: str) -> Collection:
        return self[collection_name]

class MongoDBSimulator:
    def __init__(self):
        self._databases = {}
    
    def __getitem__(self, db_name: str) -> Database:
        if db_name not in self._databases:
            self._databases[db_name] = Database(db_name)
        return self._databases[db_name]
    
    def __getattr__(self, db_name: str) -> Database:
        return self[db_name]

db = MongoDBSimulator()['ecommerce_db']
products_collection = db['products']
reviews_collection = db['reviews']
