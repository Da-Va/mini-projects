# source: https://stackoverflow.com/questions/75462164/vedo-3d-gyroid-structures-stl-export

from matplotlib import pyplot as plt
from scipy.constants import speed_of_light
from vedo import *
import numpy as np

# Paramters
a = 5
length = 100
width = 100
height = 100

pi = np.pi

x, y, z = np.mgrid[:length, :width, :height]

def gen_strut(start, stop):
    '''Generate the strut parameter t for the gyroid surface. Create a linear gradient'''
    strut_param = np.ones((length, 1))
    strut_param = strut_param * np.linspace(start, stop, width)
    t = np.repeat(strut_param[:, :, np.newaxis], height, axis=2)
    return t

plt = Plotter(shape=(1, 1), interactive=False, axes=3)


scale=0.5
D = np.sqrt((x)**2 + (y-50)**2 + (z-50)**2)
D = D / np.max(D)
D = np.sqrt(0.5*D + 1.0)
cox = cos(scale * pi * x**D / a)
siy = sin(scale * pi * y**D / a)
coy = cos(scale * pi * y**D / a)
siz = sin(scale * pi * z**D / a)
coz = cos(scale * pi * z**D / a)
six = sin(scale * pi * x**D / a)
U1 = ((six ** 2) * (coy ** 2) +
      (siy ** 2) * (coz ** 2) +
      (siz ** 2) * (cox ** 2) +
      (2 * six * coy * siy * coz) +
      (2 * six * coy * siz * cox) +
      (2 * cox * siy * siz * coz)) - (gen_strut(0, 1.3) ** 2)
U1 = ((six) * (coy) +
     +(siy) * (coz) +
     +(siz) * (cox)
     )

threshold = 0
iso1 = Volume(U1).isosurface(threshold).c('silver').alpha(1)
cube = TessellatedBox(n=(int(length-1), int(width-1), int(height-1)), spacing=(1, 1, 1))
# iso_cut = cube.cutWithMesh(iso1).c('silver').alpha(1)
# Combine the two meshes into a single mesh

# plt.at(0).show([cube, iso1], "Double Gyroid 1", resetcam=False)
plt.at(0).show([iso1], "Double Gyroid 1", resetcam=False)
plt.interactive().close()