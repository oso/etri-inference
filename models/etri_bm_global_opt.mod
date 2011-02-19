/* Global inference of ELECTRE TRI Bouyssou-Marchant model parameters */

/* Parameters */
param ncat, integer, >= 2; /* number of categories */ 
param nalt, integer, > 0; /* number of alternatives */
param ncrit, integer, > 0; /* number of criteria */

set ALTS := 1..nalt; /* set of alternatives */
set CRIT := 1..ncrit; /* set of criteria */

param perfs{i in ALTS, j in CRIT};
param assign{ALTS};

/* Variables */
var epsilon = 10e-5;
var lambda  >= 0.5;
var c_sup{ALTS,CRIT}  >= 0;
var c_inf{ALTS,CRIT}  >= 0;
var weight{CRIT}  >= 0;
var d_sup{ALTS,CRIT}, binary;
var d_inf{ALTS,CRIT}, binary;
var gb{0..ncat,CRIT}  >= 0;
var x{ALTS};
var y{ALTS};
var alpha;

/* Objective */
maximize obj: alpha;

/* Constraints */
s.t. scinf{i in ALTS}:
	sum{j in CRIT} c_inf[i,j] = lambda + y[i];

s.t. scsup{i in ALTS}:
	sum{j in CRIT} c_sup[i,j] + x[i] = lambda;

s.t. alphax{i in ALTS}:
	alpha <= x[i];

s.t. alphay{i in ALTS}:
	alpha <= y[i];

s.t. cinf{i in ALTS, j in CRIT}:
	c_inf[i,j] <= weight[j];

s.t. csup{i in ALTS, j in CRIT}:
	c_sup[i,j] <= weight[j];

s.t. cinf2{i in ALTS, j in CRIT}:
	c_inf[i,j] <= d_inf[i,j];

s.t. csup2{i in ALTS, j in CRIT}:
	c_sup[i,j] <= d_sup[i,j];

s.t. cinf3{i in ALTS, j in CRIT}:
	c_inf[i,j] >= d_inf[i,j] - 1 + weight[j];

s.t. csup3{i in ALTS, j in CRIT}:
	c_sup[i,j] >= d_sup[i,j] - 1 + weight[j];

s.t. dinf{i in ALTS, j in CRIT}:
	d_inf[i,j] >= perfs[i,j] - gb[assign[i]-1,j] + epsilon;

s.t. dsup{i in ALTS, j in CRIT}:
	d_sup[i,j] >= perfs[i,j] - gb[assign[i],j] + epsilon;

s.t. dinf2{i in ALTS, j in CRIT}:
	d_inf[i,j] <= perfs[i,j] - gb[assign[i]-1,j] + 1;

s.t. dsup2{i in ALTS, j in CRIT}:
	d_sup[i,j] <= perfs[i,j] - gb[assign[i],j] + 1;

s.t. gblim{i in 1..ncat-1, j in CRIT}:
	gb[i,j] <= gb[i+1,j];

s.t. gbliminf{j in CRIT}:
	gb[0,j] = 0 + epsilon;

s.t. gblimsup{j in CRIT}:
	gb[ncat,j] = 1;

s.t. wmin{j in CRIT}:
	weight[j] <= 1;

wsum: sum{j in CRIT} weight[j] = 1;
lbdamin: lambda >= 0.5;
lbdamax: lambda <= 1;

solve;

printf "SOLUTION:\n";

printf "### Lambda ###\n";
printf lambda;
printf "\n### Lambda ###\n";

printf "### Profiles ###\n";
for {i in 1..ncat-1}
{
	for {j in CRIT}	
		printf "%g\t", gb[i,j];
	printf "\n";
}
printf "### Profiles ###\n";

printf "### Criteria weights ###\n";
for {j in CRIT}
	printf "%g\t", weight[j];
printf "\n### Criteria weights ###\n";

end;
