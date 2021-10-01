"""
Minglang Yin, minglang_yin@brown.edu
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from fenics import *
from ufl import nabla_div
from mshr import *

path = 'Results'
os.makedirs(path, exist_ok=True)

def get_mu(E, nu):
    return E/(2*(1+nu))

def get_lambda(E, nu):
    return E*nu/((1+nu)*(1-2*nu))

def projection(u, pts):
    u_prj = []
    for x in pts:
        u_prj.append(u(x))
    return np.asarray(u_prj)

## parameters
tol = 1e-14

E1 = 1
nu1 = 0.4
mu1 = get_mu(E1, nu1)
lambda_1 = get_lambda(E1, nu1)

E2 = 2
nu2 = 0.4
mu2 = get_mu(E2, nu2)
lambda_2 = get_lambda(E2, nu2)

print(mu1, lambda_1)
print(mu2, lambda_2)

mu = Expression('x[0] < 0.5 + tol ? mu_1 : mu_2', degree=1, tol=tol, mu_1=mu1, mu_2=mu2)
lambda_ = Expression('x[0] < 0.5 + tol ? lmd_1 : lmd_2', degree=1, tol=tol, lmd_1=lambda_1, lmd_2=lambda_2)

x_plot = np.array([0.0, 1.0])

########## FEM ##########
## mesh
# mesh = RectangleMesh(Point(-1.0, -1.0), Point(1.0, 1.0), 51, 51, CellType.Type.quadrilateral)
# mesh = RectangleMesh.create([Point(-1.0, -1.0), Point(1.0, 1.0)],[51, 51],CellType.Type.quadrilateral)
mesh = UnitSquareMesh(26, 26, "right/left")
plot(mesh)
plt.savefig("mesh.png")

mesh_coord = mesh.coordinates()

## Space and Boundary
W = TensorFunctionSpace(mesh, "CG", 2)
V = VectorFunctionSpace(mesh, "CG", 2)

bot = CompiledSubDomain("near(x[1], side) && on_boundary", side = 0.0)
bot_disp = Expression(("0.0", "0.0"), degree=1)
bc_bot = DirichletBC(V, bot_disp, bot)

top = CompiledSubDomain("near(x[1], side) && on_boundary", side = 1.0)
top_disp = Expression(("0.0","0.07629"), degree=1)
bc_top = DirichletBC(V, top_disp, top)

bcs = [bc_bot, bc_top]

## Initialization
def epsilon(u):
    return 0.5*(nabla_grad(u)+nabla_grad(u).T)

def sigma(u):
    return lambda_*nabla_div(u)*Identity(d) + 2*mu*epsilon(u)

u = TrialFunction(V)
d = u.geometric_dimension()
v = TestFunction(V)
f = Constant((0, 0))
a = inner(sigma(u), epsilon(v))*dx
L = dot(f, v)*dx ## ds is on the boundary
u = Function(V)

u_his = []

# Solve variational problem
solve(a == L, u, bcs)

# Cauchy stress 
sigma_proj = project(sigma(u), W)   # Cauchy Stress
sigma_pt = sigma_proj(x_plot)
dump = np.concatenate((x_plot, u(x_plot), sigma_pt), axis= 0)
u_his.append(dump)

sigma_coord = projection(sigma_proj, mesh_coord)
u_proj = projection(u, mesh_coord)
dump = np.concatenate((mesh_coord, u_proj, sigma_coord), axis= 1)
file_name = path + "/snapshot_FEM.dat"
np.savetxt(file_name, dump)

## save
file_name = path + "/result.xdmf"
file_results = XDMFFile(file_name)
file_results.parameters["flush_output"] = True
file_results.parameters["functions_share_mesh"] = True
file_results.write(u, 0.)
file_results.write(sigma_proj, 0.)

np.savetxt("stress_strain.dat", np.array(u_his))
