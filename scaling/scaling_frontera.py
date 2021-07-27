import numpy as np
import matplotlib.pyplot as plt

def main():
    wall_time = np.asarray([67*60+37, 17*60+27, 9*60+55, 6*60+2, 3*60+5, 1*60+37, 0*60+51])
    num_cpu = np.asarray([1, 4, 8, 16, 32, 64, 128])
    eff = wall_time[0]/wall_time
    print(eff)

    ## figure
    fig = plt.figure(constrained_layout=False, figsize=(8, 4))
    gs = fig.add_gridspec(1, 2)    

    ax = fig.add_subplot(gs[0])
    ax.plot(num_cpu, num_cpu , color='black', linewidth=2, linestyle='dashed', label='Upper Bound')
    ax.scatter(num_cpu, eff , color='red', linewidth=4, marker='^', label='LAMMPS SMD')
    ax.plot(num_cpu, eff , color='red', linewidth=2)

    ax.set_xlabel('Num. Cores')
    ax.set_ylabel('Speedup')
    ax.legend()

    ax = fig.add_subplot(gs[1])
    ax.plot(num_cpu, num_cpu , color='black', linewidth=2, linestyle='dashed', label='Upper Bound')
    ax.scatter(num_cpu, eff , color='red', linewidth=4, marker='^', label='LAMMPS SMD')
    ax.plot(num_cpu, eff , color='red', linewidth=2)

    ax.set_xlabel('Num. Cores')
    ax.set_ylabel('Speedup')
    ax.legend()
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.tight_layout()
    fig.savefig('./scaling_frontera.png')
    plt.close()    

if __name__ == "__main__":
    main()