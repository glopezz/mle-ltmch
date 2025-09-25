import pandas as pd
from challenge.model import DelayModel
import joblib
import os

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "delay_model.joblib")

class Train:
    @staticmethod
    def train_and_save(data_path: str):

        data = pd.read_csv(data_path)
        
        model = DelayModel()
        features, target = model.preprocess(data, target_column="delay")
        model.fit(features, target)
        
        if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
        joblib.dump(model._model, MODEL_PATH)
        print(f"Model succesfully saved at {MODEL_PATH}")

if __name__ == "__main__":
    Train.train_and_save("data/data.csv")