import sys
import random_data
import debug
import glpk

def create_model(nalternatives, ncriteria, nprofiles):
    alternatives = [ "a%d" % (i+1) for i in range(nalternatives) ]
    criteria = [ "g%d" % (i+1) for i in range(ncriteria) ]
    palternatives = [ "b%d" % (i+1) for i in range(nprofiles) ]
    return (alternatives, criteria, palternatives)

def generate_random_data(seed, alternatives, criteria, palternatives):
    random_data.set_seed(seed)
    profiles = random_data.generate_random_profiles(palternatives, criteria)
    weights = random_data.generate_random_weights(criteria)
    lbda = random_data.generate_random_lambda() 
    pt = random_data.generate_random_pt(alternatives, criteria)
    return (pt, profiles, weights, lbda)

def etri_infer_parameters(learning_alts, criteria, pt, affectations, nprofiles, model):
    categories = [ (i+1) for i in range(nprofiles+1) ]
    categories_rank = {}
    for i, cat in enumerate(categories):
        categories_rank[cat] = i+1
    infile = glpk.create_input_file(learning_alts, criteria, pt, categories, categories_rank, affectations) 
    print "GLPK file:", infile.name
    (status, output) = glpk.solve(infile.name, model)
    if status:
        sys.exit("gklp returned status %d" % status)
    infile.close()
    return glpk.parse_output(output, learning_alts, criteria)
