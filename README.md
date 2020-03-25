# PMMS-gates

The Phase Modulated Molmer-Sorensen gate package provides various solutions to developing and analyzing PM gates. The elements are :

- cardiod.py :
  Time sampling of a Two-Tone MS gate and phase finder in order to compare to a PM gate
  
- phase_conversion.py :
  Conversion of vector phases to light phases
 
## Cardiod Analysis

The Two-Tone MS gate leads to a cardiod trajectory in phase space. The same trajectory can be implemented with Phase Modulation. Sampling and phase finding tools are therefore provided for the sake of comparison. 

The cardiod trajectory is sampled into N equidistant points. The distance between each N points must first be found, by calling :
```
opt_dist = optimizeSampleLen(20, pi)
```
In this specific example, we sample N = 20 points, with a gate time of pi seconds. The sampled times can then be retrieved: 
```
sample_times = sampleTimes(opt_dist, 20)
```
The sampling can be visualised with the cardiod trajectory with the following function :
```
plotSampleTimes(sample_times)
```
Finally, the angles of the vectors built from the sampled times can be found and visualized with :
```
thetas = findVectAngles(sample_times)
plotAngles(thetas)
```

## Phase Conversion

The angles of the vectors making up a trajectory in phase space must be converted to phases of light fields. This is done by invoking the following function :
```
phis = convertAngles(thetas, 2)
```
where the second parameters is the gate detuning, in this case delta = 2 Hz. The series of phases phis can now be implemented at a physical level.
