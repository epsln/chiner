import os

import configparser
import sqlite3

from chiner.analyzers import EmbedderAnalyzer

def main():
    config = configparser.ConfigParser()
    config.read(r'config.cfg')
    db_loc = os.path.join(config['database']['path'], config['database']['name'])
    db_con = sqlite3.connect(db_loc)
    db_cur = db_con.cursor()

    embedder = EmbedderAnalyzer.from_config(config)

    music_files = [os.path.join(path, name) for path, subdirs, files in \
            os.walk(config['search_dir']['path']) for name in files]

    if not os.path.isfile(db_loc):
        db_cur.execute('''CREATE TABLE songs
            (path text, embed text)''')

    for i, song in enumerate(music_files):
        embed = embedder.process(song)
        
        values  = "'" + os.path.abspath(song) + "'" 
        values += "'" + embed + "'"
        db_cur.execute("INSERT INTO songs" + \
                "VALUES (" + values + ")") 


if __name__ == "__main__":
    main()
