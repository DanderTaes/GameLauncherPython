class Game:
    def __init__(self, name: str, path: str, image_path: str, type: int = 0):
        self.name = name
        self.path = path
        self.image_path = image_path
        self.type = type # 0 for steam, 1 for exe, 2 for other