'''
Combine .tsv files
'''

import os
import pandas as pd
import sys

def combine(in_path, out_path):
    first_file = True

    for fname in os.listdir(in_path):
        
        context = pd.read_csv(os.path.join(in_path, fname), sep='\t')

        if first_file:
            context.to_csv(out_path, sep='\t', index = False)
            first_file = False
        else:
            context.to_csv(out_path, sep='\t', header=False, index = False, mode='a')



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Use:\n\tpython3 combine.py <input directory path> <output file path>")
        sys.exit()

    combine(sys.argv[1], sys.argv[2])
