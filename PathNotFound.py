class PathNotFound(Exception):
    def __init__(self, message="There is no valid path in this map "):
        self.message = message
        super().__init__(self.message)
