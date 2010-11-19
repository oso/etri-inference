import sys
import random_data
import debug
import glpk
import etri

nalternatives = 1000
ncriteria = 5
nprofiles = 1
lbda = 0.75
nalt_ref = 100

# Generate random data
random_data.set_seed('123456789')

alternatives = [ "a%d" % (i+1) for i in range(nalternatives) ]
criteria = [ "g%d" % (i+1) for i in range(ncriteria) ]
profiles = [ "b%d" % (i+1) for i in range(nprofiles) ]

pt = random_data.generate_random_pt(alternatives, criteria)
#debug.print_performance_table(pt, alternatives, criteria)

#profiles = random_data.generate_random_profiles(nprofiles, criteria)
profiles= []
for i in range(nprofiles):
    refs = {}
    p = {}
    q = {}
    for crit in criteria:
        refs[crit] = 0.5
        q[crit] = 0
        p[crit] = 0
    profiles.append({'refs': refs, 'p': p, 'q': q, 'v': {}})
#debug.print_profiles(profiles, criteria)

#weights = random_data.generate_random_weights(criteria)
weights = {'g1': 0.1, 'g2': 0.2, 'g3': 0.4, 'g4': 0.5, 'g5': 0.6}
#weights = {}
#for i, crit in enumerate(criteria):
#    weights[crit] = 0.2

#debug.print_weights(weights, criteria)

# Apply ELECTRE TRI method
model = etri.electre_tri(pt, profiles, weights, lbda) 
pessimist = model.pessimist()
optimist = model.optimist()

#debug.print_performance_table_with_assignements(pt, alternatives, criteria, pessimist)

# Infer ELECTRE TRI parameter
learning_alts = [ "a%d" % (i+1) for i in range(nalt_ref) ]

categories = [ (i+1) for i in range(nprofiles+1) ]
categories_rank = {}
for i, cat in enumerate(categories):
    categories_rank[cat] = i+1

infile = glpk.create_input_file(learning_alts, criteria, pt, categories, categories_rank, pessimist) 

(status, output) = glpk.solve(infile.name)
infile.close()

if status:
    sys.exit("gklp returned status %d" % status)

(iweights, iprofiles, ilbda, icompat) = glpk.parse_output(output, learning_alts, criteria)
if iweights == None:
    sys.exit("Invalid weights");
if iprofiles == None:
    sys.exit("Invalid profiles")
if ilbda == None:
    sys.exit("Invalid lambda")
if icompat == None:
    sys.exit("Invalid compat");

# Apply ELECTRE TRI model
modeli = etri.electre_tri(pt, iprofiles, iweights, ilbda) 
ipessimist = model.pessimist()

debug.print_lambda(lbda, ilbda)
debug.print_weights(weights, criteria, iweights)
debug.print_profiles(profiles, criteria, iprofiles)
debug.print_performance_table_with_assignements(pt, alternatives, criteria, pessimist, ipessimist, icompat)
