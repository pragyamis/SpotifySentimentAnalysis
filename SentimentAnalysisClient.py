import sentiment_prediction as sa

sent_prediction = sa.SentAnalysisModelTraining()

sentiment = sent_prediction.predict_sentiment('Awesome')
print("Sentiment is " + sentiment)