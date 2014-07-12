"""
GravMag: Use the polynomial equivalent layer to upward continue gravity data
"""
from fatiando.gravmag import prism, sphere
from fatiando.gravmag.eqlayer import PELGravity, PELSmoothness
from fatiando import gridder, utils, mesher
from fatiando.vis import mpl

# Make synthetic data
props = {'density':1000}
model = [mesher.Prism(-500, 500, -1000, 1000, 500, 4000, props)]
shape = (50, 50)
x, y, z = gridder.regular([-5000, 5000, -5000, 5000], shape, z=0)
gz = utils.contaminate(prism.gz(x, y, z, model), 0.1)
# Setup the layer
layer = mesher.PointGrid([-5000, 5000, -5000, 5000], 200, (100, 100))
# Estimate the density using the PEL (it is faster and more memory efficient
# than the traditional equivalent layer).
windows = (20, 20)
degree = 1
solver = (PELGravity(x, y, z, gz, layer, windows, degree) +
          10**-21*PELSmoothness(layer, windows, degree)).fit()
layer.addprop('density', solver.estimate_)
residuals = solver.residuals()
print "Residuals:"
print "mean:", residuals.mean()
print "stddev:", residuals.std()

# Plot the layer and the fit
mpl.figure(figsize=(14, 4))
mpl.subplot(1, 3, 1)
mpl.axis('scaled')
mpl.title('Layer (kg.m^-3)')
mpl.pcolor(layer.y, layer.x, layer.props['density'], layer.shape)
mpl.colorbar()
mpl.m2km()
mpl.subplot(1, 3, 2)
mpl.axis('scaled')
mpl.title('Fit (mGal)')
levels = mpl.contour(y, x, gz, shape, 15, color='r')
mpl.contour(y, x, solver.predicted(), shape, levels, color='k')
mpl.m2km()
mpl.subplot(1, 3, 3)
mpl.title('Residuals (mGal)')
mpl.hist(residuals, bins=10)
mpl.show()

# Now I can forward model the layer at a greater height and check against the
# true solution of the prism
gz_true = prism.gz(x, y, z - 500, model)
gz_up = sphere.gz(x, y, z - 500, layer)

mpl.figure()
mpl.axis('scaled')
mpl.title('True (red) | Layer (black)')
levels = mpl.contour(y, x, gz_true, shape, 12, color='r')
mpl.contour(y, x, gz_up, shape, levels, color='k')
mpl.m2km()
mpl.show()
