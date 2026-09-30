from setuptools import setup, find_packages

setup(
    name="customer_churn_prediction",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy==2.5.3",
        "scikit-learn==1.9.1",
        "scipy==1.16.3",
        "streamlit",
        "joblib",
        "fastapi",
        "uvicorn",
        "requests",
    ],
)