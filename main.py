from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import uvicorn

# Load datasets
try:
    food_data_path = "dataset/Dataset Makanan Pedagang.csv"
    ratings_data_path = "dataset/Rating.csv"
    model_path = "model.keras"

    food_data = pd.read_csv(food_data_path)
    ratings_data = pd.read_csv(ratings_data_path)

    # Normalize temperature format
    food_data['temperature'] = food_data['temperature'].str.replace("–", "-", regex=False)

    # Parse temperature range
    def parse_temperature_range(temp_range):
        try:
            temp_min, temp_max = map(int, temp_range.split(" - "))
            return temp_min, temp_max
        except Exception:
            raise ValueError(f"Invalid temperature range format: {temp_range}")

    food_data[['temp_min', 'temp_max']] = food_data['temperature'].apply(
        lambda x: pd.Series(parse_temperature_range(x))
    )

    # Load the Keras model
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    raise RuntimeError(f"Error initializing application: {e}")

# Define FastAPI app
app = FastAPI(
    title="Enhanced Street Vendor Food Recommendations API",
    description="Provides street food recommendations based on actual ratings and user preferences.",
    version="2.0"
)

# Input schema
class RecommendationRequest(BaseModel):
    user_id: int
    weather_main: str
    temp_min: float
    temp_max: float

# Output schema
class FoodRecommendation(BaseModel):
    id: int
    merchant_id: int
    name: str
    price: int
    description: str
    average_rating: float

class RecommendationResponse(BaseModel):
    recommendations: List[FoodRecommendation]

@app.get("/")
def root():
    return {"message": "Welcome to the Enhanced Street Vendor Food Recommendations API!"}

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    try:
        user_id = request.user_id
        weather_main = request.weather_main.lower()
        temp_min = request.temp_min
        temp_max = request.temp_max

        # Validate weather_main
        valid_weather = ["clear", "clouds", "drizzle", "rain"]
        if weather_main not in valid_weather:
            raise HTTPException(status_code=400, detail="Invalid weather_main. Choose from: Clear, Clouds, Drizzle, Rain.")

        # Check if user exists
        if user_id not in ratings_data['user_id'].values:
            raise HTTPException(status_code=404, detail="User ID not found.")

        # Get unrated foods
        user_ratings = ratings_data[ratings_data['user_id'] == user_id]
        rated_food_ids = user_ratings['merchant_id'].tolist()
        food_not_rated = food_data[~food_data['merchant_id'].isin(rated_food_ids)]

        # Filter by weather_main
        food_not_rated = food_not_rated[
            food_not_rated['weather_main'].str.lower().str.contains(weather_main)
        ]

        # Filter by temperature range
        food_not_rated = food_not_rated[
            (food_not_rated['temp_min'] <= temp_min) & (food_not_rated['temp_max'] >= temp_max)
        ]

        # Check if any foods are left
        if food_not_rated.empty:
            raise HTTPException(status_code=404, detail="No food items match the criteria.")

        # Calculate average rating for each food item
        avg_ratings = ratings_data.groupby('merchant_id')['rating'].mean().reset_index()
        avg_ratings.columns = ['merchant_id', 'average_rating']

        # Merge with food_not_rated
        food_not_rated = food_not_rated.merge(avg_ratings, on='merchant_id', how='left')

        # Use Keras model for prediction (if applicable)
        # For example, predict relevance scores using the model:
        features = food_not_rated[['price', 'average_rating']].values
        food_not_rated['relevance_score'] = model.predict(features).flatten()

        # Sort by relevance score and select top 10
        recommended_foods = food_not_rated.sort_values(by='relevance_score', ascending=False).head(10)

        # Use the original dataset's ID
        recommendations = recommended_foods[['id', 'merchant_id', 'name', 'price', 'description', 'average_rating']].to_dict(orient='records')

        return {"recommendations": recommendations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Start the server
port = int(os.environ.get("PORT", 8080))  # Use port from environment variable or default to 8080
print(f"Starting server at http://0.0.0.0:{port}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)