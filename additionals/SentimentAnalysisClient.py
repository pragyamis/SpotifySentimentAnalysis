import sentiment_prediction as sa

sent_prediction = sa.SentAnalysisPrediction()

sentiment = sent_prediction.predict_sentiment('Awesome')
print("Sentiment is " + sentiment)