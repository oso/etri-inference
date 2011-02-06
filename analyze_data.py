import os
import sys
from optparse import OptionParser

DEFAULT_DIRECTORY = "test_data"

def parse_cmdline(argv=None):
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory")
    (options, args) = parser.parse_args(argv[1:])
    directory = options.directory
    if directory is None:
        return DEFAULT_DIRECTORY

    return directory

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
    sum_errors = 0
    sum_time = 0
    for seed in seed_list:
        f = open("%s/%d-%d-%d-%s.txt" % (directory, nprofs, ncrit, narefs, seed))
        for line in f:
            if line.find("Assignment errors:") != -1:
                errors = float(line.lstrip("Assignment errors:"))
                sum_errors += errors
            if line.find("Time used:") != -1:
                time = float(line.lstrip("Time used:").rstrip("secs\n"))
                sum_time += time
        n = n+1

    return (round(sum_errors/n,4), round(sum_time/n, 3))

def main(argv=None):
    if argv is None:
        argv = sys.argv

    directory = parse_cmdline(argv)

    listdir = os.listdir(directory)
    nprofs_list = get_nprofiles_list(listdir)

    print "p\tc\tn\te\tt"
    for nprofs in nprofs_list:
        ncrit_list = get_ncriteria_list(listdir, nprofs)
        for ncrit in ncrit_list:
            narefs_list = get_naref_list(listdir, nprofs, ncrit) 
            for narefs in narefs_list:
                seed_list = get_seed_list(listdir, nprofs, ncrit, narefs)
                (errors, time) = get_seed_results(directory, nprofs, ncrit, narefs, seed_list)
                print "%d\t%d\t%d\t%5g\t%5g" % (nprofs, ncrit, narefs, errors, time)

if __name__ == "__main__":
    sys.exit(main())
