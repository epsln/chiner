class MusicAnalyzer():
    _FEATURE_NAME = str
    def __init__(self, feature_name):
        super().__init__()

    def _preprocess(self, song):
        return song

    def _analyze(self, preprocessed):
        return None
    
    def _postprocess(self, analyzed):
        return {self._FEATURE_NAME, analyzed}
        
    def process(self, song, meta):
        preprocessed = self._preprocess(song)
        analyzed = self._analyze(preprocessed)
        postproc = self._postprocess(analyzed)
        
        return postproc


