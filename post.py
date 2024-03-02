#!/usr/bin/env python3


import random
import re


from bs4 import BeautifulSoup
from bs4.element import Tag
from mastodon import Mastodon
import requests
from urllib.parse import quote


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


def text_departicipal_verb():
    return random_definition('Partizipation')


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
    dls = soup.find_all('dl')
    dl = random.choice(dls)
    dts = dl.find_all('dt')
    dt = random.choice(dts)
    # Collect <dd>s
    dds = []
    for sibling in dt.next_siblings:
        if type(sibling) == Tag:
            if sibling.name != 'dd':
                break
            dds.append(sibling)
    # Build text
    text = dt.get_text()
    text += ':'
    for dd in dds:
        text += ' '
        text += dd.get_text()
    # Add link
    text += ' https://neutsch.org/' + quote(title)
    # Return
    return text


if __name__ == '__main__':
    f = random.choice((text_verb, text_antonym, text_departicipal_verb))
    text = f()
    #print(text)
    mastodon = Mastodon(
        access_token = 'token.secret',
        api_base_url = 'https://botsin.space',
    )
    mastodon.toot(text)
