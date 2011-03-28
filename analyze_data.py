import os
import sys
from optparse import OptionParser

DEFAULT_DIRECTORY = "test_data"

def parse_cmdline(argv=None):
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory")
    parser.add_option("-e", "--errors", action="store_false", dest="errors")
    parser.add_option("-t", "--time", action="store_false", dest="time")
    parser.add_option("-1", "--firstonly", action="store_false", dest="first")
    (options, args) = parser.parse_args(argv[1:])
    directory = options.directory
    o_errors = options.errors
    o_time = options.time
    o_first = options.first
    if directory is None:
        return DEFAULT_DIRECTORY

    return (directory, o_errors, o_time, o_first)

def get_nprofiles_list(listdir):
    nprofs_list = []
    for directory in listdir[:]:
        nprofs = directory.split("-")
        try:
            nprofs_list.append(int(nprofs[0]))
        except:
            pass

    return sorted(set(nprofs_list))

def get_ncriteria_list(listdir, nprofs):
    ncrit_list = []
    for directory in listdir[:]:
        try:
            data = directory.split("-")
            if nprofs == int(data[0]):
                ncrit_list.append(int(data[1]))
        except:
            pass

    return sorted(set(ncrit_list))

def get_naref_list(listdir, nprofs, ncrit):
    narefs_list = []
    for directory in listdir[:]:
        try:
            data = directory.split("-")
            if nprofs == int(data[0]) and ncrit == int(data[1]):
                narefs_list.append(int(data[2]))
        except:
            pass

    return sorted(set(narefs_list))

def get_seed_list(listdir, nprofs, ncrit, narefs):
    seed_list = []
    for directory in listdir[:]:
        try:
            directory = directory.rstrip(".txt")
            data = directory.split("-")
            if nprofs == int(data[0]) and ncrit == int(data[1]) and narefs == int(data[2]):
                seed_list.append(data[3])
        except:
            pass

    return set(seed_list)

def get_seed_results(directory, nprofs, ncrit, narefs, seed_list):
    n = 0
    n2 = 0
    list_errors = []
    list_time = []
    list_errors2 = []
    list_time2 = []
    for seed in seed_list:
        f = open("%s/%d-%d-%d-%s.txt" % (directory, nprofs, ncrit, narefs, seed))
        i = 0
        for line in f:
            if i == 0:
                if line.find("Time used:") != -1:
                    time = float(line.lstrip("Time used:").rstrip("secs\n"))
                    list_time.append(time)
                if line.find("Assignment errors:") != -1:
                    errors = float(line.lstrip("Assignment errors:"))
                    list_errors.append(errors)
                if line.find("Output 2") != -1:
                    i = 1
            else:
                if line.find("Time used:") != -1:
                    time2 = float(line.lstrip("Time used:").rstrip("secs\n"))
                    list_time2.append(time2)
                if line.find("Assignment errors:") != -1:
                    errors2 = float(line.lstrip("Assignment errors:"))
                    list_errors2.append(errors2)
                    n2 = n2+1

    results = {}

    n = len(list_errors)
    if n > 0:
        m = round(sum(list_errors)/n,4)
        s = round(sum([(x-m)**2 for x in list_errors])/(n-1), 4)**0.5

        results["n"] = n
        results["avg_errors"] = m
        results["std_errors"] = s
        results["max_errors"] = round(max(list_errors), 4)
        results["min_errors"] = round(min(list_errors), 4)
        results["avg_time"] = round(sum(list_time)/n,4)
        results["std_time"] = round(sum([(x-results["avg_time"])**2 for x in list_time])/(n-1), 4)**0.5
        results["max_time"] = round(max(list_time),4)
        results["min_time"] = round(min(list_time),4)
    else:
        results["n"] = 0
        results["avg_errors"] = 0 
        results["std_errors"] = 0
        results["max_errors"] = 0
        results["min_errors"] = 0
        results["avg_time"] = 0
        results["std_time"] = 0
        results["max_time"] = 0
        results["min_time"] = 0

    n2 = len(list_errors2)
    if n2 > 0:
        m = round(sum(list_errors2)/n2,4)
        s = round(sum([(x-m)**2 for x in list_errors2])/(n2-1), 4)**0.5

        results["n2"] = n2 
        results["avg_errors2"] = m
        results["std_errors2"] = s
        results["max_errors2"] = round(max(list_errors2), 4)
        results["min_errors2"] = round(min(list_errors2), 4)
        results["avg_time2"] = round(sum(list_time2)/n, 4)
        results["std_time2"] = round(sum([(x-results["avg_time2"])**2 for x in list_time2])/(n2-1), 4)**0.5
        results["max_time2"] = round(max(list_time2),4)
        results["min_time2"] = round(min(list_time2),4)
    else:
        results["n2"] = -1
        results["avg_errors2"] = 0 
        results["std_errors2"] = 0
        results["max_errors2"] = 0
        results["min_errors2"] = 0
        results["avg_time2"] = 0
        results["std_time2"] = 0
        results["max_time2"] = 0
        results["min_time2"] = 0

    return results

def main(argv=None):
    if argv is None:
        argv = sys.argv

    (directory, o_errors, o_time, o_first) = parse_cmdline(argv)

    listdir = os.listdir(directory)
    nprofs_list = get_nprofiles_list(listdir)

    print "p\tc\tn\ti",
    if o_errors is not None:
        print "\te\testd\temin\temax",
    if o_time is not None:
        print "\tt\ttstd\ttmin\ttmax",

    if o_first is None:
        print "\ti2",
        if o_errors is not None:
            print "\te2\testd2\te2min\te2max",
        if o_time is not None:
            print "\tt2\ttstd2\ttmin2\ttmax2",

        if o_errors is not None:
            print "\ted",

    print ""

    for nprofs in nprofs_list:
        ncrit_list = get_ncriteria_list(listdir, nprofs)
        for ncrit in ncrit_list:
            narefs_list = get_naref_list(listdir, nprofs, ncrit) 
            for narefs in narefs_list:
                seed_list = get_seed_list(listdir, nprofs, ncrit, narefs)
                results = get_seed_results(directory, nprofs, ncrit, narefs, seed_list)
                print "%d\t%d\t%d\t%d" % (nprofs, ncrit, narefs, results["n"]),
                if o_errors is not None:
                    print "\t%5g\t%.2g\t%5g\t%5g" % (results["avg_errors"]*100, results["std_errors"]*100,
                        results["min_errors"]*100, results["max_errors"]*100),
                if o_time is not None:
                    print "\t%5g\t%.2g\t%5g\t%5g" % (results["avg_time"], results["std_time"],
                        results["min_time"], results["max_time"]),

                if o_first is None:
                    print "\t%d" % (results["n2"]),

                    if o_errors is not None:
                        print "\t%5g\t%.2g\t%5g\t%5g" % (results["avg_errors2"]*100, results["std_errors2"]*100,
                            results["min_errors2"]*100, results["max_errors2"]*100),
                    if o_time is not None:
                        print "\t%5g\t%.2g\t%5g\t%5g" % (results["avg_time2"], results["std_time2"],
                            results["min_time2"], results["max_time2"]),

                    if o_errors is not None:
                        print "\t%5g" % ((results["avg_errors2"]-results["avg_errors"])*100),

                print ""

if __name__ == "__main__":
    sys.exit(main())
