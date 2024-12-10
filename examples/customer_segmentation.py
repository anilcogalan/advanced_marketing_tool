from marketing_analytics.models import AdvancedSegmentationModel
import pandas as pd

# Load data
data = pd.read_csv('customer_data.csv')

# Initialize model
model = AdvancedSegmentationModel(
    method='kmeans',
    n_segments=3,
    feature_selection=True
)

# Fit and analyze
segments = model.fit_predict(data)
profiles = model.get_segment_profiles(data)
recommendations = model.get_segment_recommendations(0, data)

print("Segment Profiles:", profiles)
print("Recommendations:", recommendations) 