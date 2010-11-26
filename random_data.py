import random

ROUND = 4

def set_seed(seed):
    random.seed(seed)

def generate_random_pt(alternatives, criteria):
	pt = {}
	for i in alternatives: 
		p = {}
		for j in criteria:
			p[j] = round(random.random(),ROUND)
		pt[i] = p
	return pt

def generate_random_weights(criteria):
	weights = {}
	for i in criteria:
		weights[i] = round(random.random(),ROUND)
	return weights

def generate_random_profiles(palternatives, criteria):
	profiles = []
	for i in palternatives:
		profiles.append({"q" : {}, "p": {}, "v": {}, "refs": {}})
	for i in criteria:
		rnd = []
		for j in palternatives:
			rnd.append(round(random.random(),ROUND))
		rnd.sort()
		for j, palt in enumerate(palternatives):
			profiles[j]["refs"][i] = rnd[j]
			profiles[j]["q"][i] = 0
			profiles[j]["p"][i] = 0
	return profiles

def generate_random_lambda():
    return round(random.uniform(0.5,1),ROUND)
