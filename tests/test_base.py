import unittest
import numpy as np
import pandas as pd
from marketing_analytics.core.base import BaseModel
from marketing_analytics.core.exceptions import ModelNotFittedError, ValidationError

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        class DummyModel(BaseModel):
            def fit(self, X, y=None):
                self.is_fitted = True
                return self
                
            def predict(self, X):
                if not self.is_fitted:
                    raise ModelNotFittedError()
                return np.ones(len(X))
                
        self.model = DummyModel()
        self.X = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
        
    def test_validation(self):
        # Test valid input
        self.model.validate_input(self.X)
        
        # Test invalid input
        with self.assertRaises(ValidationError):
            self.model.validate_input([1, 2, 3])
            
    def test_save_load(self):
        self.model.fit(self.X)
        self.model.save_model('dummy_model.pkl')
        
        loaded_model = self.model.load_model('dummy_model.pkl')
        self.assertTrue(loaded_model.is_fitted) 