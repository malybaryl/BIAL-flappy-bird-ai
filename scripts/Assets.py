import scripts.load as load

class Assets:
    """
    Singleton manager for loading and accessing game assets.

    Loads image resources for player, background, and pipe sprites on first
    instantiation and provides centralized access to these assets throughout
    the game.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of Assets and enforces the singleton pattern.

        This function is called when an instance of Assets is created. If the
        instance does not exist, it creates it. Otherwise, it returns the existing
        instance.

        Returns:
            Assets: The instance of Assets.
        """
        if cls._instance is None:
            cls._instance = super(Assets, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the Assets singleton.

        This function is called when an instance of Assets is created. If the
        instance does not exist, it creates it. Otherwise, it returns the existing
        instance.

        The assets are loaded from the assets/images directory and stored in the
        `assets` dictionary.

        The `assets` dictionary contains the following assets:
            - player: A list of images of the player.
            - background: A list of images of the background.
            - pipe: A list of images of the pipe.

        Returns:
            None
        """
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        
        self.assets = {
            'player': load.loadImages('player'),
            'background': load.loadImages('background'),
            'pipe': load.loadImages('pipe')
        }

