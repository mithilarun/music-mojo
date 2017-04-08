from extractFeatures import ExtractFeatures
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

'''
	Uses bag of words and valence value as features
	to train a random forest.
'''
class RandomForestClassifer:


	def __init__(self):
		self.valenceDict = {}
		self.classifier = None
		self.countVectorizer = None
	def train(self):
		
		extracter = ExtractFeatures('./data/reviewsData.txt')
		self.valenceDict = extracter.getValenceDict()
		
		tokenizedData = extracter.getTokenizedData()
		trainingData = tokenizedData['train']

		print ''
		print 'Training Random Forest Classifier'
		print 'Training data size = ', len(trainingData)
		print ''

		train_wordList = []
		train_labels = []
		for item in trainingData:
			train_wordList.append(" ".join( item[0] ))
			train_labels.append(item[1])

		self.countVectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 
		countFeatures = self.countVectorizer.fit_transform(train_wordList)
		

		self.classifier = RandomForestClassifier(n_estimators = 50) 
		self.classifier = self.classifier.fit(countFeatures.toarray(), train_labels)
		print 'Training Random Forest Classifier Completed'
		

	def validateClassifier(self):

		extracter = ExtractFeatures('./data/reviewsData.txt')
		tokenizedData = extracter.getTokenizedData()
		testData = tokenizedData['test']

		print ''
		print 'Validating Random Forest Classifier'
		print 'Test data size = ', len(testData)
		print ''

		test_wordList = []
		test_labels = []
		for item in testData:
			test_wordList.append(" ".join( item[0] ))
			test_labels.append(item[1])
		countTestFeatures = self.countVectorizer.transform(test_wordList)
		predictedVal = self.classifier.predict(countTestFeatures.toarray())
		
		score = accuracy_score(test_labels,predictedVal)
		print 'Accuracy: ', score

	def classify(self, statusMessage):
		print statusMessage
		countFeatures = self.countVectorizer.transform([statusMessage])
		print 'countFeatures: ',countFeatures
		val = self.classifier.predict(countFeatures.toarray())
		print 'Prediction: ', val
		return val[0]

