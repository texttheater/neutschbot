#!/usr/bin/env python3


import random
import re
import sys
import unicodedata
from urllib.parse import quote


from bs4 import BeautifulSoup
from bs4.element import Tag
from mastodon import Mastodon
import requests


def text_verb():
    r = requests.get('https://neutsch.org/api/verbs.php')
    r.raise_for_status()
    verbs = r.json()
    verb = random.choice(verbs)
    alpha = verb['alpha']
    inf = verb['inf']
    ind_praet = verb['ind_praet']
    konj_ii = verb['konj_ii']
    part_ii = verb['part_ii']
    text = f'{inf} – {ind_praet} – {konj_ii} – {part_ii}'
    text += f' https://neutsch.org/Starke_Verben/{alpha}'
    return text


def text_antonym():
    return random_definition('Antonyme')


def text_denegation():
    return random_definition('Entneinungen')


def text_departicipal_verb():
    return random_definition('Partizipation')


def text_rerivation():
    return random_definition('Morphologische Aufleitung')


def is_punctuation(char):
    return unicodedata.category(char)[0] == 'P'


def random_definition(title):
    # Get page data
    url = 'https://neutsch.org/api.php?action=parse&page=' + quote(title) + \
            '&format=json'
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    text = data['parse']['text']['*']
    # Find a <dt>
    soup = BeautifulSoup(text, features='html.parser')
    dts = soup.find_all('dt')
    dt = random.choice(dts)
    # Collect <dd>s
    dds = []
    for sibling in dt.next_siblings:
        if type(sibling) == Tag:
            if sibling.name != 'dd':
                break
            dds.append(sibling)
    # Build text
    text = dt.get_text().strip()
    text += ':'
    for dd in dds:
        text += ' '
        text += dd.get_text().strip()
        if not is_punctuation(text[-1]):
            text += '.'
    # Shorten if needed
    max_len = 500 - 24 # URL incl. space before it counted as 24 chars
    if len(text) > max_len:
        text = text[:max_len - 1] + '…'
    # Add URL
    text += ' https://neutsch.org/' + quote(title.replace(' ', '_'))
    # Return
    return text


def random_row(title, relation):
    # Get page data
    url = 'https://neutsch.org/api.php?action=parse&page=' + quote(title) + \
            '&format=json'
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    text = data['parse']['text']['*']
    # Find a non-header <tr>
    soup = BeautifulSoup(text, features='html.parser')
    trs = soup.find_all('tr')
    trs = [t for t in trs if t[0].name != 'th']
    tr = random.choice(trs)
    # Collect <td>s
    tds = tr.find_all('td')
    # Build text
    text = tds[0].get_text().strip()
    text += ' ('
    text += relation
    text += ' '
    text += td[1].get_text().strip()
    text += ') '
    text += td[2].get_text().strip()
    # Shorten if needed
    max_len = 500 - 24 # URL incl. space before it counted as 24 chars
    if len(text) > max_len:
        text = text[:max_len - 1] + '…'
    # Add URL
    text += ' https://neutsch.org/' + quote(title.replace(' ', '_'))
    # Return
    return text


if __name__ == '__main__':
    f = random.choice((text_verb, text_antonym, text_denegation,
        text_departicipal_verb, text_rerivation))
    text = f()
    print(text)
    if '-n' not in sys.argv:
        mastodon = Mastodon(
            access_token = 'token.secret',
            api_base_url = 'https://botsin.space',
        )
        mastodon.toot(text)
