#!/bin/sh

OUTPUT_DIR=data_compat_opt_10

AREF_MIN=10
AREF_MAX=100

NCRIT_MIN=2
NCRIT_MAX=5

NPROF_MIN=3
NPROF_MAX=3

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

for nprof in $(seq $NPROF_MIN $NPROF_MAX); do
	for ncrit in $(seq $NCRIT_MIN $NCRIT_MAX); do
		for i in $(seq $(($AREF_MIN/10)) $(($AREF_MAX/10))); do
			r=$((i*10))
			for seed in ${SEED[*]}; do
				if [ ! -f "$OUTPUT_DIR/$nprof-$ncrit-$r-$seed.txt" ]; then
					echo "Nprof: $nprof - Ncrit: $ncrit - Naref: $r - Seed: $seed"
					tmpfile=$(mktemp)

					python etri-bm-global-opt.py -s $seed -a 10000 -c $ncrit -p $nprof -r $r >$tmpfile
					mv $tmpfile $OUTPUT_DIR/$nprof-$ncrit-$r-$seed.txt
				fi
			done
		done
	done
done
