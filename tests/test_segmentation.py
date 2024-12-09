import unittest
import pandas as pd
import numpy as np
from marketing_analytics.models import AdvancedSegmentationModel

class TestSegmentation(unittest.TestCase):
    def setUp(self):
        self.model = AdvancedSegmentationModel(n_segments=3)
        self.X = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100)
        })
        
    def test_fit_predict(self):
        segments = self.model.fit_predict(self.X)
        self.assertEqual(len(np.unique(segments)), 3)
        
    def test_segment_profiles(self):
        self.model.fit(self.X)
        profiles = self.model.get_segment_profiles(self.X)
        self.assertEqual(len(profiles), 3) 