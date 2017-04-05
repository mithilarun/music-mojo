

from extractFeatures import ExtractFeatures
import nltk.classify.util
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier

"""
Class that generate the sentiment of the given sentence.

Initializing the class will train the classifier with the 
training data.

Then you can use the method getSEntiments(message) to get the sentiment 
value.

"""
class SentimentalAnalyzer:

	def __init__(self):
		self.valenceDict = {}
		self.classifier = None
		self.initializeValenceDict()

	'''
	Uses valence data from http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
	The dataset contains words marked in range [-5,5] 
	'''
	def initializeValenceDict(self):
		for line in open('./data/AFINN/AFINN-111.txt'):
			word, valenceValue = line.split('\t')
			self.valenceDict[word] = int(valenceValue.rstrip())
		self.trainNaiveBayes()
		

	'''
		Train a naivebayes classifer with the training data.
	'''
	def trainNaiveBayes(self):
		
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


	# Return 1 if happy 0 if sad
	def getSentiments(self, message):
		tokenizedwords = word_tokenize(message)
		return self.classifier.classify(self.word_feats(tokenizedwords))

obj = SentimentalAnalyzer() 
print obj.getSentiments('I am feeling happy')
