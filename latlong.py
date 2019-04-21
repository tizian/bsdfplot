import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"

colorbar = True
title    = "Latlong BRDF Plot"
data     = np.load("example_data/conductor_ggx_0.2_60.npy")

fig, ax = plt.subplots(figsize=(8, 4))

im = ax.imshow(data, extent=[0, 360, 180, 0], cmap='jet')

plt.xlabel(r'$\phi_o$', size=14, ha='center', va='top')
l=plt.ylabel(r'$\theta_o$', size=14, ha='right', va='center')
l.set_rotation(0)
ax.set_xticks([0, 180, 360])
ax.set_yticks([0, 90, 180])

if title:
    plt.title(title, size=10, weight='bold')

if colorbar:
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='3%', pad=0.1)
    plt.colorbar(im, cax=cax)

plt.savefig("latlong.pdf")
plt.show()

