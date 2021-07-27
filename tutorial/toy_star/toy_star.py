"""
SPH code for simulating Euler equation
Minglang Yin, minglang_yin@brown.edu
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

np.random.seed(42)
h_max = 0.1

def w(x, y, z, h):
    r = np.sqrt(x**2 + y**2 + z**2)
    # ind = np.ones(r.shape)
    # for id_x, rr in enumerate(r):
    #     for id_y, rrr in enumerate(rr):
    #         if rrr > h_max:
    #             ind[id_x, id_y] = 0
    w = (1.0 / (h*np.sqrt(np.pi)))**3 * np.exp( -r**2 / h**2)
    # w = w*ind
    return w

def grad_w(x, y, z, h):
    r = np.sqrt(x**2 + y**2 + z**2)
    n = -2 * np.exp( -r**2 / h**2) / h**5 / (np.pi)**(3/2) #-2/(h**5*np.pi**(3/2))*np.exp(-r**2/h**2)
    
    # ind = np.ones(r.shape)
    # for id_x, rr in enumerate(r):
    #     for id_y, rrr in enumerate(rr):
    #         if rrr > h_max:
    #             ind[id_x, id_y] = 0
    
    w_x = n*x#*ind
    w_y = n*y#*ind
    w_z = n*z#*ind
    return w_x, w_y, w_z

def get_pairwise_separations(r, pos):
    M = r.shape[0]
    N = pos.shape[0]

    # position
    rx = r[:, 0].reshape((M, 1))
    ry = r[:, 1].reshape((M, 1))
    rz = r[:, 2].reshape((M, 1))
    
    posx = pos[:, 0].reshape((N, 1))
    posy = pos[:, 1].reshape((N, 1))
    posz = pos[:, 2].reshape((N, 1))

    dx = rx - posx.T
    dy = ry - posy.T
    dz = rz - posz.T
    return dx, dy, dz

def get_density(r, pos, m, h):
    M = r.shape[0]
    dx, dy, dz = get_pairwise_separations(r, pos)
    weight = w(dx, dy, dz, h)
    rho = np.sum( m*weight, 1).reshape((M, 1))
    return rho

def get_pres(rho, k, n):
    p = k*rho**(1+1/n)
    return p

def get_acc( pos, vel, m, h, k, n, lmd, nu ):
    N = pos.shape[0]
    rho = get_density(pos, pos, m, h)
    P = get_pres(rho, k, n)
    dx, dy, dz = get_pairwise_separations(pos, pos)
    dw_x, dw_y, dw_z = grad_w(dx, dy, dz, h)

    a_x = -np.sum(m*(P/rho**2 + P.T/rho.T**2)*dw_x ,1).reshape((N, 1))
    a_y = -np.sum(m*(P/rho**2 + P.T/rho.T**2)*dw_y ,1).reshape((N, 1))
    a_z = -np.sum(m*(P/rho**2 + P.T/rho.T**2)*dw_z ,1).reshape((N, 1))
    a = np.hstack((a_x, a_y, a_z))
    f = - nu*vel -lmd*pos # -2*np.random.randn(N, 3)
    a += f
    return a


def get_init(N, M):
    m = M/N
    pos = np.random.randn(N, 3)
    # pos[:, 2] = 0
    vel = np.random.randn(N, 3)
    # vel[:, 2] = 0
    # vel = np.zeros(pos.shape)
    return m, pos, vel

def main():
    ## parameters
    N       = 400   # number of particles
    t_init  = 0     # initial time
    t_end   = 12    # end time
    dt      = 0.04  # time size
    M       = 2     # mass
    R       = 0.75  # star radius
    h       = 0.1   # smoothing length
    k       = 0.1   # state constant
    n       = 1     # polytropic index
    nu      = 1     # damping
    plot_realtime = True
    steps   = int((t_end-t_init)/dt)
    lmd = 2*k*(1+n)*np.pi**(-3/(2*n)) * (M*gamma(5/2+n)/R**3/gamma(1+n))**(1/n) / R**2  # ~ 2.01

    # get initial conditions
    m, pos, vel = get_init(N, M)

    # get initial accerlation
    acc = get_acc( pos, vel, m, h, k, n, lmd, nu )

    # prep figure
    fig = plt.figure(figsize=(4,5), dpi=80)
    grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.3)
    ax1 = plt.subplot(grid[0:2,0])
    ax2 = plt.subplot(grid[2,0])
    rr = np.zeros((100,3))
    rlin = np.linspace(0,1,100)
    rr[:,0] =rlin
    rho_analytic = lmd/(4*k) * (R**2 - rlin**2)

    # time stepping
    for i in range(0, steps):
        vel += acc*dt/2
        pos += vel*dt
        acc = get_acc(pos, vel, m, h, k, n, lmd, nu )
        vel += acc*dt/2
        t_init += dt
        rho = get_density( pos, pos, m, h )

        ## save plot
        # plot in real time
        if plot_realtime:
            plt.sca(ax1)
            plt.cla()
            cval = np.minimum((rho-3)/3,1).flatten()
            plt.scatter(pos[:,0],pos[:,1], c=cval, cmap=plt.cm.autumn, s=10, alpha=0.5)
            ax1.set(xlim=(-1.4, 1.4), ylim=(-1.2, 1.2))
            ax1.set_aspect('equal', 'box')
            ax1.set_xticks([-1,0,1])
            ax1.set_yticks([-1,0,1])
            ax1.set_facecolor('black')
            ax1.set_facecolor((.1,.1,.1))

            plt.sca(ax2)
            plt.cla()
            ax2.set(xlim=(0, 1), ylim=(0, 3))
            ax2.set_aspect(0.1)
            plt.plot(rlin, rho_analytic, color='gray', linewidth=2)
            rho_radial = get_density( rr, pos, m, h )
            plt.plot(rlin, rho_radial, color='blue')
            plt.pause(0.001)

            plt.savefig('./figure/sph_'+ str(i+100) +'.png',dpi=240)
	    
	
    # add labels/legend
    plt.sca(ax2)
    plt.xlabel('radius')
    plt.ylabel('density')

    # Save figure
    plt.savefig('sph.png',dpi=240)
    plt.show()
        

if __name__ == "__main__":
    main()