#!/bin/sh

INPUT_DIRECTORY=test_data

cd $INPUT_DIRECTORY
#ls $INPUT_DIRECTORY/2-3-* | sort -k3 -t\- -n
#ls 2-3-* | cut -d1 

NPROFILES=$(ls *-* | cut -f1 -d\- | uniq | sort -n)

for nprof in $NPROFILES; do
	NCRITERIA=$(ls $nprof-* | cut -f2 -d\- | uniq | sort -n)
	for ncriteria in $NCRITERIA; do
		NAREFS=$(ls $nprof-$ncriteria-* | cut -f3 -d\- | uniq | sort -n)
		for narefs in $NAREFS; do
			SEEDS=$(ls $nprof-$ncriteria-$narefs-* | cut -f4 -d\- | cut -f1 -d.)
			for seed in $SEEDS; do
				filename="$nprof-$ncriteria-$narefs-$seed.txt"
				echo "$filename $(grep "Assignment errors" $filename)"
			done
		done
	done
done
