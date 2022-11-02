'''
1. Read html from folder list
2. Extract text from html
3. Save sampled context to tsv file
'''

import os
from wikiReader import * # Path: experiments\wikiReader\wikiReader.py


if __name__ == "__main__":
    # Create title for tsv file
    tsv = 'data/experiment.tsv'
    createTitle(tsv)
        
    # traverse all files and save samples
    for fname in os.listdir('./raw/'):
        print(fname)
        if os.path.isfile(os.path.join('./raw/', fname)):
            html = readHtml(os.path.join('./raw/', fname))
            sample = extractText(html)
            saveText(tsv, sample)
        else:
            print(fname, 'is not a file')