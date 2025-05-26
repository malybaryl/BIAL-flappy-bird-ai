import scripts.load as load

class Assets:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Assets, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        
        self.assets = {
            'player': load.loadImages('player'),
            'background': load.loadImages('background'),
            'pipe': load.loadImages('pipe')
        }

