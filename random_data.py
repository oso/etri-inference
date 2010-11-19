import random

def set_seed(seed=123456789):
    random.seed(seed)

def generate_random_pt(alternatives, criteria):
	pt = {}
	for i in alternatives: 
		p = {}
		for j in criteria:
			p[j] = random.random()
		pt[i] = p
	return pt

def generate_random_weights(criteria):
	weights = {}
	for i in criteria:
		weights[i] = random.random()
	return weights

def generate_random_profiles(nprofiles, criteria):
	profiles = []
	for i in range(nprofiles):
		profiles.append({"q" : {}, "p": {}, "v": {}, "refs": {}})
	for i in criteria:
		rnd = []
		for j in range(nprofiles):
			rnd.append(random.random())
		rnd.sort()
		for j in range(nprofiles):
			profiles[j]["refs"][i] = rnd[j]
			profiles[j]["q"][i] = 0
			profiles[j]["p"][i] = 0
	return profiles
