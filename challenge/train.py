import pandas as pd
from .model import DelayModel
import joblib
import os
import argparse
from google.cloud import storage

MODEL_FILENAME = "delay_model.joblib"

class Train:
    @staticmethod
    def train_and_save(bucket_name: str):

        data = pd.read_csv("data/data.csv")
        
        model = DelayModel()
        features, target = model.preprocess(data, target_column="delay")
        model.fit(features, target)
        
        local_model_path = os.path.join("/tmp", MODEL_FILENAME)
        joblib.dump(model._model, local_model_path)

        # Upload model to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"model/{MODEL_FILENAME}")
        blob.upload_from_filename(local_model_path)
        print(f"Model successfully uploaded to gs://{bucket_name}/model/{MODEL_FILENAME}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train model and save to GCS.")
    parser.add_argument("--bucket-name", required=True, help="GCS bucket name.")
    args = parser.parse_args()
    
    Train.train_and_save(args.bucket_name)