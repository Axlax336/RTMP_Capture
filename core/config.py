import configparser
from pathlib import Path


instanct = None


def getInstance():
    global instanct
    if not isinstance(instanct, Config):
        instanct = Config()
    return instanct


class Config:
    def __init__(self, path: str = "config.ini"):
        path_search_order = (
            Path(path),
            Path.cwd() / "config.ini",
        )
        ini_path = None
        for p in path_search_order:
            if p.is_file():
                ini_path = p.resolve()
                break
        if ini_path:
            print(f"find config.ini at {ini_path}")
            self.conf = configparser.ConfigParser()
            self.ini_path = ini_path
            self.conf.read(ini_path, encoding="utf-8-sig")
        else:
            print("config.ini not found")

    def get_player_path(self):
        return self.conf.get('main', 'player_path')

    def get_cmd_template(self):
        return self.conf.get('main', 'cmd_template')


