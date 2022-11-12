'''
1. Read html from folder list
2. Extract text from html
3. Save sampled context to tsv file
'''


import os
import re
import csv
import requests


def readHtml(fname):
    # Read html from folder list
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    return html


def getHtmlByURL(url):
    # Get html from URL
    return requests.get(url).text


def extractText(html):
    # Extract text from html
    title = re.findall(r'<title>(.*?)</title>', html)[0]
    item, site = title.split(' | ')
    
    blockquote = re.findall(r'<blockquote>(.*?)</blockquote>', html, re.DOTALL)[0]
    desc = re.findall(r'<p>(.*?)</p>', blockquote, re.DOTALL)[0]
    # print(repr(desc))
    
    breadcrumbs = re.findall(r'<div id="breadcrumbs-container">(.*?)</div>', html, re.DOTALL)[0]
    breadcrumbs = re.findall(r'>(.*?)</a>', breadcrumbs, re.DOTALL)

    cat = breadcrumbs[1]
    subcat = breadcrumbs[2]
    # print(cat, subcat)
    
    return (item, site, cat, subcat, desc)


def saveText(fname, sample):
    # Save text to tsv file
    with open(fname, 'a', newline='', encoding='utf-8') as f:
        # f.write(sample)
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(sample)
        

def createTitle(fname, title=None):
    # Create title for tsv file
    if title is None:
        title = ['item', 'site', 'category', 'subcategory', 'description'] # default title
    with open(fname, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(title)
    
if __name__ == "__main__":
    # Create title for tsv file
    tsv = 'data/darksoul3_weapon.tsv'
    file_path = "./raw_ds3/"
    createTitle(tsv)
        
    # traverse all files and save samples
    file_count = 0;
    for fname in os.listdir(file_path):
        print(fname)
        if os.path.isfile(os.path.join(file_path, fname)):
            file_count += 1
            html = readHtml(os.path.join(file_path, fname))
            sample = extractText(html)
            saveText(tsv, sample)
        else:
            print(fname, 'is not a file')

    print(file_count)
