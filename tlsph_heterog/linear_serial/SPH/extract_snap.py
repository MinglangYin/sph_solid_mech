"""
python extract_pointdata.py dump.LAMMPS <id>
"""
import numpy as np
import os
import glob
import sys

# Usage
path = 'snapshots'
os.makedirs(path, exist_ok=True)

# IMPORTANT : the full file path must be enclosed in single quote
fnames = glob.glob(str(sys.argv[1]))
num_snap = glob.glob(int(sys.argv[1]))

def emptyline(thisline):        # check whether thisline is empty.
    if not (len(thisline.split()) == 0):
        raise Exception("Not an empty line.")

with open(fnames) as f:
    for id in range(0, num_snap):
        fdump = path + "/snap_" + str(id) + ".dat"
        currentline = f.readline()
        currentline = f.readline()
        currentline = f.readline()
        currentline = f.readline()

        with open(fdump,'w') as fnew:
        
            
    
        
            if not currentline: break

            currentline = f.readline()
            words = currentline.split()
            fnew.write(" ".join(words))
            fnew.write('\n')
            
                if len(words) == 2:
                    if words[1] == "TIMESTEP": 
                        fnew.close()
                        ct += 1
                        break
        if not currentline: break
