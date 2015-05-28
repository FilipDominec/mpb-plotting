## Overview of mpb-plotting 

Plot photonic dispersion curves with mode shapes (a frontend to MIT Photonic bands, http://ab-initio.mit.edu/wiki/index.php/MIT_Photonic_Bands)

A set of Scheme/Python scripts that computes and plots the band structure of a 2-D photonic crystal and,
most importantly, draws also the modes corresponding to the band edges.

The `batch.sh' script feeds `compute_dispersion_and_modes.ctl' to the MPB program to get the numerical data. 
Then it runs `plot_dispersion_and_modes.py' to plot all results (see this file for explanation). This procedure 
can be repeated in a cycle in batch.sh, mapping how the electromagnetic behaviour of the structure changes with 
some of its parameters. The scripts can be fully customized and automated to fit your research.

Written in 2013-15 by Filip Dominec, filip.dominec@gmail.com

## Example 
A typical output of the script follows. This one shows six dispersion curves, and all corresponding modes, for 
a periodic dielectric slab with a permittivity of 2 and 30% filling fraction. 

The electric field shapes at the Gamma, X, and M-points are added at the sides, and clearly connected by red arrows with the
respective points in the dispersion curves. Red-white-blue color scheme shows the perpendicular amplitude of the
electric field. Green lines depict the nodal planes, where the amplitude of the electric field is always zero (for a monochromatic wave).
The black lines outline the dielectric structure.

For a more physical background, see the excellent book *Photonic Crystals: Molding the Flow of Light*  (freely available from http://ab-initio.mit.edu/book/)

![1-D dielectric slab dispersion curves and corresponding modes](./example_1D_dielectric_slabs/EBars_eps100_R=10000_eps=2.png)


## Requirements
* unix-like environment with a bash-like shell
* mpb
* python-scipy
* python-matplotlib
* (imagemagick)

## TODOs
* [ ] sync with the project from 2014-01 and cleanup of old code
* [ ] add all relevant structures (rods, holes, etc.)
* [ ] enable electric/magnetic field switching
* [ ] write some better documentation, add more example plots
* [ ] possibly test anisotropy of materials?
