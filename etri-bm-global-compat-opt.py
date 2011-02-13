import sys
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

def parse_cmdline(argv=None):
    parser = OptionParser()
    parser.add_option("-a", "--nalternatives", dest="nalternatives")
    parser.add_option("-c", "--ncriteria", dest="ncriteria")
    parser.add_option("-p", "--nprofiles", dest="nprofiles")
    parser.add_option("-r", "--nlearning", dest="nlearning")
    parser.add_option("-s", "--seed", dest="seed")
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

    return (nalternatives, ncriteria, nprofiles, nlearning, seed)

def remove_incompatible_alts(pt, icompat):
    pt_adapted = pt.copy()
    for alt, compat in pt.iteritems():
        if compat == 0:
            del pt_adapted[alt]

    return pt_adapted

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # Parse command line
    (nalternatives, ncriteria, nprofiles, nlearning, seed) = parse_cmdline(argv)
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

    # Infer ELECTRE Tri parameters with max compat program
    (iweights, iprofiles, ilbda, icompat, info) = etri_infer_parameters(nlearning, criteria, pt, affectations, nprofiles, "models/etri_bm_global_compat.mod")

    # Apply ELECTRE Tri model with infered parameters 
    modeli = etri.electre_tri(pt, iprofiles, iweights, ilbda) 
    iaffectations = modeli.pessimist()

    # Print result
    print "Output 1"
    print "========"
    print "Time used:", info[0]
    print "Memory used:", info[1]
    debug.print_lambda(lbda, ilbda)
    debug.print_weights(weights, criteria, iweights)
    debug.print_profiles(profiles, criteria, iprofiles)
    debug.print_performance_table_with_assignements(pt, alternatives, criteria, affectations, iaffectations, icompat)

    # Infer ELECTRE Tri parameters to optimize parameters
    pt_adapted = remove_incompatible_alts(pt, icompat)
    (iweights, iprofiles, ilbda, icompat, info) = etri_infer_parameters(nlearning, criteria, pt_adapted, affectations, nprofiles, "models/etri_bm_global_opt.mod")

    # Apply ELECTRE Tri model with infered parameters 
    modeli = etri.electre_tri(pt, iprofiles, iweights, ilbda) 
    iaffectations = modeli.pessimist()

    print "Output 2"
    print "========"
    print "Time used:", info[0]
    print "Memory used:", info[1]
    debug.print_lambda(lbda, ilbda)
    debug.print_weights(weights, criteria, iweights)
    debug.print_profiles(profiles, criteria, iprofiles)
    debug.print_performance_table_with_assignements(pt, alternatives, criteria, affectations, iaffectations, icompat)

if __name__ == "__main__":
    sys.exit(main())
