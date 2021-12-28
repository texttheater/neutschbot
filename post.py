#!/usr/bin/env python3


import config
import mysql.connector
import re
import tweepy


if __name__ == '__main__':
    db = mysql.connector.connect(host=config.db_host, user=config.db_user,
            password=config.db_pass, database=config.db_name)
    cursor = db.cursor()
    cursor.execute('''SELECT alpha, inf, ind_praes, ind_praet, konj_ii, imp,
            part_ii FROM mw_verb ORDER BY RAND() LIMIT 1''')
    row = cursor.fetchone()
    alpha, inf, ind_praes, ind_praet, konj_ii, imp, part_ii = row
    cursor.close()
    db.close()
    inf = inf.decode('utf-8')
    ind_praes = ind_praes.decode('utf-8')
    ind_praet = ind_praet.decode('utf-8')
    konj_ii = konj_ii.decode('utf-8')
    imp = imp.decode('utf-8')
    part_ii = part_ii.decode('utf-8')
    text = f'{inf} – {ind_praet} – {konj_ii} – {part_ii}'
    text += f' https://neutsch.org/Starke_Verben/{alpha}'
    client = tweepy.Client(
        bearer_token=config.bearer_token,
        consumer_key=config.consumer_key,
        consumer_secret=config.consumer_secret,
        access_token=config.access_token,
        access_token_secret=config.access_token_secret,
    )
    client.create_tweet(text=text)
