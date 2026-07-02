


class Game:
    def __init__(self, name: str, path: str, image_path: str, type: int = 0):
        self.name = name
        self.path = path
        self.image_path = image_path
        self.type = type # 0 for steam, 1 for exe, 2 for other
    
    def to_json(self):
        return {
            "name": self.name,
            "path": self.path,
            "image_path": self.image_path,
            "type": self.type
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            image_path=data.get("image_path", ""),
            type=data.get("type", 0)
        )