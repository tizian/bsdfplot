import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"

data = np.load("example_data/conductor_ggx_0.2_60.npy")
theta_res = data.shape[0]
phi_res   = data.shape[1]

zenith_i        = 60.0
azimuth_i       = 0.0
transmission    = False
incident_marker = True
azimuth_marker  = False
title           = "Polar BRDF Plot"


plt.figure(figsize=(12,4))

outer = gridspec.GridSpec(1, 2, wspace=0.0, hspace=0.0)
gs = gridspec.GridSpecFromSubplotSpec(1, 3, wspace=0.05, width_ratios=[0.01, 1.0, 0.06], subplot_spec = outer[0])
ax0 = plt.subplot(gs[0])
ax0.axis('off')

## Setup main polar plot
ax1 = plt.subplot(gs[1], projection='polar')

# Determine which case
if zenith_i < 90 and not transmission:
    component = 'Rt'
elif zenith_i < 90 and transmission:
    component = 'Ttb'
elif zenith_i >= 90 and not transmission:
    component = 'Rb'
else:
    component = 'Tbt'

# Convert incident direction to radians
phi_i   = np.radians(azimuth_i)
theta_i = np.radians(zenith_i)

# Setup phi ticks & labels
azimuths      = np.linspace(0, 360, phi_res)
phi_ticks_deg = np.array([0, 45, 90, 135, 180, 225, 270, 315], dtype=np.float32)
phi_labels    = [("%d˚" % i) for i in phi_ticks_deg]
if azimuth_marker:
    phi_labels[0] = ""; phi_labels[4] = ""
phi_ticks_deg -= np.degrees(phi_i)
phi_ticks_deg = np.where(phi_ticks_deg < 0, phi_ticks_deg + 360, phi_ticks_deg)
phi_ticks_deg = np.where(phi_ticks_deg > 360, phi_ticks_deg - 360, phi_ticks_deg)

# Setup theta ticks & labels.
if component == 'Rt' or component == 'Tbt':
    zeniths = np.linspace(0, 90, theta_res//2)
    theta_ticks_deg = [10, 30, 50, 70, 90]
    theta_labels = ['0˚', '', '', '', '90˚']
elif component == 'Rb' or component == 'Ttb':
    zeniths = np.linspace(90, 180, theta_res//2)
    theta_ticks_deg = [180, 160, 140, 120, 100]
    theta_labels = ['90˚', '', '', '', '180˚']

# Setup extents & data
theta_o, phi_o = np.meshgrid(np.radians(zeniths), np.radians(azimuths))
if component == 'Rt' or component == 'Tbt':
    data_hemisphere = data[0:theta_res//2, :]
    theta_o_plot = theta_o
    theta_i_plot = theta_i
else:
    data_hemisphere = data[theta_res//2:, :]
    theta_o_plot = np.radians(270) - theta_o
    theta_i_plot = np.abs(np.radians(270) - theta_i)
phi_o_plot = phi_o + np.pi
phi_i_plot = np.pi

# Set style
ax1.grid(linestyle='-', linewidth=0.6, alpha=0.3, color='w')
ax1.set_rgrids(np.radians(theta_ticks_deg),
               labels=theta_labels,
               angle=270,
               color='w',
               fontweight='ultralight',
               size='10',
               ha='center',
               alpha=0.8)
ax1.set_thetagrids(phi_ticks_deg,
                   labels=phi_labels,
                   color='k',
                   fontweight='ultralight',
                   size='10',
                   ha='center',
                   va='center',
                   alpha=0.8,
                   frac=1.13)

# Create actual plot
view = ax1.contourf(phi_o_plot, theta_o_plot, data_hemisphere.T, 100, cmap='jet')

# Remove contour lines edges
for c in view.collections:
    c.set_edgecolor("face")
    c.set_rasterized(True)

# Optionally set incident direction marker
if incident_marker and (component == 'Rt' or component == 'Rb'):
    xy = (phi_i_plot, theta_i_plot)
    ax1.plot(xy[0], xy[1], 'x', color='w', ms='10', mew=3)

# Optionally show azimuth rotation markers
if azimuth_marker:
    dr = 0.1
    if component == 'Rb' or component == 'Ttb':
        dstart = np.pi
    else:
        dstart = 0.5*np.pi
    orientation_line_radii = [dstart, dstart + dr]

    x, y = np.array([[-phi_i, -phi_i], orientation_line_radii])
    line = mlines.Line2D(x, y, lw=30, color='k')
    line.set_zorder(0)
    line.set_clip_on(False)
    ax1.add_line(line)

    x, y = np.array([[-phi_i - np.pi, -phi_i - np.pi], orientation_line_radii])
    line = mlines.Line2D(x, y, lw=30, color='k')
    line.set_zorder(0)
    line.set_clip_on(False)
    ax1.add_line(line)

# Make outline edge bold
[i.set_linewidth(2) for i in ax1.spines.values()]

# Set title
ax1.set_title(title, size=9, y=1.1, weight='bold')

## Setup colorbar
ax2 = plt.subplot(gs[2])
ax2.set_aspect(14.0)
cb = plt.colorbar(view, cax=ax2, format='%.2f')

plt.savefig("polar.pdf", bbox_inches = 'tight')
plt.show()

