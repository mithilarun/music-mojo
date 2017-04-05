from extractFeatures import ExtractFeatures

'''
	Uses bag of words and valence value as features
	to train a random forest.
'''
class RandomForestClassifer:


	def __init__(self):
		self.valenceDict = {}
		self.classifier = None

	def train(self):
		extracter = ExtractFeatures('./data/reviewsData.txt')
		self.valenceDict = extracter.getValenceDict()
		print self.valenceDict

