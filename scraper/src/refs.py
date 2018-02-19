# Imports ------------------------------------
import urllib.request as url_req
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import re
import tqdm

# Links, headers, parsers -------------------

def open_link(link):

    comm = re.compile('<!--|-->')
    request = url_req.urlopen(link)
    soup = BeautifulSoup(comm.sub('', request.read().decode('utf-8')), 'lxml')

    return soup

def get_officials():

    soup = open_link(REFS_ROOT)
    table = soup.find('table', {'id': 'officials'})
    rows = table.find_all('tr')
    header = rows[0].find('th')
    cols = ['id']
    cols.append(header['data-stat'])
    df = pd.DataFrame(columns=cols)
    ref_list = []

    for idx, row in enumerate(rows[1:]):

        vals = row.find('th')
        one_row = [vals.text]
        vals = vals.find('a')
        ref_id = vals['href'].split('.')[0].split('/')[2]
        one_row = [ref_id] + one_row

        ref_list.append(ref_id)
        df.loc[idx] = one_row

    return df, ref_list


def get_official_all_games(official_id):

    soup = open_link(REF_STR.format(official_id))
    table = soup.find('table', {'id': 'games'})
    rows = table.find_all('tr')
    header = rows[0].find_all('th')
    cols = ['id']
    [cols.append(col['data-stat']) for col in header]
    df = pd.DataFrame(columns=cols)

    for idx, row in enumerate(rows[1:]):

        try:

            one_row = [official_id]
            vals = row.find('th')
            vals = vals.find('a')
            one_row.append(vals['href'].split('.')[0].split('/')[2])

            vals = row.find_all('td')
            [one_row.append(val.text) for val in vals]

            df.loc[idx] = one_row

        except:
            pass

    return df






df, list = get_officials()
dfs = []
for ref in list:
    dfs.append(get_official_all_games(ref))

print('finished..')