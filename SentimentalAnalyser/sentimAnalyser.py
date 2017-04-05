

from naiveBayesClassifier import SentiNaiveBayesClassifier
from randomForestClassifier import RandomForestClassifer

"""
Class that generate the sentiment of the given sentence.

Initializing the class will train the classifier with the 
training data.

Then you can use the method getSEntiments(message) to get the sentiment 
value.

"""
class SentimentalAnalyzer:

	def __init__(self):
		
		self.classifier = RandomForestClassifer()
		# self.classifier = SentiNaiveBayesClassifier()
		self.classifier.train()
		
	
	# Return 1 if happy 0 if sad
	def getSentiments(self, message):
		return self.classifier.classify(message)

obj = SentimentalAnalyzer() 
print obj.getSentiments('I am feeling happy')
