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
    ncat = len(palternatives)+1
    step = float(1)/ncat
    for i in palternatives:
        profiles.append({"q" : {}, "p": {}, "v": {}, "refs": {}})
    for i, palt in enumerate(palternatives):
        for j in criteria:
            if i > 0:
                lower = max((float(i+1)/ncat-step),profiles[i-1]["refs"][j])
            else:
                lower = float(i+1)/ncat - step 
            upper = float(i+1)/ncat + step 
            rnd = random.uniform(lower, upper)
            profiles[i]["refs"][j] = rnd
            profiles[i]["q"][j] = 0
            profiles[i]["p"][j] = 0

    return profiles

def generate_random_lambda():
    return round(random.uniform(0.5,1),ROUND)
