"""
GravMag: Use an equivalent layer to reduce a magnetic total field anomaly to the
pole
"""
from fatiando.gravmag import prism, sphere
from fatiando.gravmag.eqlayer import EQLTotalField
from fatiando.inversion.regularization import Smoothness2D
from fatiando import gridder, utils, mesher
from fatiando.vis import mpl

# Make synthetic data
inc, dec = -60, 23
props = {'magnetization':10}
model = [mesher.Prism(-500, 500, -1000, 1000, 500, 4000, props)]
shape = (25, 25)
x, y, z = gridder.regular([-5000, 5000, -5000, 5000], shape, z=0)
tf = utils.contaminate(prism.tf(x, y, z, model, inc, dec), 5)
# Setup the layer
layer = mesher.PointGrid([-7000, 7000, -7000, 7000], 1000, (50, 50))
# Estimate the magnetization intensity
# Need to apply regularization so that won't try to fit the error as well
solver = (EQLTotalField(x, y, z, tf, inc, dec, layer) +
          10**-17*Smoothness2D(layer.shape)).fit()
residuals = solver.residuals()
layer.addprop('magnetization', solver.estimate_)
print "Residuals:"
print "mean:", residuals.mean()
print "stddev:", residuals.std()
# Plot the layer and the fit
mpl.figure(figsize=(14,4))
mpl.subplot(1, 3, 1)
mpl.axis('scaled')
mpl.title('Layer (A/m)')
mpl.pcolor(layer.y, layer.x, layer.props['magnetization'], layer.shape)
mpl.colorbar()
mpl.m2km()
mpl.subplot(1, 3, 2)
mpl.axis('scaled')
mpl.title('Fit (nT)')
levels = mpl.contour(y, x, tf, shape, 15, color='r')
mpl.contour(y, x, solver.predicted(), shape, levels, color='k')
mpl.m2km()
mpl.subplot(1, 3, 3)
mpl.title('Residuals (nT)')
mpl.hist(residuals, bins=10)
mpl.show()
# Now I can forward model the layer at the south pole and check against the
# true solution of the prism
tfpole = prism.tf(x, y, z, model, -90, 0)
tfreduced = sphere.tf(x, y, z, layer, -90, 0)
mpl.figure()
mpl.axis('scaled')
mpl.title('True (red) | Reduced (black)')
levels = mpl.contour(y, x, tfpole, shape, 12, color='r')
mpl.contour(y, x, tfreduced, shape, levels, color='k')
mpl.m2km()
mpl.show()
