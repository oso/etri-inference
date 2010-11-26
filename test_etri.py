import sys
import random_data
import debug
import glpk
import etri
from optparse import OptionParser

default_seed = 1
default_nalternatives = 1000
default_ncriteria = 5
default_nprofiles = 1
default_lbda = 0.75
default_nlearning = 100

def create_model(nalternatives, ncriteria, nprofiles):
    alternatives = [ "a%d" % (i+1) for i in range(nalternatives) ]
    criteria = [ "g%d" % (i+1) for i in range(ncriteria) ]
    palternatives = [ "b%d" % (i+1) for i in range(nprofiles) ]
    return (alternatives, criteria, palternatives)

def generate_random_data(seed, alternatives, criteria, palternatives):
    random_data.set_seed(seed)
    pt = random_data.generate_random_pt(alternatives, criteria)
    profiles = random_data.generate_random_profiles(palternatives, criteria)
    weights = random_data.generate_random_weights(criteria)
    lbda = random_data.generate_random_lambda() 
    return (pt, profiles, weights, lbda)

def etri_infer_parameters(nlearning, criteria, pt, affectations, nprofiles):
    learning_alts = [ "a%d" % (i+1) for i in range(nlearning) ]
    categories = [ (i+1) for i in range(nprofiles+1) ]
    categories_rank = {}
    for i, cat in enumerate(categories):
        categories_rank[cat] = i+1
    infile = glpk.create_input_file(learning_alts, criteria, pt, categories, categories_rank, affectations) 
    (status, output) = glpk.solve(infile.name)
    if status:
        sys.exit("gklp returned status %d" % status)
    infile.close()
    return glpk.parse_output(output, learning_alts, criteria)

def parse_cmdline(argv=None):
    parser = OptionParser()
    parser.add_option("-a", "--nalternatives", dest="nalternatives")
    parser.add_option("-c", "--ncriteria", dest="ncriteria")
    parser.add_option("-p", "--nprofiles", dest="nprofiles")
    parser.add_option("-r", "--nlearning", dest="nlearning")
    parser.add_option("-l", "--lambda", dest="lbda")
    parser.add_option("-s", "--seed", dest="seed")
    (options, args) = parser.parse_args(argv[1:])
    nalternatives = options.nalternatives
    if not nalternatives:
        nalternatives = default_nalternatives
    ncriteria = options.ncriteria
    if not ncriteria:
        ncriteria = default_ncriteria
    nprofiles = options.nprofiles
    if not nprofiles:
        nprofiles = default_nprofiles
    nlearning = options.nlearning
    if not nlearning:
        nlearning = default_nlearning
    lbda = options.lbda
    if not lbda:
        lbda = default_lbda
    seed = options.seed
    if not seed:
        seed = default_seed

    return (nalternatives, ncriteria, nprofiles, nlearning, lbda, seed)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # Parse command line
    (nalternatives, ncriteria, nprofiles, nlearning, lbda, seed) = parse_cmdline(argv)

    # Create a model
    (alternatives, criteria, palternatives) = create_model(nalternatives, ncriteria, nprofiles)
    (pt, profiles, weights, lbda) = generate_random_data(seed, alternatives, criteria, palternatives)
    model = etri.electre_tri(pt, profiles, weights, lbda) 
    affectations = model.pessimist() 

    # Infer ELECTRE Tri parameters
    (iweights, iprofiles, ilbda, icompat) = etri_infer_parameters(nlearning, criteria, pt, affectations, nprofiles)

    # Apply ELECTRE Tri model with infered parameters 
    modeli = etri.electre_tri(pt, iprofiles, iweights, ilbda) 
    iaffectations = modeli.pessimist()

    # Print result
    debug.print_lambda(lbda, ilbda)
    debug.print_weights(weights, criteria, iweights)
    debug.print_profiles(profiles, criteria, iprofiles)
    debug.print_performance_table_with_assignements(pt, alternatives, criteria, affectations, iaffectations, icompat)

if __name__ == "__main__":
    sys.exit(main())
