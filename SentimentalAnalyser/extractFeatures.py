from nltk.tokenize import word_tokenize
import nltk

class ExtractFeatures:


	def __init__(self, filePath):
		self.filePath = filePath

	def getTokenizedData(self):
		# Read the file
		for line in open(self.filePath):
			word, tag = line.split('\t')
			print tag
			
		# Tokenize the data