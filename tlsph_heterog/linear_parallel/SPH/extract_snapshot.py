"""
python extract_pointdata.py dump.LAMMPS
"""
import numpy as np
import os
import glob
import sys

save_path = "snapshots"
os.makedirs(save_path, exist_ok=True)

# IMPORTANT : the full file path must be enclosed in single quote
fname = "dump.LAMMPS"

def emptyline(thisline):        # check whether thisline is empty.
    if not (len(thisline.split()) == 0):
        raise Exception("Not an empty line.")

ct = 0
f = open(fname, 'r')
while True:
    currentline = f.readline()
    if not currentline: break
    words = currentline.split() 
    if words[1] == "TIMESTEP":
        if ct != 0:
            fnew.close()
        fnew_name = save_path + "/snapshot_" + str(ct) + ".dat"
        fnew = open(fnew_name, "w")
        ct += 1
        for _ in range(0, 8):
            currentline = f.readline()
    else:
        fnew.write(" ".join(words))
        fnew.write('\n')