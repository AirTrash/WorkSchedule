from abc import ABC, abstractmethod
import json


class BaseStorage(ABC):
    @abstractmethod
    def save(self, key: str, data):
        pass

    @abstractmethod
    def get(self, key: str):
        pass



class JSStorage(BaseStorage):
    def __init__(self, filepath: str):
        self.cache = {}
        self.filepath = filepath
        self.load_data()


    def load_data(self):
        with open(self.filepath, "r") as file:
            self.cache = json.load(file)


    def get(self, key: str):
        return self.cache[key]


    def save(self, key: str, data):
        self.cache[key] = data
        with open(self.filepath, "w") as file:
            json.dump(self.cache, file, indent=4)
