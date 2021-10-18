# bsdfplot

This repository contains simple Python scripts to create nice looking BSDF plots.

## Details

Plots are designed to visualize the outgoing domain of a BSDF, parameterized via spherical coordinates (*theta* from 0 - 180˚ and *phi* from 0 - 360˚), for a fixed incident direction.
The expected data format is a 2d *NumPy* array of shape `[theta_res, phi_res]`.

Some example data for microfacet conductors and dielectrics at various incident directions is provided as well.
 
All plotting is handled by [*matplotlib*](https://matplotlib.org/).

### Polar plots

A clear and intuitive visualization type is the *polar* plot which focuses on either the upper or lower hemisphere for displaying BRDF or BTDF data respectively.
There is additional support to mark incident direction or azimuthal rotation around the surface normal to help with anisotropic materials.

<img src="http://tizianzeltner.com/images/projects/bsdfplot/polar.gif" alt="polar" width="500"/>

### Latlong plots

The underlying data can also be directly visualized in a *latlong* plot over spherical coordinates.

<img src="http://tizianzeltner.com/images/projects/bsdfplot/latlong.gif" alt="polar" width="500"/>
