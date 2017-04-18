import nltk
from merge import *
from createTestDataset import *
import xml.etree.ElementTree as ET
import sys
def summarize(testFilePath,trainFolder):
	trainData=getTrainingData()
	sids,testData=getTestdata(testFilePath)#give filepath of test data

	classifier = nltk.classify.NaiveBayesClassifier.train(trainData) 
	result = classifier.classify_many(testData)

	i=0
	ans={}
	for r in result:
		if r == 'y':
			ans[sids[i]]=1    # would give corresponding sids
		i = i+1	
	return ans

if __name__=='__main__':
	if len(sys.argv)<2:
		print "Usage: python "+sys.argv[0]+" 'path of test chunk' "
		sys.exit(0)
	testFilePath=sys.argv[1]
	trainFolder="splitted"
	ans_ids=summarize(testFilePath,trainFolder)
	fo = open("resultids","w")
	summary=[]
	tree = ET.parse(testFilePath)
	root=tree.getroot()
	print root.iter('DOC')
	for doc in root.iter('DOC'):
		for text in doc.iter('Text'):
			for sentence in text.iter('Sent'):
				if ans_ids.has_key(sentence.attrib['id']):
					summary.append((sentence.text,sentence.attrib['id']))#sentence, sentence id
					fo.write(sentence.attrib['id']+"\n")
				else:
					print "does not have key " +sentence.attrib['id']
	print "summary is " + testFilePath
	target = open("./summaryOfTest/" + testFilePath.rsplit('/',1)[1], 'w')
	print summary
	for i in summary:
		#print "("+i[1]+") : "+i[0].encode('utf-8') +"\n"
		target.write("("+i[1]+") : "+i[0].encode('utf-8') +"\n")
	target.close()
	fo.close()
