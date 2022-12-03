'''
Construct raw data from HTML files
'''

HELP_MSG = "Use:\n\tpython3 HTMLReader.py <input directory path> <output file path> [-c]\n-c : combine mode, will combine files in input dir into one"

from asyncore import read
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
import csv

def combine(in_path, out_path):
    first_file = True

    for fname in os.listdir(in_path):
        
        context = pd.read_csv(os.path.join(in_path, fname), sep='\t')

        if first_file:
            context.to_csv(out_path, sep='\t', index = False)
            first_file = False
        else:
            context.to_csv(out_path, sep='\t', header=False, index = False, mode='a')


def createTSV(fname, samples, title=None):
    '''
    Generate one .tsv file from given samples
    '''

    # Create title for tsv file
    if title is None:
        title = ['item', 'site', 'category', 'subcategory', 'description'] # default title

    with open(fname, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(title)

        for sample in samples:
            # Save text to tsv file
            writer.writerow(sample)


def readHTML(fname):
    '''
    Read html content from fname
    '''
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    return html


def extractData(context):
    '''
    Find needed data from the given context
    context should in HTML format
    '''

    soup = BeautifulSoup(context, "html.parser")

    # First find the item name and source
    node = soup.find("title")
    content = node.get_text().split('|')
    if len(content) != 2:
        return None
    item = content[0].strip()
    src = content[1].strip()

    # Second find the category and subcategory
    node = soup.find("div", id="breadcrumbs-container").find_all("a")
    # if format mismatch, should skip the file
    if len(node) < 3:
        return None     
    cat = node[1].get_text()
    subcat = node[2].get_text()

    
    # Then find the description
    
    '''
    ------------------------------------------------------------------------------------
    Modify below part if any format mismatch found
    ------------------------------------------------------------------------------------
    '''

    # first try Dark Souls 3 style HTML format
    # where desc are located in <blockquote>
    node = soup.find_all("blockquote")
    # format mismatch
    if len(node) not in (0, 1):
        return None
    # Dark Soul 3 format
    elif len(node) == 1:
        desc = node[0].get_text()

    # Dark Soul 1, 2 format
    # as well as elden ring's
    # which located in first several occurances of <p>
    else:
        node = soup.find_all("p")

        desc = ""
        for subnode in node:
            ems = subnode.find_all("em")
            if len(ems) > 0:
                for s in ems:
                    # skipp the context that are too short
                    # usually they are not what we want
                    if (len(s.get_text()) > 5):
                        desc += s.get_text() + '\n'

    return (item, src, cat, subcat, desc)


#----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    if len(sys.argv) not in (3, 4):
        print(HELP_MSG)
        sys.exit()

    # combine mode
    if len(sys.argv) == 4:
        if sys.argv[3] == "-c":
            combine(sys.argv[1], sys.argv[2])
        else:
            print(HELP_MSG)
        
        sys.exit()

    # generate mode
    in_dir = sys.argv[1]
    out_file = sys.argv[2]

    file_done = 0

    samples = []
    skiped_file = []

    print("Running...")
    for fname in os.listdir(in_dir):
        file_path = os.path.join(in_dir, fname)

        if os.path.isfile(file_path):
            html = readHTML(file_path)
            sample = extractData(html)

            # if format mismatch
            if sample is None:
                skiped_file.append(fname)
                continue

            samples.append(sample)
            file_done += 1

        # if not file
        else:
            skiped_file.append(fname)
            print(fname, " is not a file")

        if (file_done + 1) % 100 == 0:
            print(f"{file_done + 1} files done...")
  
    print("Analyze Done...")
    print(f"Total {file_done} files")

    if len(skiped_file) > 0:
        print(f"Following {len(skiped_file)} file(s) have been skipped")
        for f in skiped_file:
            print(f)

    # generate file(s)
    createTSV(out_file, samples)
    print("Output file ", out_file, " generated...")