import unittest
import pandas as pd
import numpy as np
from marketing_analytics.utils import AdvancedPreprocessor

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = AdvancedPreprocessor()
        self.data = pd.DataFrame({
            'numeric': [1, 2, np.nan, 4],
            'categorical': ['A', 'B', None, 'A']
        })
        
    def test_handle_missing_values(self):
        result = self.preprocessor.handle_missing_values(
            self.data,
            categorical_features=['categorical']
        )
        self.assertFalse(result.isnull().any().any())
        
    def test_scale_features(self):
        data = pd.DataFrame({
            'feature': [1, 2, 3, 4]
        })
        result = self.preprocessor.scale_features(data)
        self.assertTrue(abs(result.mean()[0]) < 1e-10) 