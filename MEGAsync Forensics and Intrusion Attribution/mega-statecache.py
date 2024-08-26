#!/usr/bin/env python

import sqlite3
from argparse import ArgumentParser
from datetime import datetime
from urllib.parse import quote_plus

__author__ = "Maxime Thiebaut (0xThiebaut)"
__license__ = "EUPL-1.2"

class Nodes:
    def __init__(self, path) -> None:
        con = sqlite3.connect(f"file:{quote_plus(path)}?mode=ro", uri=True)
        cur = con.cursor()
        self.__nodes = {}
        for (nodehandle, parenthandle, name, size, ctime, mtime, kind) in cur.execute("SELECT nodehandle, parenthandle, name, size, ctime, mtime, type FROM nodes;"):
            self.__nodes[nodehandle] = {'parenthandle': parenthandle, 'name': name, 'size': size, 'ctime': ctime, 'mtime': mtime, 'type': kind}
        cur.close()
        con.close()

    def __resolve(self, nodehandle, depth=0) -> str:
        node = self.__nodes.get(nodehandle, {})
        parenthandle=node.get('parenthandle', -1)
        name=node.get('name')
        kind=node.get('type', -1)
        if kind == 2:
            name = "ROOT"
        elif kind == 3:
            name = "VAULT"
        elif kind == 4:
            name = "RUBBISH"


        parent = ""
        if parenthandle != -1:
            parent = self.__resolve(parenthandle, depth+1)

        if depth == 0:
            mtime = node.get('mtime', 0)
            if mtime == 0:
                mtime = node.get('ctime', 0)
            name = f"{name} ({datetime.fromtimestamp(mtime, tz=None)})"

        return f"{parent}/{name}"
    
    def files(self):
        files = []
        for nodehandle in self.__nodes.keys():
            files.append(self.__resolve(nodehandle))
        files.sort()
        return files
    
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    nodes = Nodes(args.filename)
    for node in nodes.files():
        print(node.encode('unicode-escape').decode('ascii'))
