from abc import ABC, abstractmethod
import re
from pathlib import Path

from mace_aze.config import (
    RAWDATA_DIR,
    DATASET_DIR,
    raw_dataset_path,
    dataset_path
)

class Record(ABC):
    @staticmethod
    def validate(label: str, file_type: str):
        if not isinstance(label, str):
            raise TypeError(f'Provided paramter is not string')
        
        if not isinstance(file_type, str):
            raise TypeError(f'Extensio is not a string')
        
        pattern = r'^([a-zA-Z0-9]+_)*[a-zA-Z0-9]+$'
        if not re.fullmatch(pattern, label):
            raise ValueError(f'{label} is not a valid label')
        
    
    def __init__(self, label: str, file_type: str):
        Record.validate(label=label, file_type=file_type)
        self.label = label
        self.file_type = file_type

    

    def file_path(self)->str:
        '''Sends path version of label.
        E.g abc_def returns abc/def and so on '''
        return '/'.join(self.label.split('_'))

    @staticmethod
    @abstractmethod
    def parse(data: tuple):
        ...
    
    @staticmethod
    @abstractmethod
    def extract_path(label: str, *args):
        ...

    @abstractmethod
    def db_format(self):
        ...
    
    @abstractmethod
    def file_name(self, *args, **kwargs):
        ...

    @abstractmethod
    def full_path(self)->Path:
        ...

class RawDataset(Record):
    def __init__(self, label: str, file_type: str = 'xyz'):
        super().__init__(label=label, file_type=file_type)

    def db_format(self)->tuple:
        return (self.file_type, self.label)
    
    def file_name(self):
        path = '__'.join([self.label, RAWDATA_DIR])
        return f'{path}.{self.file_type}'
  
    def full_path(self):
        return raw_dataset_path/Path(f'{self.file_path()}/{self.file_name()}')
    
    @staticmethod
    def extract_path(label, file_type='xyz'):
        return RawDataset(label, file_type).full_path()
    
    @staticmethod
    def parse(data: tuple):
        '''Expects (file_type, label)'''
        return RawDataset(label=data[1], file_type = data[0])
    
class Dataset(Record):
    def __init__(self, label: str, operation: str, file_type: str = 'xyz'):
        super().__init__(label=label, file_type=file_type)
        if not isinstance(operation, str):
            raise TypeError("operation parameter is not string")
        self.operation = operation

    def db_format(self)->tuple:
        return (self.file_type, self.label, self.operation)
    
    def file_name(self):
        path = '__'.join([self.label, DATASET_DIR, self.operation])
        return f'{path}.{self.file_type}'
    
    def full_path(self):
        return dataset_path/Path(f'{self.file_path()}/{self.file_name()}')
    
    @staticmethod
    def extract_path(label, operation, file_type='xyz'):
        return Dataset(label=label, file_type=file_type, operation=operation).full_path()
    
    @staticmethod
    def parse(data: tuple):
        '''Expects (file_type, label, operation)'''
        return Dataset(label=data[1],  operation=data[2], file_type = data[0])