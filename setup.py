from setuptools import setup, find_packages

setup(
    name="marketing_analytics",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.2',
        'pandas>=1.2.0',
        'scikit-learn>=0.24.0',
        'tensorflow>=2.4.0',
        'networkx>=2.5',
        'plotly>=4.14.0',
        'lifelines>=0.25.0',
        'xgboost>=1.3.0',
        'shap>=0.40.0',
        'category_encoders>=2.3.0',
        'feature-engine>=1.2.0',
        'optuna>=2.10.0',
        'imbalanced-learn>=0.8.1',
        'yellowbrick>=1.4',
        'umap-learn>=0.5.3',
        'scipy>=1.7.0',
        'statsmodels>=0.13.0',
        'seaborn>=0.11.0',
        'matplotlib>=3.3.0',
        'PyYAML>=5.4.1',
        'joblib>=1.0.0'
    ],
    author="Anil Cogalan",
    author_email="anilcogalan@gmail.com",
    description="Advanced Marketing Analytics Library",
    python_requires=">=3.7",
) 