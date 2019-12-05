#import modules
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover, IDF
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import  MulticlassClassificationEvaluator


class SentAnalysis(object):
    def __init__(self):
        self.appName = "Sentiment Analysis in Spark"
        # create Spark session
        self.spark = SparkSession.builder.appName(self.appName) \
            .config("spark.executor.heartbeatInterval", "200000") \
            .config("spark.network.timeout", "300000") \
            .getOrCreate()

        self.data = None
        self.training_data = None
        self.testing_data = None
        self.pipeline = None
        self.cross_validator = None
        self.evaluator = None

        self.predict_training_data = None
        self.predict_testing_data = None
        self.cv_model = None
        return



    # read csv file into dataFrame with automatically inferred schema
    def read_data(self):
        emotion_csv = self.spark.read.csv('dataset/text_emotions1.csv', inferSchema=True, header=True)
        emotion_csv.show(truncate=False, n=10)
        emotion_csv.select("sentiment").distinct().show()
        print(emotion_csv)

        # select only "content" and "sentiment" column,
        # and cast "Sentiment" column data into integer
        self.data = emotion_csv.select("content", "sentiment")
        self.data.show(truncate=False, n=10)
        return self.data.count

    # divide data, 70% for training, 30% for testing
    def split_data(self):
        dividedData = self.data.randomSplit([0.9, 0.1])
        self.training_data = dividedData[0]  # index 0 = data training
        self.testing_data = dividedData[1]  # index 1 = data testing
        train_rows = self.training_data.count()
        test_rows = self.testing_data.count()
        print("Training data rows:", train_rows, "; Testing data rows:", test_rows)
        return

    def create_pipeline(self):
        # Creating all the pipeline elements
        tokenizer = Tokenizer(inputCol="content", outputCol="SentimentWords")
        labelStringIdx = StringIndexer(inputCol="sentiment", outputCol="label")
        stopwordsRemover = StopWordsRemover(inputCol=tokenizer.getOutputCol(), outputCol="RelevantWords")
        hashTF = HashingTF(inputCol=stopwordsRemover.getOutputCol(), outputCol="features")
        self.pipeline = Pipeline(stages=[tokenizer, labelStringIdx, stopwordsRemover, hashTF])

        lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=15, regParam=0.001, \
                                elasticNetParam=0.8, family="multinomial")

        self.evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
        # paramGrid = ParamGridBuilder()\
        #    .addGrid(lr.aggregationDepth,[2,5,10])\
        #    .addGrid(lr.elasticNetParam,[0.0, 0.5, 1.0])\
        #    .addGrid(lr.fitIntercept,[False, True])\
        #    .addGrid(lr.maxIter,[10, 15])\
        #    .addGrid(lr.regParam,[0.01, 0.1]) \
        #    .build()

        paramGrid = ParamGridBuilder() \
            .addGrid(lr.aggregationDepth, [2]) \
            .addGrid(lr.elasticNetParam, [0.0, 0.8]) \
            .addGrid(lr.fitIntercept, [False, True]) \
            .addGrid(lr.maxIter, [15]) \
            .addGrid(lr.regParam, [0.001]) \
            .build()

        # Create 5-fold CrossValidator
        self.cross_validator = CrossValidator(estimator=lr, estimatorParamMaps=paramGrid, evaluator=self.evaluator, numFolds=5)

        return

    # Fit the pipeline to training documents.
    def train_model(self):
        pipelineFit = self.pipeline.fit(self.training_data)
        dataset = pipelineFit.transform(self.training_data)

        # Run cross validations
        self.cv_model = self.cross_validator.fit(dataset)

        # this will likely take a fair amount of time because of the amount of models that we're creating and testing
        self.predict_training_data = self.cv_model.transform(dataset)
        print("The area under ROC for train set after CV  is {}".format(self.evaluator.evaluate(self.predict_training_data)))

        print("Training is done!")
        return

    # Fit the pipeline to training documents.
    def test_model(self):
        pipelineFit = self.pipeline.fit(self.testing_data)
        preparedTestData = pipelineFit.transform(self.testing_data)
        self.predict_testing_data = self.cv_model.transform(preparedTestData)
        print("The area under ROC for test set after CV  is {}".format(self.evaluator.evaluate(self.predict_testing_data)))

        print("Testing is done!")
        return



    def print_model_summary(self):
        predictionFinal = self.predict_training_data.select(
            "RelevantWords", "prediction", "label", "sentiment")
        predictionFinal.show(n=20, truncate=False)

        # check the accuracy
        correctPrediction = self.predict_testing_data.filter(
            self.predict_testing_data['prediction'] == self.predict_testing_data['label']).count()
        totalData = self.predict_testing_data.count()
        print("correct prediction:", correctPrediction, ", total data:", totalData,
              ", accuracy:", correctPrediction / totalData)

        trainingSummary = self.cv_model.bestModel.summary

        # Obtain the objective per iteration
        objectiveHistory = trainingSummary.objectiveHistory
        # print("objectiveHistory:")
        # for objective in objectiveHistory:
        #    print(objective)

        # for multiclass, we can inspect metrics on a per-label basis
        print("False positive rate by label:")
        for i, rate in enumerate(trainingSummary.falsePositiveRateByLabel):
            print("label %d: %s" % (i, rate))

        print("True positive rate by label:")
        for i, rate in enumerate(trainingSummary.truePositiveRateByLabel):
            print("label %d: %s" % (i, rate))

        print("Precision by label:")
        for i, prec in enumerate(trainingSummary.precisionByLabel):
            print("label %d: %s" % (i, prec))

        print("Recall by label:")
        for i, rec in enumerate(trainingSummary.recallByLabel):
            print("label %d: %s" % (i, rec))

        print("F-measure by label:")
        for i, f in enumerate(trainingSummary.fMeasureByLabel()):
            print("label %d: %s" % (i, f))

        accuracy = trainingSummary.accuracy
        falsePositiveRate = trainingSummary.weightedFalsePositiveRate
        truePositiveRate = trainingSummary.weightedTruePositiveRate
        fMeasure = trainingSummary.weightedFMeasure()
        precision = trainingSummary.weightedPrecision
        recall = trainingSummary.weightedRecall
        print("Accuracy: %s\nFPR: %s\nTPR: %s\nF-measure: %s\nPrecision: %s\nRecall: %s"
              % (accuracy, falsePositiveRate, truePositiveRate, fMeasure, precision, recall))
        return

def main():
    sent_analysis = SentAnalysis()
    sent_analysis.read_data()
    sent_analysis.split_data()
    sent_analysis.create_pipeline()
    sent_analysis.train_model()
    sent_analysis.test_model()
    sent_analysis.print_model_summary()

if __name__ == '__main__':
    main()

