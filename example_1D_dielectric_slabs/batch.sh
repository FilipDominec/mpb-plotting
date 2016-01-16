## Clean all old files
#rm *png

## == Parametric bandstructure sweep ==
GUILE_WARN_DEPRECATED="no"
mkdir data -p

#for rr in `seq 90 2 120`
#for rr in 0 3000 10000 30000
#for rr in 0 3000 10000 12000
rr=10000

#for ee in `seq 1 1 20`
for ee in `seq 1 1 20`
do
	## Prepare and print the parameters that are used in IFC.ctl to define the structure
	param="R=$rr eps=${ee}"		
    echo Plotting dispersion curves and modes for parameters: $param

    ## Generate IFC and fields (at Gamma, X and M points)
	mpb $param ../compute_dispersion_and_modes.ctl | grep kgrid > freq.csv
    cp freq.csv data/freq_`echo $param | tr ' ' '_'`.csv
	mpb-data -m 2 compute_dispersion_and_modes-*h5 
	mpb-data -m 2 compute_dispersion_and_modes-epsilon.h5

	## Plot the results
	python ../plot_dispersion_and_modes.py $param 
	#python ../IFC_plot.py $param 
	#python ../Nplot.py $param 
	#python ../HxHyEz_plot.py  [e].*h5 [h].*h5 [h].*h5

	## Clean up
    rm -r compute_dispersion_and_modes-*h5
done


