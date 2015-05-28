#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
This script plots the results of MPB (MIT Photonics Bands, http://ab-initio.mit.edu/wiki/index.php/MIT_Photonic_Bands)
in a visually attractive way. 

Near the center of the figure, the dispersion curves are shown for several lowest modes. 

The electric field shapes at the Gamma, X, and M-points are added at the sides, and clearly connected with the
respective points in the dispersion curves. Red-white-blue color scheme shows the perpendicular amplitude of the
electric field. Green lines depict the nodal planes, where the amplitude of E is always zero (for a monochromatic wave).
The black lines outline the dielectric structure.

This is just a plotting script. Run batch.sh to start whole computation.

(c) Filip Dominec 2013-2015
"""

## Import common moduli
import matplotlib, sys, os
import numpy as np
import h5py
from scipy.constants import c, hbar, pi
import matplotlib.pyplot as plt
import matplotlib.cm as cm

filename = "freq.csv"
bandnumber = 6
cellspacing = 100e-6
fcoef = c / cellspacing
funit = 1e12
contourcount = 20
# format
# "kgrid:, band, kx, [frequencies at different Ky]"
band    = np.loadtxt(filename, usecols=[1], unpack=True, delimiter=',', skiprows=1) 
Kx_allbands      = np.loadtxt(filename, usecols=[2], unpack=True, delimiter=',', skiprows=1)
with open(filename) as f: colcount = len(f.readlines()[0].split(','))
Ky      = 0.0+np.arange(0,colcount-4, dtype=np.float64) / (colcount-4) / 2
freqs_allbands = np.loadtxt(filename, usecols=range(3,colcount-1), unpack=True, delimiter=',', skiprows=1)

def plot_IFC_guidecircles():#{{{
    ls = np.linspace(0,.5*np.pi)
    plt.plot(-np.sin(ls)*.50+.5,  -np.cos(ls)*.50+.5,  c='k', lw=.15)
    plt.plot( np.sin(ls)*.50+.0,   np.cos(ls)*.50+.0,  c='k', lw=.15)
    plt.plot(-np.sin(ls)*.25+.5,  -np.cos(ls)*.25+.5,  c='k', lw=.15)
    plt.plot( np.sin(ls)*.25+.0,   np.cos(ls)*.25+.0,  c='k', lw=.15)
    plt.plot(-np.sin(ls)*.125+.5, -np.cos(ls)*.125+.5, c='k', lw=.15)
    plt.plot( np.sin(ls)*.125+.0,  np.cos(ls)*.125+.0, c='k', lw=.15)
#}}}
def plot_IFC(Kx, Ky, freqs):#{{{

    ## Plot the iso-frequency contours (IFC)
    #                           np.linspace(0., 1., 100)
    plt.title('IFC for band %d' % selectband)
    plt.legend(prop={'size':10}, loc='upper right')
    plt.contourf(Kx, Ky, freqs*fcoef/funit, 50, cmap=cm.jet); plt.colorbar()
    plt.clabel(plt.contour(Kx, Ky, freqs*fcoef/funit, colors='k', levels=np.arange(0., funit*10, funit/10)))


    plt.annotate("$\Gamma$", xy = (.001, .001), xytext = (10, 10),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round, pad=.15', fc='white', alpha=0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    plt.annotate("X", xy = (.499,.001), xytext = (-10, 10),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round, pad=.15', fc='white', alpha=0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    plt.annotate("M", xy = (.499,.499), xytext = (-10, -10),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round, pad=.15', fc='white', alpha=0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.xlabel(u"$K_x a /(2\\pi)$"); plt.ylabel(u"$K_y a /(2\\pi)$"); 
    plt.xlim((0,.5)); plt.ylim((0,.5))
    plt.grid(True)
#}}}
def generate_filenames(k=1, band=1, pol='tm'):#{{{
    file_Ez = 'e.k%02d.b%02d.z.%s.h5' % (k, band, pol)
    file_Hx = 'h.k%02d.b%02d.x.%s.h5' % (k, band, pol)
    file_Hy = 'h.k%02d.b%02d.y.%s.h5' % (k, band, pol)
    return file_Ez, file_Hx, file_Hy
#}}}
def plot_mode(file1, file2, file3, title='', plot_vectors=True):#{{{
    #print "---------"
    #print h5py.File('epsilon.h5', "r").keys()
    #print h5py.File(file2, "r").keys()
    eps = np.array(h5py.File('epsilon.h5', "r")['data-new'])
    Ez_data = np.array(h5py.File(file1, "r")['z.i-new'])
    Hx_data = np.array(h5py.File(file2, "r")['x.r-new'])
    Hy_data = np.array(h5py.File(file3, "r")['y.r-new'])

    ## Location of data points
    xpoints = np.linspace(0, 1, len(Ez_data))
    ypoints = np.linspace(0, 1, len(Ez_data[0]))

    ## Plot the scalar values, normalize the field amplitude scale
    lvlextent = max(np.abs(np.min(Ez_data)), np.abs(np.max(Ez_data)))
    contours = plt.contourf(xpoints, ypoints, Ez_data, cmap=matplotlib.cm.RdBu, levels=np.linspace(-lvlextent, lvlextent, contourcount), label='')
    for contour in contours.collections: contour.set_antialiased(False) ## fix aliasing for old Matplotlib
    plt.contour(xpoints, ypoints, Ez_data, levels=[0], label='', colors='#00ff00', lw=2, alpha=.5)

    ## Plot permittivity
    plt.contour(xpoints, ypoints, eps, colors='k',alpha=1, label='', lw=4, levels=[1.5])

    ## Plot the vector field
    if plot_vectors:
        xgrid, ygrid    = np.meshgrid(xpoints, ypoints)                 ## the vector locations
        plt.quiver(xgrid, ygrid, Hy_data, Hx_data, pivot='middle', headwidth=3, headlength=6, label='')
    if title: plt.title(title)

    ## Finish the graph + save 
    #plt.xlabel(u"$y/(2a)$"); plt.ylabel(u"$x/(2a)$"); 
#}}}


#columncount = 3     # Gamma-modes, bandstructure, X-modes
columncount = 4     # Gamma-modes, bandstructure, X-modes, M-modes
plot_vector = False


plt.figure(figsize=(3*columncount, 16))



# Plot the band structure
try:
    plt.subplot2grid((bandnumber,columncount), (0,1), rowspan=bandnumber)
    for plotband in range(1,1+bandnumber):
        freqs = ((freqs_allbands.T)[band==plotband]).T

        Kx      = Kx_allbands[band==plotband]     # Filter the data for the selected band
        freqs_GammaUptoX = freqs[:][0]
        plt.plot(Kx, freqs_GammaUptoX*fcoef/funit, label=u"band #$%d$"%(plotband-1), ls='-', lw=2, c='k')

        #Ky      = Ky     # Filter the data for the selected band
        freqs_XUptoM = freqs[:,-1]
        plt.plot(Ky+.5, freqs_XUptoM*fcoef/funit, label=u"band #$%d$"%(plotband-1), ls='-',  lw=2, c='#888888')

        ## Floating annotation of the points at the dispersion curves
        bbox_args = dict(boxstyle="round, pad=.1", fc='w', ec='w', color='#ffffff', alpha=.7)
        arrow_args = dict(arrowstyle="->", color='r', lw=1, alpha=1)
        plt.annotate('$\Gamma%d$'%plotband, xy=((1./columncount-.02), (plotband - .5)/bandnumber),  xycoords='figure fraction',
                     xytext=(-.05, freqs_GammaUptoX[0]*3), textcoords='data',
                     ha="left", va="bottom", bbox=bbox_args, arrowprops=arrow_args)
        plt.annotate('$X%d$'%plotband, xy=(2./columncount+.02, (plotband - .5)/bandnumber),  xycoords='figure fraction',
                     xytext=(.50, freqs_GammaUptoX[-1]*3), textcoords='data',
                     ha="left", va="bottom", bbox=bbox_args, arrowprops=arrow_args)
        if columncount == 4:
            plt.annotate('$M%d$'%plotband, xy=(1.-(1./columncount), (plotband - .5)/bandnumber),  xycoords='figure fraction',
                         xytext=(1.02, freqs_XUptoM[-1]*3), textcoords='data',
                         ha="left", va="bottom", bbox=bbox_args, arrowprops=None) # do not plot arrow connecting to the M-point modes; the plot would be messy
        #plt.ylim((0,1.75))
    plt.xlabel(u"wave vector path along $\Gamma-X-M$ curve"); 
    plt.ylabel(u""); 

except: 
    print "bands could not be plotted!", sys.exc_info() 
    raise





for selectband in range(1,1+bandnumber):

    #try:
        # Plot the IFC
        #plt.subplot(2, 2, 1, adjustable='box', aspect=1)
        #Kx      = Kx_allbands[band==selectband]     # Filter the data for the selected band
        #freqs = ((freqs_allbands.T)[band==selectband]).T
        #plot_IFC(Kx, Ky, freqs)
        #plt.plot([0], Ky, freqs)
    #except: print "IFC could not be plotted!" , sys.exc_info() 


    if selectband > 1:          ## avoid plotting the field at zero frequency (
        try:
            ##Plot the MODE at Gamma-point
            ax = plt.subplot2grid((bandnumber,columncount), (bandnumber-(selectband), 0))
            ax.set_xticks([])
            ax.set_yticks([])
            filenames = generate_filenames(k=04, band=selectband, pol='tm')
            plot_mode(*filenames, title='$\Gamma%d$' % selectband, plot_vectors=plot_vector)
        except: 
            print "Mode00 could not be plotted!", sys.exc_info() 
            #raise

    try:
        ## Plot the MODE at X-point
        ax = plt.subplot2grid((bandnumber,columncount), (bandnumber-(selectband), 2))
        ax.set_xticks([])
        ax.set_yticks([])
        filenames = generate_filenames(k=1, band=selectband, pol='tm')
        plot_mode(*filenames, title='$X%d$' % selectband, plot_vectors=plot_vector)
    except: print "Mode01 could not be plotted!", sys.exc_info() 

    if columncount == 4:
        try:
            ## Plot the MODE at M-point
            ax = plt.subplot2grid((bandnumber,columncount), (bandnumber-(selectband), 3))
            ax.set_xticks([])
            ax.set_yticks([])
            filenames = generate_filenames(k=22, band=selectband, pol='tm')
            if not os.path.exists(filenames[0]): filenames = generate_filenames(k=12, band=selectband, pol='tm')
            plot_mode(*filenames, title='$M%d$' % selectband, plot_vectors=plot_vector)
        except: print "Mode12 could not be plotted!", sys.exc_info() 

## Finish the plot
plt.savefig("EBars_eps100_%s.png" % ("_".join(sys.argv[1:]) if len(sys.argv)>1 else ''),  bbox_inches='tight')

