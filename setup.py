from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="marketing-analytics-toolkit",
    version="0.1.1",
    author="Anil Cogalan",
    author_email="anilcogalan@gmail.com",
    description="Advanced marketing analytics toolkit for customer segmentation and analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anilcogalan/advanced_marketing_tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.2",
        "pandas>=1.2.0",
        "scikit-learn>=0.24.0",
        "tensorflow>=2.4.0",
        "networkx>=2.5",
        "plotly>=4.14.0",
        "lifelines>=0.25.0",
        "xgboost>=1.3.0",
        "shap>=0.40.0",
        "category_encoders>=2.3.0",
        "feature-engine>=1.2.0",
        "optuna>=2.10.0",
        "umap-learn>=0.5.3",
        "scipy>=1.7.0",
        "statsmodels>=0.13.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=0.5.0',
        ],
    }
) 