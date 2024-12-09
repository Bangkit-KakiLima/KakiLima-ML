# Ping - Kaki Lima Online - Machine Learning

## Bangkit Capstone Project 2024
Here is our repository for the Bangkit 2024 Capstone project - Machine Learning.

## Description
The Machine Learning model can be used to provide information about a Content-Based Filtering focuses on recommending items based on the characteristics or features of the food itself, rather than the behavior of other users. The idea is to find foods that are similar to the ones the user has previously interacted with or rated highly and Collaborative Filtering recommends food items based on the preferences of similar users. The system assumes that if users agree on one item, they are likely to agree on others. Collaborative filtering can either be user-based or item-based, but for simplicity, most systems use item-based collaborative filtering.

## TOOLS
* Python
* TensorFlow
* NumPy
* Pandas
* Matplotlib
* Google Colab

## Dataset
We made the dataset from scratch by specifying the variables manually in Excel. The variabel are merchant,	name,	description,	price, temperature,	weather_main
[Latest Dataset](https://github.com/Bangkit-KakiLima/KakiLima-ML/blob/main/dataset/Dataset%20Makanan%20Pedagang.csv)

## How To Recomend
The system will first filter the food items based on the weather condition. Then, it will narrow down the options based on the temperature range to suggest food suitable for the current temperature. The system will rank the remaining food items by user preferences (through Collaborative Filtering) and food characteristics (Content-Based Filtering).

### Response: The system will return a list of recommended food items with the following information:

Food Name: The name of the food item.
Merchant ID: The vendor offering the food.
Price: The price of the food item.
Description: A brief description of the food item.

## Benefit
* Personalized Experience: Recommendations are tailored to each user based on their preferences and past interactions.
* Weather-Aware: Suggests food based on real-time weather conditions, making sure the food matches the user’s environment.
* Variety: Combines Content-Based Filtering (recommending food similar to what the user likes) and Collaborative Filtering (recommending food liked by similar users) to ensure both personalized and diverse food options.
Average Rating: The average user rating for a food from highest to worst.

## How to Get Started:
1. Clone the repository.
2. Set up the environment and dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
4. Use the API to send a POST request to the `/recommend` endpoint with the required parameters (user ID, weather, and temperature).
