from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow

description = """
This is an API that calls a Getaround rental price for a given car's specs.
"""

tags_metadata = [
    {
        "name": "Try out the API",
        "description": "A simple endpoint to try out!",
    },
    {
        "name": "Predictions",
        "description": "Let's get down to business!",
    }
]

app = FastAPI(
    title="Getaround project price prediction API — Aengus B",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

class PredictionFeatures(BaseModel):
    CarActeristics: list[list[int|str|bool]]

@app.get("/", tags=["Try out the API"])
async def index():
    """
    Simply returns a welcome message!
    """
    return {"message": "Hi! This is an API that calls a Getaround rental price for a given car's specs. Check out its other features!"}

@app.post("/predict", tags=["Predictions"])
async def predict(data: PredictionFeatures):
    """
    ### Prediction of the rental price given the car's specs!

    Inputs must be formatted as a list of sub-lists. Each sub-list represents one data point (ie. one car),
    so there may only be one sub-list within the outer list if you only wish to predict one price.
    Each sub-list must contain exactly 13 elements corresponding to the following variables: \n
    model_key:                    string \n
    mileage:                       int64 \n
    engine_power:                  int64 \n
    fuel:                         string \n
    paint_color:                  string \n
    car_type:                     string \n
    private_parking_available:      bool \n
    has_gps:                        bool \n
    has_air_conditioning:           bool \n
    automatic_car:                  bool \n
    has_getaround_connect:          bool \n
    has_speed_regulator:            bool \n
    winter_tires:                   bool \n

    ### Call it in python:
    ```
    import requests
    response = requests.post(url="https://aengusbl-getaround-price-predict-api.hf.space/predict", json=dict(CarActeristics=inputs_list_of_list))
    print(response.json())
    ```
    """
    explanatory_vars = ["model_key", "mileage", "engine_power", "fuel", "paint_color",
       "car_type", "private_parking_available", "has_gps",
       "has_air_conditioning", "automatic_car", "has_getaround_connect",
       "has_speed_regulator", "winter_tires"]
    inputs_df = pd.DataFrame({item[0]:item[1:] for item in list(zip(explanatory_vars, *data.CarActeristics))})

    model_uri = "s3://getaround-mlflow-artifactstore/2/b21d60925615456587e03b92d95843c4/artifacts/model"
    loaded_model = mlflow.pyfunc.load_model(model_uri)
    prediction = loaded_model.predict(inputs_df)

    response = {"prediction": prediction.tolist()}
    return response