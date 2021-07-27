import numpy as np

ntype = 2
fname = "wavy_plate.data"
dim = 21

x = np.linspace(-10, 10, dim)
y = np.linspace(-10, 10, dim)
xx, yy = np.meshgrid(x, y)

line = np.linspace(-1, 1, dim)
y_inc = np.sin(np.pi*line)[:, None]

xx = xx + y_inc
# print(xx.flatten())
# print(yy.flatten())
# exit()

xx = xx.flatten()
yy = yy.flatten()

with open(fname,'w') as f:
    f.write("LAMMPS\n")
    f.write("441 atoms\n")
    f.write("2 atom types\n")
    f.write("-11.000000 11.000000 xlo xhi\n")
    f.write("-10.000000 10.000000 ylo yhi\n")
    f.write("-0.100000 0.100000 zlo zhi\n")
    f.write("\n")

    f.write("Atoms\n")
    f.write("\n")

    for i in range(dim*dim):
        f.write("%d      1     1     %f      %f     0\n" %(i, xx[i], yy[i]))
        # print(x[i], y[i])
