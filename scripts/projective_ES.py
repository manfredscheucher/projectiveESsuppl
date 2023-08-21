#!/usr/bin/python3
"""
	Supplemental program to investigate projective gons and holes
	(c) 2023 Manfred Scheucher <scheucher@math.tu-berlin.de>
"""

from itertools import *
from sys import *

import datetime

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("n",type=int,help="number of points")
parser.add_argument("k",type=int,help="forbid projective gons/holes of specified size")
parser.add_argument("empty",type=int,help="0=gon;1=hole")

parser.add_argument("--symmetrybreaking",action='store_false',help="by default break symmetries, use flag to disable")

parser.add_argument("-a","--all",action='store_true', help="enumerate all configurations")
parser.add_argument("-o","--output", help="if specified, export CNF to this file")
parser.add_argument("-i","--inccnf", help="export inccnf for cubing")

parser.add_argument("--solver", choices=['cadical', 'pycosat'], help="SAT solver")

args = parser.parse_args()
print("args",args)


time_start = datetime.datetime.now()

n = args.n 
k = args.k 
empty = args.empty

if not args.solver and not args.output:
	print("please specify whether you want to solve or output the instance")
	exit()


N = range(n)

all_variables = []

#all_variables += [('chi',I) for I in combinations(N,3)] # lex order
all_variables += [('chi',I[::-1]) for I in combinations(N[::-1],3)][::-1] # revlex order

all_variables += [('triangle_contains',(a,b,c,p)) for a,b,c,p in permutations(N,4)] # triangle abc contains p (abp=bcp=cap=+)
all_variables += [('sector_contains'  ,(a,b,c,p)) for a,b,c,p in permutations(N,4)] # sector of abc contains p (bap=bcp=cap=+)

all_variables_index = {}

num_vars = 0
for v in all_variables:
	all_variables_index[v] = num_vars
	num_vars += 1

def var(L):	
	return 1+all_variables_index[L]

chi_cache = {}
def var_chi(*L): 
	if L not in chi_cache:
		LS = tuple(sorted(L))
		inversions = len([(i,j) for (i,j) in combinations(L,2) if j>i])
		chi_cache[L] = var(('chi',LS)) * (-1)**inversions
	return chi_cache[L]

def var_triangle_contains(*L): 
	return var(('triangle_contains',L))

def var_sector_contains(*L): 
	return var(('sector_contains',L)) 


constraints = []

print ("(*) signotope axioms",len(constraints))
# forbid invalid configuartions in the signature
for I4 in combinations(N,4):
	I4_triples = list(combinations(I4,3))
	for t1,t2,t3 in combinations(I4_triples,3): 
		# for any three lexicographical ordered triples t1 < t2 < t3
		# the signature must not be "+-+" or "-+-"
		for sgn in [-1,+1]:
			constraints.append([sgn*var_chi(*t1),-sgn*var_chi(*t2),sgn*var_chi(*t3)])


if args.symmetrybreaking:
	print("(3) wlog: 0,...,r-3 lie on the boundary of convex hull and others are sorted around (to break symmetries)",len(constraints))
	for i,j in combinations(range(1,n),2):
		constraints.append([var_chi(0,i,j)])


print("(*) assert containment",len(constraints))
for a,b,c,p in permutations(N,4):
	constraints.append([-var_triangle_contains(a,b,c,p),+var_chi(a,b,p)])
	constraints.append([-var_triangle_contains(a,b,c,p),+var_chi(b,c,p)])
	constraints.append([-var_triangle_contains(a,b,c,p),+var_chi(c,a,p)])
	constraints.append([+var_triangle_contains(a,b,c,p),-var_chi(a,b,p),-var_chi(b,c,p),-var_chi(c,a,p)])

	constraints.append([-var_sector_contains(a,b,c,p),-var_chi(a,b,p)])
	constraints.append([-var_sector_contains(a,b,c,p),+var_chi(b,c,p)])
	constraints.append([-var_sector_contains(a,b,c,p),+var_chi(c,a,p)])
	constraints.append([+var_sector_contains(a,b,c,p),+var_chi(a,b,p),-var_chi(b,c,p),-var_chi(c,a,p)])



if args.empty:
	print(f"(*) no {k}-hole",len(constraints))
else:
	print(f"(*) no {k}-gons",len(constraints))

for t in range(k):
	for A in combinations(N,t):
		for B in combinations(set(N)-set(A),k-t):
			if A and B and A[0]>B[0]: continue # symmetry 
			clause = []
			potential_inner = set(N) if args.empty else set(A+B)
			for X,Y in permutations([A,B]):
				for I in combinations(X,3):
					clause += [var_triangle_contains(*I,p) for p in potential_inner-set(I)] # affine inclusion
				for (x1,x2),y in product(permutations(X,2),Y):
					clause += [var_sector_contains(x1,x2,y,p) for p in potential_inner-{x1,x2,y}] # projective inclusion
			constraints.append(clause)


print("Total number of constraints:",len(constraints))
time_before_solving = datetime.datetime.now()
print("creating time:",time_before_solving-time_start)


if args.output:
	print ("write cnf instance to file:",args.output)
	with open(args.output,"w") as f:
		#f.write("p inccnf\n")
		if args.inccnf:
			f.write("p inccnf\n")
		else:
			f.write("p cnf "+str(num_vars)+" "+str(len(constraints))+"\n")
		for c in constraints:
			f.write(" ".join(str(x) for x in c)+" 0\n")

if args.solver:
	if args.solver == "cadical":
		print ("use pysat/Cadical")
		from pysat.solvers import Cadical153	
		solver = Cadical153()
		for c in constraints: solver.add_clause(c)
		solution_iterator = solver.enum_models()
	else:
		print ("use pycosat")
		import pycosat
		solution_iterator = pycosat.itersolve(constraints)

	print (datetime.datetime.now(),"start solving")

	ct = 0
	for sol in solution_iterator:
		ct += 1
		sol = set(sol)
		s = ''.join('+' if var_chi(*I) in sol else "-" for I in combinations(N,3))
		print("solution #",ct,s)
		if not args.all: break

	print("number of solutions:",ct)

	time_end = datetime.datetime.now()

	if ct == 0:
	    print (time_end,"no solution!?")
	else:
	    if args.all:
	        print (time_end,"total count:",ct)
	    else:
	        print("use parameter -a/--all to enumerate all solutions")

	print("solving time :",time_end-time_before_solving)
	print("total time   :",time_end-time_start)

