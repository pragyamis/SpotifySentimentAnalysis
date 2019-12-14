#import modules
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover, IDF
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, IndexToString
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import  MulticlassClassificationEvaluator
from pyspark.ml.classification import LogisticRegressionModel

class SentAnalysisPrediction(object):
    def __init__(self):
        print("Initializing SentAnalysisProdiction!!");
        self.appName = "Sentiment Analysis in Spark"
        # create Spark session
        self.spark = SparkSession.builder.appName(self.appName) \
            .config("spark.executor.heartbeatInterval", "200000") \
            .config("spark.network.timeout", "300000") \
            .getOrCreate()
        self.model_name = "prediction_pipeline"
        self.pipeline = Pipeline.load(self.model_name)
        return

    def predict_sentiment_with_cache(self, song_title, text, sentiment_cache):
        try:
            # if key doesn't exist, it throws a key error
            predicted_sentiment = sentiment_cache[song_title]
            print("found song in the sentiment cache {0}".format(song_title))
        except Exception as e:
            print("Exception while pulling data {0}".format(e))
            predicted_sentiment = self.predict_sentiment(text)
            sentiment_cache[song_title] = predicted_sentiment
            print("saved sentiment {0} data for {1} to cache".format(predicted_sentiment, song_title))
        return predicted_sentiment

    def predict_sentiment(self, text):
        cSchema = StructType().add("sentiment", StringType()).add("content", StringType())

        # notice extra square brackets around each element of list
        test_list = [["dummy", text]]
        rdd = self.spark.sparkContext.parallelize(test_list)
        df = self.spark.createDataFrame(rdd, schema=cSchema)
        fittedPipeline = self.pipeline.fit(df)
        final_result = fittedPipeline.transform(df)
        predicted_sentiment = final_result.collect()[0].predictionLabel
        print("Predicted Sentiment for {0} is {1}".format(text, predicted_sentiment))
        return predicted_sentiment
