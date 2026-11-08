import joblib
import pandas as pd
from ml.dataset import extract_features


def predict_best(reqs, head):
    model, cols = joblib.load("ml/model.pkl")
    feats = pd.DataFrame([extract_features(reqs, head)])[cols]
    return model.predict(feats)[0]


if __name__ == "__main__":
    print(predict_best([98, 183, 37, 122, 14, 124, 65, 67], 53))