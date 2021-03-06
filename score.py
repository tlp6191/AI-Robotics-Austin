#!/usr/bin/python
from predict import Predictor
from predict import Predictor_KNN
from pf_predict import PfPredictor
import math

class Scorer:
	"""A class for generating scores for a predictor (vs. actual data)."""

	def __init__(self, pred):
		self.p=pred

	def error(self, initial_point=10, final_point=99999999):
		"""Calculate and return the average error per point from the initial point on.
		For each point, sum the error predicting the next 63 points.
		"""
		sum=0
		count=0
		for i in range(initial_point, final_point):
			inner_sum=0
			for j in range(0,64):
				if(self.p.test_set_lines[i+j][0]!=-1 and self.p.test_set_lines[i][0]!=-1):
					count+=1
					err=Scorer.squared_err(self.p.predict(i,i+j),self.p.test_set_lines[i+j])		
					print str(err)+"|",
					inner_sum+=err
				else:
					print "|",
			sum+=math.sqrt(inner_sum)
		if count==0:
			return 0
		return sum*64.0/(count)

	@staticmethod
	def squared_err(p1,p2):
		return (float(p1[0])-float(p2[0]))**2 + (float(p1[1])-float(p2[1]))**2


# Run the code below only if this module is being directly executed
if __name__ == "__main__":
	p_train=PfPredictor()
	p_train.read("training_video1-centroid_data")
	p_train.process()
	
	pf_pred=PfPredictor()
	pf_pred.read("testing_video-centroid_data")
	pf_pred.process(False)
	pf_pred.collision_database = p_train.collision_database
	p_knn=Predictor_KNN()
	p_knn.read("training_video1-centroid_data")
	p_knn.read_test_set("testing_video-centroid_data")
	print "Preprocessing complete"

	for i in range (300,1378):
		start_index = i
		pf_pred.learn(start_index)
		pf_pred.read_test_set("testing_video-centroid_data")
		s_pred=Scorer(pf_pred)
		print str(s_pred.error(i,i+1))+"|pf_pred"
		s_knn=Scorer(p_knn)
		print str(s_knn.error(i,i+1))+"|knn_pred"
