# MLE Challenge


## 1. Implementation

-   **API (`challenge/api.py`):** A FastAPI application that exposes two main endpoints:
    -   `POST /predict`: Predicts flight delays. It validates incoming data using Pydantic models.
    -   `POST /train`: Triggers a model retraining process.
-   **Model Logic (`challenge/model.py`):** The `DelayModel` class encapsulates all ML logic, including data preprocessing, model fitting, and prediction. It is designed to be independent of the API layer.
-   **Training (`challenge/training.py`):** A simple script that orchestrates the training process by using the `DelayModel` class and saving the resulting model artifact.
-   **Validation (`challenge/validations.py`):** `Enum` classes are used to define the allowed values for categorical features, ensuring robust input validation at the API entry point.

## 2. Next Steps: GCP Deployment

The current implementation uses a local file system to store the model. The next step is to evolve this into a scalable, cloud-native architecture on GCP.

-   **Model & Data Storage**: Move model artifacts and datasets to a GCS bucket.
-   **CI/CD Automation**: Implement GitHub Actions to automate testing (CI) and deployment (CD). The CD pipeline will handle model retraining and API deployment on every push to the `main` branch.
-   **API Serving**: Deploy the containerized FastAPI application to **Cloud Run**. On startup, each instance will fetch the latest model from GCS, ensuring the API is always serving predictions with the most up-to-date model in a scalable, serverless environment.