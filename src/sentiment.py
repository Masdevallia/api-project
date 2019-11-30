
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')

def sentimentAnalyzer(data):
    sid = SentimentIntensityAnalyzer()
    newdata = {}
    for key, value in data.items():
        newdata[key] = value
        newdata[f"sentiments_{key}"] = sid.polarity_scores(value)
    return newdata