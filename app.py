from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pickle
import pandas as pd
import json
import numpy as np
import os
from flask_cors import CORS
from flask_cors import cross_origin


app = Flask(__name__)

# Configure CORS for all routes
CORS(app)


# Load data from the .pkl file
def load_data_from_pkl(file_name):
    file_path = os.path.abspath(os.path.join(os.getcwd(), file_name))
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    return data


# Convert data to JSON
def convert_to_json(data):
    # Convert DataFrame to JSON (replace with appropriate conversion based on data type)
    json_data = data.to_json(orient="records")
    return json.loads(json_data)  # Parse JSON string to dictionary


def recommend_courses(keyword):
    df = load_data_from_pkl("df.pkl")
    pt = load_data_from_pkl("pt.pkl")
    similarity_scores = load_data_from_pkl("similarity_scores.pkl")

    courses = []
    for x in pt.index:
        if keyword in x:
            courses.append(x)

    suggestion = []

    for courses_name in courses:
        index = np.where(pt.index == courses_name)[0][0]
        similar_courses = sorted(
            list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True
        )[1:6]
        for i in similar_courses:
            suggestion.append(pt.index[i[0]])

    recommended_df = df[df["Subtitle"].isin(suggestion[1:10])]
    json_string = recommended_df.to_json(orient="records")
    return json.loads(json_string)


@app.route("/")
def index():
    return "Hello World!"


# API endpoint to return data as JSON
@app.route("/get_data", methods=["GET"])
def get_data():
    # Load data from .pkl file
    data = load_data_from_pkl("popular.pkl")

    # Convert data to JSON
    json_data = convert_to_json(data)

    return jsonify(json_data)


@app.route("/recommend/<user_input>", methods=["GET"])
@cross_origin()
def recommend(user_input):
    # Call the recommend function with the user input
    recommendation = recommend_courses(user_input)

    # Return the JSON response
    return jsonify(recommendation)


if __name__ == "__main__":
    app.run(debug=True)
