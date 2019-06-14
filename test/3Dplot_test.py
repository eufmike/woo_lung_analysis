import os, sys
import numpy as np
import pandas as pd
from core.fileop import DirCheck
from core.msxml import MSXmlReader
from mayavi import mlab

x = [1, 2, 3, 4, 5, 6]
y = [0, 0, 0, 0, 0, 0]
z = y

s = [.5, .6, .7, .8, .9, 1]

from mayavi import mlab
pts = mlab.points3d(x, y, z, s)
mlab.show()