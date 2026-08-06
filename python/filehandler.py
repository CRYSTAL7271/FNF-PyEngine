import json, pickle, os, sys
from python.loghandle import LogHandler


class FileHandler:
    def loadJsonData(path):
        d = None
        with open(path, "r") as f:
            d = json.load(f)
        return d

    def findChar(string: str, letter: str):
        if len(list(letter)) > 1:
            LogHandler.printLog("Can't find more than one letter! >> Returning None")
            return None
        for c in string:
            if c == letter:
                return True
        return False

    def getFN(path: str):
        # gets filename from path, kind of stupid code but useful imo ^^ !
        # bro i'm getting crazy right here
        way = ""
        if FileHandler.findChar(path, "/"):
            way = "/"
        elif FileHandler.findChar(path, "\\"):
            way = "\\"
        else:
            LogHandler.printLog("Can't use a way to get FN.")
            return None

        name = ""
        for row in path.split(way):
            name = row

        return name
