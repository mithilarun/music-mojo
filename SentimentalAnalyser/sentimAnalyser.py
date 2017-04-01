

from nltk.tokenize import word_tokenize
import nltk
from extractFeatures import ExtractFeatures

class SentimentalAnalyzer:

	def __init__(self):
		self.valenceDict = {}
		self.initializeValenceDict()

	# Uses valence data from http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
	# The dataset contains words marked in range [-5,5] 
	def initializeValenceDict(self):
		for line in open('./data/AFINN/AFINN-111.txt'):
			word, valenceValue = line.split('\t')
			self.valenceDict[word] = int(valenceValue.rstrip())
		self.trainNaiveBayes()
		

	def trainNaiveBayes(self):
		# Get data from the 
		extracter = ExtractFeatures('./data/reviewsData.txt')
		extracter.getTokenizedData()

	# Return 1 if happy 0 if sad
	def getSentiments(self, message):
		tokenizedwords = word_tokenize(message)
		return 1

obj = SentimentalAnalyzer() 
obj.getSentiments('hello there i am here')
