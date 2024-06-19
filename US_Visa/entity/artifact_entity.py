from dataclasses import dataclass

@dataclass
class dataingestionartifact:
    train_file_path: str
    test_file_path: str

@dataclass
class datavalidationartifact:
    validation_status: bool
    message: str
    drift_report_file_path: str

@dataclass
class datatransformationartifact:
    transformed_train_file_path: str 
    transformed_test_file_path: str 
    transformed_object_file_path: str 
