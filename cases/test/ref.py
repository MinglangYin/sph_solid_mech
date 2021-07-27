# --- This file converts atom-style full to atom-style bond
# --- Only read and modify the atom section.
# --- Need the full path.
# ---
# --- Ansel Blumers


import numpy as np
import os
import glob
import sys


# Usage
if ( len(sys.argv) < 3 ):
    raise Exception('Usage: python file.py file.data n_concentration')


nspecies = int(sys.argv[2])		# number of species


# IMPORTANT : the full file path must be enclosed in single quote
fnames = glob.glob(str(sys.argv[1]))
paths = [os.path.split(i)[0] for i in fnames]
newfnames = ['tDPDmeso_spec'+str(nspecies)+'_'+os.path.split(i)[1] for i in fnames]
newfnames = [os.path.join(paths[i], newfnames[i]) for i in range(len(newfnames))]



def emptyline(thisline):        # check whether thisline is empty.
    if not (len(thisline.split()) == 0):
        raise Exception("Not an empty line.")

for ct,fn in enumerate(fnames):
    with open(newfnames[ct],'w') as fnew:
        with open(fn) as f:
            while True:
                currentline = f.readline()
                fnew.write(currentline)
                words = currentline.split()
                if 'Atoms' in words: 
                    break
            emptyline(f.readline())   # Empty line after section header.
            fnew.write('\n')
            while True:
                currentline = f.readline()
                words = currentline.split()
                if len(words)==0 : 
                    break		# signaling the end of 'Atoms' section
                #####################################
                # Do modification here --------------
                del words[3]
                
                if words[2] == "2":
                    #for i in range(0,nspecies): 	# pass in number of species as argument
                    words.append('1.0')
                else:
                    # for i in range(0,nspecies): 	# pass in number of species as argument
                    words.append('0.0')
                 #   words.append('0.0')

                # -----------------------------------
                #####################################
                fnew.write(" ".join(words))
                fnew.write('\n')
            fnew.write('\n')   # After 'Atoms' section.
            while True:
                # read the rest of the file - until there is no bytes left.
                currentline = f.readline()
                if not currentline: break
                fnew.write(currentline)
    print("%d/%d file is done." % (ct+1, len(fnames)))
