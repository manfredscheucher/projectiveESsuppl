This repository contains supplemental material to the article 
"Erdős--Szekeres-type problems in the real projective plane"
by Martin Balko, Manfred Scheucher, and Pavel Valtr
see http://arxiv.org/abs/2203.07518



# Setup 

We provide a python script `projective_ES.py` that can generate a CNF for a particular question.
One can install the interface [pysat](https://pysathq.github.io/installation/) to the solver cadical and solve the CNF directly from python via the parameter `--solver cadical`. Alternatively one can export the CNF in DIMACS form via `-o file` and run a solver like [cadical](https://github.com/arminbiere/cadical) or [gimsatul](https://github.com/arminbiere/gimsatul) manually on that instance.



# SAT framework

We extended the SAT framework from "Two Disjoint 5-Holes in Point Sets" (http://arxiv.org/abs/1807.10848)
so that it can operate on projective k-gons and projective k-holes.


## projective 6-gons
`n8_no_p6g.json` encodes a set of 8 points with no projective 6-gon. 
To verify that every set of 9 points yields a projective 6-gon,
run
```
python projective_ES.py 9 6 0 --solver cadical
```
The computations take less than one CPU second.


## projective 6-holes
`n15_no_p6h.json` encodes a set of 15 points with no projective 6-hole.
To verify that every set of 16 points yields a projective 6-hole,
run
```
python projective_ES.py 16 6 1 --solver cadical
```
The computations take about 5 CPU minutes.


## projective 7-gons
`n17_no_p7g.json` encodes a set of 17 points with no projective 7-gon. 
To verify that every set of 19 points yields a projective 7-gon,
run
```
python projective_ES.py 19 7 0 --solver cadical 
```
The computations take about 1 CPU month. 
This can be speed-up almost linearly 
by exporting an incremental CNF 
and then cadical in running parallel using cubes.
However, the procedure gets more complex. 
For more information, please contact the author.

In order to verify that every set of 18 points yields a projective 7-gon, 
the computation is much more involved.
The outline is as following:
First we ran
```
python projective_ES.py 18 7 0 --solver cadical --all --solutions2file sol18_7_0.txt
```
to enumerate all chirotopes which do not yield a 18-gon.
We then used an implementation 
of the method of biquadratic final polynomials 
to show that all found chirotopes are actually non-realizable as pointsets.
This concludes that 18 points yields a projective 7-gon.
We are currently enhancing the usability of our non-realizability framework
and look forward to make it publicly available in the future/in a subsequent article.
For more information, please contact the author.