import sys
import random
import random_data
import debug
import glpk
import etri
from etri_utils import *
from optparse import OptionParser

default_seed = 1
default_nalternatives = 1000
default_ncriteria = 5
default_nprofiles = 1
default_nlearning = 100
default_error = 0

def parse_cmdline(argv=None):
    parser = OptionParser()
    parser.add_option("-a", "--nalternatives", dest="nalternatives")
    parser.add_option("-c", "--ncriteria", dest="ncriteria")
    parser.add_option("-p", "--nprofiles", dest="nprofiles")
    parser.add_option("-r", "--nlearning", dest="nlearning")
    parser.add_option("-s", "--seed", dest="seed")
    parser.add_option("-e", "--error", dest="error")
    (options, args) = parser.parse_args(argv[1:])
    nalternatives = int(options.nalternatives)
    if not nalternatives:
        nalternatives = default_nalternatives
    ncriteria = int(options.ncriteria)
    if not ncriteria:
        ncriteria = default_ncriteria
    nprofiles = int(options.nprofiles)
    if not nprofiles:
        nprofiles = default_nprofiles
    nlearning = int(options.nlearning)
    if not nlearning:
        nlearning = default_nlearning
    seed = int(options.seed)
    if not seed:
        seed = default_seed
    error = int(options.error)
    if not error:
        error = default_error

    return (nalternatives, ncriteria, nprofiles, nlearning, seed, error)

def add_errors_in_learning_alts(affectations, nlearning, nprofiles, errors):
    learning_alts = [ "a%d" % (i+1) for i in range(nlearning) ]
    ncat = nprofiles
    for alt in learning_alts:
        if errors == 0:
            break

        old =  affectations[alt]
        new = old
        while old == new:
            new = ((old+random.randint(1, 10)) % (nprofiles+1))+1
        print "alt", alt
        print "old", old
        print "new", new
        affectations[alt] = new
        errors = errors - 1

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # Parse command line
    (nalternatives, ncriteria, nprofiles, nlearning, seed, error) = parse_cmdline(argv)
    print "Input parameters"
    print "================"
    print "Nalternatives:", nalternatives
    print "Ncriteria:", ncriteria
    print "Nprofiles:", nprofiles
    print "Nlearning:", nlearning
    print "Seed:", seed

    # Create a model
    (alternatives, criteria, palternatives) = create_model(nalternatives, ncriteria, nprofiles)
    (pt, profiles, weights, lbda) = generate_random_data(seed, alternatives, criteria, palternatives)
    model = etri.electre_tri(pt, profiles, weights, lbda) 
    affectations = model.pessimist() 

    # Add errors in learning alternatives
    add_errors_in_learning_alts(affectations, nlearning, nprofiles, error)

    # Infer ELECTRE Tri parameters
    (iweights, iprofiles, ilbda, icompat, info) = etri_infer_parameters(nlearning, criteria, pt, affectations, nprofiles, "models/etri_bm_global_compat.mod")

    # Apply ELECTRE Tri model with infered parameters 
    modeli = etri.electre_tri(pt, iprofiles, iweights, ilbda) 
    iaffectations = modeli.pessimist()

    # Print result
    print "Output"
    print "======"
    print "Time used:", info[0]
    print "Memory used:", info[1]
    debug.print_lambda(lbda, ilbda)
    debug.print_weights(weights, criteria, iweights)
    debug.print_profiles(profiles, criteria, iprofiles)
    debug.print_performance_table_with_assignements(pt, alternatives, criteria, affectations, iaffectations, icompat)

if __name__ == "__main__":
    sys.exit(main())
