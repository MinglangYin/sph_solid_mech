"""
SPH code for solid mechanics, cantilever beam, statics, fix end
Minglang Yin, minglang_yin@brown.edu
"""
import numpy as np
import matplotlib.pyplot as plt

def get_w(x, h):
    r = abs(x - x.T)
    w = 10*(h-r)**3/(np.pi*h**5)

    ind = np.ones(r.shape)
    for id_x, rr in enumerate(r):
        for id_y, rrr in enumerate(rr):
            if rrr > h or rrr < -h:
                ind[id_x, id_y] = 0
    w = w*ind

    return w

def get_grad_w(x, h):
    r = abs(x - x.T)
    grad_w = -30*(h-r)**2/(np.pi*h**5)
    
    ind = np.ones(r.shape)
    for id_x, rr in enumerate(r):
        for id_y, rrr in enumerate(rr):
            if rrr > h or rrr < -h:
                ind[id_x, id_y] = 0
    grad_w = grad_w*ind

    return grad_w

# def strain_energy():
    
#     return w_c

def main():
    ## parameter
    L_l = 0.0
    L_r = 6.0

    N_x = 61
    h = 3
    x = np.linspace(L_l, L_r, N_x)[:, None]

    # weight = get_w(xx, yy, h)
    # grad_weight = get_grad_w(xx, yy, h)

    ## figure
    fig = plt.figure(constrained_layout=False, figsize=(6, 6))
    gs = fig.add_gridspec(1, 1)
    ax = fig.add_subplot(gs[0])
    h = ax.plot(x, '.')
    ax.set_xlim([-1, 7])
    # ax.set_ylim([-1, 7])
    # fig.colorbar(h)
    fig.savefig('./beam_pos.png')
    plt.close()
    

if __name__ == "__main__":
    main()