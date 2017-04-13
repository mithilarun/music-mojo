
import nltk
import re
from nltk.corpus import stopwords
from random import shuffle
from nltk.tokenize import word_tokenize

"""
Extracts features from the given file containing sentences and tags.

getTokenizedData returns a list of training data. Each item in the list contains
the list of words in that sentence and the tag.
[
	[['Item', 'Does', 'Not', 'Match', 'Picture', '.'], '0'],
	[['Great', 'brunch', 'spot', '.'], '1'],
	 ....

]
"""

class ExtractFeatures:


	def __init__(self, filePath):
		self.filePath = filePath

	def getTokenizedData(self):
		
		# Read the file
		print ''
		print ("Extracting training data ")
		stops = set(stopwords.words("english"))
		result = []
		for line in open(self.filePath):
			
			sentence, tag = line.split('\t')

			# Remove all non letters from the sentence
			# We need to rethink this logic since smileys and
			# other emoticons will be usefull in sentimental 
			# analysis.
			sentence = re.sub("[^a-zA-Z]", " ", sentence) 

			# Convert the sentence into list of words.
			tokenizedlist = word_tokenize(sentence)

			# Remove all stop words
			tokenizedlist = [word for word in tokenizedlist if word not in stops]

			# Store the tokenized sentence and its tag to a list.
			item = [tokenizedlist, tag.rstrip()]
			result.append(item)

		print ("Extracted tokenized words from training data - " + self.filePath)
		shuffle(result)
		
		finalData = {}
		count = len(result)
		percentageOfTrainingData = 0.8
		trainDataIndex = int(count * percentageOfTrainingData)

		finalData['train'] = result[:trainDataIndex]
		finalData['test'] = result[trainDataIndex:]
		return finalData


	'''
	Uses valence data from http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
	The dataset contains words marked in range [-5,5] 
	'''
	def getValenceDict(self):
		valenceDict = dict(map(lambda (k,v): (k,int(v)), 
                     [ line.split('\t') for line in open('./data/AFINN/AFINN-111.txt') ]))
		return valenceDict
