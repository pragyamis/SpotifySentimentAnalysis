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

class SentAnalysisModelTraining(object):
    def __init__(self):
        print("Initializing SentAnalysisModelTraining!!");
        self.appName = "Sentiment Analysis in Spark"
        # create Spark session
        self.spark = SparkSession.builder.appName(self.appName) \
            .config("spark.executor.heartbeatInterval", "200000") \
            .config("spark.network.timeout", "300000") \
            .getOrCreate()
        self.model_name = "prediction_pipeline"
        self.pipeline = Pipeline.load(self.model_name)
        return

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
