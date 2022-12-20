#!/usr/bin/env python3


import random
import re


from mastodon import Mastodon
import requests


if __name__ == '__main__':
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
    mastodon = Mastodon(
        access_token = 'token.secret',
        api_base_url = 'https://botsin.space',
    )
    mastodon.toot(text)
