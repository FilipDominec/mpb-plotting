; ------------------------------------------------------------------------------
; Code to output the data needed for a wavevector diagram at a grid of
; k points, suitable for plotting with a contour-plot program.

(define		
	(kgrid kx-min kx-max ky-min ky-max nkx nky)
	(map	
		(lambda 
			(kx) 
			(interpolate nky (list (vector3 kx ky-min) (vector3 kx ky-max))))
		(interpolate nkx (list kx-min kx-max))))

; ------------------------------------------------------------------------------
; output a bunch of lines of the form:
;					kgrid:, band#, kx, frequencies at kys...
; Frequencies above the light cone omega > c |k| / n-lightcone are
; excluded (multiplied by -1); set n-lightcone = 0 to disable this.

(define		
	(wavevector-diagram kgrid parity n-lightcone output)
	(map	
		(lambda 
			(kylist)
			(set! k-points kylist)
			(run-parity parity true)
			(map
				(lambda 
					(band)
					(if output (print "kgrid:, " band ", " (vector3-x (car kylist))))
					(map 
						(lambda 
							(freqs k)
							(print ", "
							(* 
								(if 
									(and 
										(positive? n-lightcone)
										(> 
											(list-ref freqs (- band 1))
											(* n-lightcone (vector3-norm (reciprocal->cartesian k))))) -1 1)
								(list-ref freqs (- band 1)))))
						  all-freqs k-points)
					(print "\n"))
			 (arith-sequence 1 1 num-bands)))
			kgrid))
; ------------------------------------------------------------------------------

(define-param R 20)
(define-param eps 10)
(define-param res 16)

(define-param Kx 0.5)

(set! num-bands 6)



(set! geometry 
	(list 
		(make block 
			(center 0 0 0) 
			(size R infinity infinity)
			(material (make dielectric (epsilon eps))))
	)
)

(set! geometry-lattice (make lattice (size 1 1 no-size)))

(set! resolution res)


; ----------- Export the field patterns for Gamma point (could not merge with X and M) -----------
(wavevector-diagram (kgrid 0 1. 0 1. 2 2 ) TM 0 false)
(run-tm (output-at-kpoint (vector3 1. 1. 0)	output-efield-z ))
(run-tm (output-at-kpoint (vector3 1. 1. 0)	output-hfield-x output-hfield-y))
	
; ----------- Export the IFC -----------
(wavevector-diagram (kgrid 0 .5 0 .5 20 20 ) TM 0 true)

; ----------- Export the field patterns for X and M points -----------

(run-tm (output-at-kpoint (vector3 .5 0  0)	output-efield-z ))
(run-tm (output-at-kpoint (vector3 .5 0  0)	output-hfield-x output-hfield-y))
(run-tm (output-at-kpoint (vector3 .5 .5 0)	output-efield-z))
(run-tm (output-at-kpoint (vector3 .5 .5 0)	output-hfield-x output-hfield-y))

