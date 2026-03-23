from fastapi import FastAPI
import boto3
import pickle
import os

app = FastAPI(title="ML Prediction API")

# Connect to LocalStack S3 (Mock AWS)
s3_client = boto3.client(
    "s3",
    endpoint_url="http://host.docker.internal:4566", # Connects out of the container to your host's LocalStack
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# Global variable to hold our model in memory
loaded_model = None

@app.on_event("startup")
async def load_model():
    global loaded_model
    print("Downloading model.pkl from LocalStack S3...")
    try:
        # Download the file from our mock bucket
        s3_client.download_file("ml-models-bucket", "model.pkl", "local_model.pkl")
        
        # Open and load the pickle file
        with open("local_model.pkl", "rb") as f:
            loaded_model = pickle.load(f)
            
        print(f"Model successfully loaded into memory: {loaded_model}")
    except Exception as e:
        print(f"Error loading model: {e}")
        loaded_model = {"error": "Failed to load from S3. Is LocalStack running?"}

@app.get("/predict")
def predict(input_data: str):
    # The API now returns the data processed by the "model"
    return {
        "status": "success",
        "input_received": input_data,
        "active_model": loaded_model,
        "prediction": f"AIOps analysis complete for: {input_data}"
    }