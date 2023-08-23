This repository contains supplemental material to the article 
"Erdős--Szekeres-type problems in the real projective plane"
by Martin Balko, Manfred Scheucher, and Pavel Valtr
see http://arxiv.org/abs/2203.07518



# SAT framework

We extended the SAT framework from "Two Disjoint 5-Holes in Point Sets" (http://arxiv.org/abs/1807.10848)
so that it can operate on projective k-gons and projective k-holes.


## projective 6-gons
`n8_no_p6g.json` encodes a set of 8 points with no projective 6-gon. 
To verify that every set of 9 points yields a projective 6-gon,
run
```
python scripts/projective_ES.py 9 6 0 --solver cadical
```
The computations take less than one CPU second.


## projective 6-holes
`n15_no_p6h.json` encodes a set of 15 points with no projective 6-hole.
To verify that every set of 16 points yields a projective 6-hole,
run
```
python scripts/projective_ES.py 16 6 1 --solver cadical
```
The computations take about 10 CPU minutes.


## projective 7-gons
`n17_no_p7g.json` encodes a set of 17 points with no projective 7-gon. 
To verify that every set of X points yields a projective 7-gon,
run
```
python scripts/projective_ES.py 18 7 0 --solver cadical
```
The computations take about X CPU minutes.

!!TODO!!
