import json 

from chiner.analyzers import ANALYZER_DICT

class ChinerPipeline():
    #Class responsible for instanciating all analyzer and running them

    def __init__(self,
            config_filename,
            analyzers,
            db_updater):
        super().__init__()
        with open(config_filename, 'r') as fi:
            self.config = json.loads(fi)

    def _add_analyzers_from_config(self, config):
        analyzer_list = []
        for analyzer in config['analyzers']:
            analyzer_list.append(
                    ANALYZER_DICT[analyzer['class']].from_config(analyzer))

    @classmethod
    def from_config(cls, config_filename):
        with open(config_filename, 'r') as fi:
            config = json.loads(fi)
        analyzers = _add_analyzers_from_config(config)
        db_updater = DatabaseFormatter.from_config(config['database'])

    def update():
        #TODO: Check if last check has been done in the past week
        #songs_to_analyze should be a generator that delete the song
        #each time its been passed
        for song in db_updater.get_songs_to_analyze():
        for analyzer in self.analyzers:
            analyzers.run(song)
