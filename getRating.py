from transformers import pipeline
import pandas as pd
import pymongo
from pymongo.server_api import ServerApi

sentiment_pipeline = pipeline("sentiment-analysis")

uri = "mongodb+srv://main:main123@cluster0.wda04dt.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

db = client["Ratings"]
collection = db["RatingCollections"]


def getReviews(gameName):
    data = pd.read_csv(f"gameReviews/{gameName}.csv")
    reviews = list(data.Review)
    for i in range(len(reviews)):
        if len(reviews[i].split(" ")):
            reviews[i] = reviews[i][:512]

    return reviews


def process(gameName):
    # Call the getReviews() function to get the reviews
    print("running sentiment analysis for " + gameName)
    reviews = getReviews(gameName)
    res = sentiment_pipeline(reviews)
    ratings = []
    for i in res:
        if i["label"] == "POSITIVE":
            if i["score"] >= 0.999:
                i["score"] = 1
            ratings.append(i["score"])
        else:
            if i["score"] <= 0.099:
                i["score"] = 0
            ratings.append(1-i["score"])

    avg_rating = sum(ratings) / len(ratings) * 10
    avg_rating = round(avg_rating, 2)

    print(f"\n-------- {gameName} result: {avg_rating} --------")

    # Upload the results to MongoDB
    document = {
        'rating': str(avg_rating),
        'name': gameName,
        'cover': 'https://i.kym-cdn.com/entries/icons/mobile/000/033/421/cover2.jpg'
    }

    collection.insert_one(document)
    print("Result uploaded to MongoDB.")
