import random

seed = '123456789'
random.seed(seed)

def print_performance_table(pt, alternatives, criteria):
    print "Performance table:"
    str = "ai/gj"
    for crit in criteria:
        str += "\t%s" % crit
    print str
    for alt in alternatives:
        str = "%s" % alt
        for crit in criteria:
            str += "\t%.3g" % round(pt[alt][crit],3)
        print str

def print_performance_table_with_assignements(pt, alternatives, criteria, assign, assign2=None, compat=None):
    print "Performance table and assignment:" 
    str = "ai/gj"
    for crit in criteria:
        str += "\t%s" % crit
    str += "\t|\tAssign"
    if assign2 <> None:
        str += "\tAssign2"
    if compat <> None:
        str += "\tCompat"
    print str
    assign_errors = 0
    rounding_errors = 0
    compatible = len(alternatives)
    for alt in alternatives:
        str = "%s" % alt
        for crit in criteria:
            str += "\t%.3g" % round(pt[alt][crit],3)
        str += "\t|\t%d" % assign[alt]
        if assign2 <> None:
            str += "\t%d" % assign2[alt]
        if compat <> None:
            if compat.has_key(alt):
                str += "\t%d" % compat[alt]
                if compat == 0:
                    compatible = compatible - 1
            else:
                str += "\t-"
        if assign2 <> None:
            if assign[alt] <> assign2[alt]:
                str += "!"
                assign_errors += 1
                if compat == 1:
                    rounding_errors += 1
            if compat == 0 and assign[alt] == assign2[alt]:
                str += "!!"
        print str

    print "Compatible alternatives:", float(compatible)/len(alternatives)
    print "Assignment errors:", float(assign_errors)/float(len(alternatives))
    print "Aref rounding errors:", rounding_errors

def print_profiles(profiles, criteria, iprofiles=None):
    print "Profiles:"
    str = "bi/gj"
    for crit in criteria:
        str += "\t%s" % crit
    print str
    for i, profile in enumerate(profiles):
        str = "b%d" % (i+1)
        str2 = "    q"
        str3 = "    p"
        str4 = "    v"
        for crit in criteria:
            str += "\t%.3g" % round(profile["refs"][crit],3)
#            str2 += "\t%.3g" % profile["q"][crit]
#            str3 += "\t%.3g" % profile["p"][crit]
#            if profile["v"].has_key(crit):
#                str4 += "\t%.3g" % profile["v"][crit]
#            else:
#                str4 += "\t"
        print str
#        print str2
#        print str3
#        print str4

    if iprofiles == None:
        return

    for i, profile in enumerate(iprofiles):
        str = "ib%d" % (i+1)
        str2 = "    q"
        str3 = "    p"
        str4 = "    v"
        for crit in criteria:
            str += "\t%.3g" % round(profile["refs"][crit],3)
#            str2 += "\t%.3g" % profile["q"][crit]
#            str3 += "\t%.3g" % profile["p"][crit]
#            if profile["v"].has_key(crit):
#                str4 += "\t%.3g" % profile["v"][crit]
#            else:
#                str4 += "\t"
        print str
#        print str2
#        print str3
#        print str4

def print_weights(weights, criteria, iweights=None):
    print "Criteria weights:"
    str = "w/gj"
    sum_weights = sum(weights.values())
    for crit in criteria:
        str += "\t%s" % crit
    print str
    str = "w"
    for crit in criteria:
        str += "\t%.3g" % (weights[crit]/sum_weights)
        #str += "\t%.3g" % round((weights[crit]/sum_weights),3)
    print str
    if iweights <> None:
        sum_iweights = sum(iweights.values())
        str = "wi"
        for crit in criteria:
            str += "\t%.3g" % (iweights[crit]/sum_iweights)
            #str += "\t%.3g" % round((iweights[crit]/sum_iweights),3)
        print str

def print_lambda(lbda, ilbda=None):
    print "Lambda: %g" % lbda
    if ilbda <> None:
        print "iLambda: %g" % ilbda
