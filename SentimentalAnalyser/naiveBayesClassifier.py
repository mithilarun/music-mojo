
from extractFeatures import ExtractFeatures
import nltk.classify.util
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

class SentiNaiveBayesClassifier:

	def __init__(self):
		self.classifier = None

	'''
		Train a naivebayes classifer with the training data.
	'''
	def train(self):
		
		# Get data from the extracter
		extracter = ExtractFeatures('./data/reviewsData.txt')
		tokenizedData = extracter.getTokenizedData()

		trainingData = tokenizedData['train']
		testData = tokenizedData['test']

		print ''
		print 'Training data size = ', len(trainingData)
		print 'Test data size = ', len(testData)
		print ''

		modifiedTrainingData = [(self.word_feats(item[0]), item[1]) for item in trainingData]
		modifiedTestData = [(self.word_feats(item[0]), item[1]) for item in testData]

		self.classifier = NaiveBayesClassifier.train(modifiedTrainingData)
		print 'accuracy:', nltk.classify.util.accuracy(self.classifier, modifiedTestData)

	def word_feats(self, words):
		return dict([(word, True) for word in words])


	def classify(self, statusMessage):
		tokenizedwords = word_tokenize(statusMessage)
		return self.classifier.classify(self.word_feats(tokenizedwords))