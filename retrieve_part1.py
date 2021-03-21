from bs4 import BeautifulSoup
import re
import sys
import os
import shutil

print(os.listdir('sec-edgar-filings'))

def get_date(filing_dir, file_name):
    with open(os.path.join(filing_dir, file_name)) as file:
        for i, line in enumerate(file):
            if i == 15:
                break
            comps = line.split(':')
            str_ = comps[0].strip()
            if re.match('CONFORMED PERIOD OF REPORT', str_):
                return(comps[-1].strip())

def get_part1(filing_dir, file_name):
    file = open(os.path.join(filing_dir, file_name))
    html = BeautifulSoup(file.read(), 'html.parser')
    soup = html.prettify() # clean up html formatting, returns string
    html = BeautifulSoup(soup, 'html.parser')
    contents = html.get_text()
    text = " ".join(line.strip() for line in contents.split("\n")) # clean up resulting text
    text = " ".join(text.split()) 
    text = re.sub('[^A-Za-z0-9 ]+', '', text)
    pattern = '((PART I)\s*(Item 1|ITEM 1.)).+?(PART II\s)'
    try:
        part1 = re.search(pattern, text, re.DOTALL)[0]
        return part1
    except:
        print('ERROR getting Part 1')
        wf = open('error_file.txt', 'a')
        wf.write(text)
        wf.close()





base_dir = 'sec-edgar-filings'

company_tickers = os.listdir('sec-edgar-filings')
try:
    os.mkdir('data-part1')
except:
    pass

for ticker in company_tickers:
    if re.match('.DS_Store', ticker):
        continue
    curr_dir = os.path.join(base_dir, ticker, '10-K')
    dirs = os.listdir(curr_dir)
    try:
        os.mkdir(os.path.join('data-part1', ticker))
    except:
        pass
    for dir_ in dirs:
        filing_dir = os.path.join(curr_dir, dir_)
        date_of_coverage = get_date(filing_dir, 'full-submission.txt')
        if os.path.isfile('data-part1/' + ticker + '/' + ticker + '_' + date_of_coverage + '.txt'):
            print('Skipping ', ticker, ' ', date_of_coverage, 'because it already exists.')
            continue
        try:
            part1 = get_part1(filing_dir, 'filing-details.html')
            wf = open('data-part1/' + ticker + '/' + ticker + '_' + date_of_coverage + '.txt', 'a')
            wf.write(part1)
            wf.close()
        except:
            print("ERROR: ", ticker)
            continue