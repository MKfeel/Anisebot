from pathlib import Path
from typing import Optional, Callable

import toml
from pygtrie import CharTrie, Trie
from pypinyin import lazy_pinyin
from fuzzywuzzy import process

from ..config import RES_PATH
from ..object import GameObject
class AliasManager:
    def __init__(self):
        self.alias2obj: CharTrie[str, GameObject] = CharTrie()
        self.pyalias2obj: Trie[str, GameObject] = Trie(separator='-')


    def init_from_toml(self, path: Path, obj_getter: Callable[[str], GameObject]):
        if not path.exists():
            path.mkdir(parents=True)
            path.write_text(toml.dumps({}))
        d: dict = toml.load(path.read_text('utf-8'))
        for id_, names in d.items():
            for n in names:
                if n in self.alias2obj:
                    continue
                self.alias2obj[n] = obj_getter(id_)

    def init(self):
        self.init_from_toml(RES_PATH / 'alias' / 'character.toml', lambda x: characters.get())
        self.init_from_toml(RES_PATH / 'alias' / 'equipment.toml', lambda x: equipments.get())

    def get_obj(self, s: str) -> Optional[GameObject]:
        return self.alias2obj.get(s)

    def add(self, alias: str, obj: GameObject):
        self.alias2obj[alias] = obj
        self.pyalias2obj['-'.join(lazy_pinyin(alias))] = obj

    def clear(self):
        self.alias2obj.clear()
        self.pyalias2obj.clear()

    def guess(self, s: str) -> Optional[GameObject]:
        name, score = process.extract(s, self.alias2obj.keys())
        if score >= 60:
            return self.alias2obj[name]
        return None
        # if s in self.alias2obj:
        #     return self.get_obj(s)
        # else:
        #     for i in reversed(range(len(s))):
        #         self.alias2obj.items(prefix='')

if __name__ == '__main__':
    print('aa')