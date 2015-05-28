== Overview of mpb-plotting ==

Plot photonic dispersion curves with mode shapes (a frontend to MIT Photonic bands)

A set of Scheme/Python scripts that computes and plots the band structure of a 2-D photonic crystal and,
most importantly, draws also the modes corresponding to the band edges.

The `batch.sh' script feeds `compute_dispersion_and_modes.ctl' to the MPB program to get the numerical data. 
Then it runs `plot_dispersion_and_modes.py' to plot all results (see this file for explanation). This procedure 
can be repeated in a cycle in batch.sh, mapping how the electromagnetic behaviour of the structure changes with 
some of its parameters.

Written in 2013-15 by Filip Dominec, filip.dominec@gmail.com

== TODOs ==
[ ] sync with the project from 2014-01 and cleanup of old code
[ ] add all relevant structures (rods, holes, etc.)
[ ] enable electric/magnetic field switching
[ ] write some better documentation, add example plots
[ ] (test anisotropy of materials?)

== Dependencies ==
* mpb
* python-numpy
* python-matplotlib

