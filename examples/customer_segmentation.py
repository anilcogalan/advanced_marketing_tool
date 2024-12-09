from marketing_analytics.models import AdvancedSegmentationModel
from marketing_analytics.utils import AdvancedPreprocessor
import pandas as pd

# Load data
data = pd.read_csv('customer_data.csv')

# Preprocess
preprocessor = AdvancedPreprocessor()
processed_data = preprocessor.handle_missing_values(data)

# Segment
model = AdvancedSegmentationModel(n_segments=5)
segments = model.fit_predict(processed_data) 