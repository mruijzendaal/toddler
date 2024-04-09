# Toddler: Tools and Operations for Diagnostics, Data, Light, and other Electromagnetic Radiation

> Data processing is often limiting the output of starting physicists. With this library,  I try to make at so easy a toddler kan do it.

![image](./assets/hero_256x256.png)

## Functionality
This module is split up into physics (e.g. conversion of units) and data processing (e.g. filtering images)


### Data
`toddler.data.spectrum.Spectrum` has the most utility of this library. It makes iterative processing on numpy arrays and its coordinates much simpler. The code below loads data of an optical spectrometer, applies some heavy processing, and plots the result. The equivalent code with out-of-the-box numpy would be much more convoluted.

```python
s = Spectrum.from_file("some_file.csv")
s = s.median(axis=2)
     .mean(axis=1)
     .slice(lambda_start=534e-9, lambda_end=600e-9)
     .filter("movmean", N=5)
     .squeeze()

plt.figure()
plt.plot(s.lambdanm, s.data)
plt.show()
```

### Physics
`toddler.physics.const` constains all [scipy constants](https://docs.scipy.org/doc/scipy/reference/constants.html). 

`toddler.physics.energy` contains utility functions related to energy (e.g. conversion from eV to J)

`toddler.physics.flow` contains utility functions related to flow (e.g. conversion from slm to mass flux)

`toddler.physics.kinetics` is an empty work-in-progress.

`toddler.physics.light` contains utility functions related to the intensity and unit of light (e.g. conversion from wavenumbers to wavelength)

`toddler.physics.thermodynamics` contains utilities for thermodynamic properties (e.g. pressure to gas density)

`toddler.physics.transport` is a work-in-progress.