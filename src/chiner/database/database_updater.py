import os
import sqlite3
import time

from src.chiner.database import DatabaseFormatter

class DatabaseUpdater():
    ANALYZERS = []
    ACCEPTED_FILETYPES = [".mp3", ".wav"]
    def __init__(self,
            db_name,
            db_path,
            music_folder):
        self.db_name = db_name
        self.db_path = db_path
        self.music_folder = music_folder
        self.db_fullpath = os.path.join(db_path, db_name) 
        self.db_con = sqlite3.connect(self.db_fullpath)
        self.db_cur = self.db_con.cursor()

        self.formatter = DatabaseFormatter() 

        if self._check_table_exist() is False:
            self._init_db()

    #TODO: Implement me
    def _check_table_exist(self):
        pass

    def _init_db(self):
        """ As of now, we'll create the table using a scheme
        but we can be much clever(er) by getting the return value
        (should be a dict with a metric_name: value)of each analyzer and 
        building a table using this
        """
        #TODO: Implement me 
        for table in self.formatter.get_insert_tables():
            self.db_cur.execute(table_command)

    def _check_filetype(self, song_filename):
        _, file_extension = os.path.splitext(song_filename)
        if file_extension in self.ACCEPTED_FILETYPES:
            return True 
        else:
            return False

    #TODO: Implement me
    def _check_analyzed(self, song_filename):
        pass
    
    def _write_to_analyzer_db(self, song_filename):
        values  = "'" + os.path.abspath(song_filename) + "'" 
        values += "'" + str(time.time()) + "'"
        self.db_cur.execute("INSERT INTO songs_to_analyze" + \
                "VALUES (" + values + ")") 

    def add_folder_filelist(self):
        """get all files in directory, check if they are of the correct
        filetype, check wether they are already analyzed, and update the db
        """
        #Should probably not be the job of db_updater to get list of file
        music_files = [os.path.join(path, name) for path, subdirs, files in \
            os.walk(self.music_folder) for name in files]
        for song in music_files:
            if self._check_filetype(song):
                self._write_to_analyzer_db(song)

    def _remove_song_filelist(self, song_filename):
        pass

    def get_song_to_analyze(self):
        song_filename = self.db_cur.execute('\
            SELECT * FROM songs_to_analyze ORDER BY date_added')

        while song_filename:
            yield song_filename.pop()

    def add_analyzed_song(self, analyzed_song):
        if validator.is_song_valid(analyzed_song) == True:
            self.db_cur.execute("INSERT INTO analyzed_songs" + \
                    "VALUES (" + values + ")") 

