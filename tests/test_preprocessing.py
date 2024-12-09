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
        
    def test_init(self):
        """Test initialization"""
        self.assertEqual(self.preprocessor.scaling_method, 'robust')
        self.assertEqual(self.preprocessor.encoding_method, 'target')
        self.assertEqual(self.preprocessor.imputation_method, 'knn') 