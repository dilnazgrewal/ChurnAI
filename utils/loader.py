import joblib
from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"


@lru_cache(maxsize=1)
def load_pipeline():
    return joblib.load(MODEL_DIR / "churn_pipeline.pkl")


@lru_cache(maxsize=1)
def load_threshold():
    return joblib.load(MODEL_DIR / "threshold.pkl")


@lru_cache(maxsize=1)
def load_shap_background():
    return joblib.load(MODEL_DIR / "shap_background.pkl")


@lru_cache(maxsize=1)
def load_feature_mapping():
    return joblib.load(MODEL_DIR / "feature_name_mapping.pkl")


@lru_cache(maxsize=1)
def load_readable_feature_names():
    return joblib.load(MODEL_DIR / "readable_feature_names.pkl")