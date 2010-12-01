#!/bin/sh

OUTPUT_DIR=test_data

SEED[0]=123
SEED[1]=456
SEED[2]=789
SEED[3]=012
SEED[4]=345
SEED[5]=678
SEED[6]=901
SEED[7]=234
SEED[8]=567
SEED[9]=890

AREF_MAX=150
AREF_STEP=10

NCRIT_MIN=3
NCRIT_MAX=6

NPROF_MIN=1
NPROF_MAX=4

for nprof in $(seq $NPROF_MIN $NPROF_MAX); do
	for i in $(seq 1 $((150/10))); do
		r=$((i*10))
		for seed in ${SEED[*]}; do
			for ncrit in $(seq $NCRIT_MIN $NCRIT_MAX); do
				echo "Nprof: $nprof - Naref: $r - Seed: $seed - Ncrit: $ncrit"
				python test_etri.py -s $seed -a 10000 -c $ncrit -p $nprof -r $r >$OUTPUT_DIR/$nprof-$r-$seed-$ncrit.txt
			done
		done
	done
done
