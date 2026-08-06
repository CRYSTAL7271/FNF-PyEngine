import os, sys, pickle, json
from python.loghandle import LogHandler


class ChartHandler:
    def listSongs():
        songs = {}
        for f in os.listdir("assets//songs"):
            songs.update({f: {"Difficulties": []}})
            for difficulty in os.listdir(f"assets//songs//{f}//data"):
                diff = difficulty.split("-")[1]
                songs[f]["Difficulties"].append(diff)

        return songs

    def canBePlayed(name):
        try:
            if name.split(".")[1] == "ogg":
                LogHandler.printLog(f"{name} can be played!")
                return True
            else:
                LogHandler.printLog(f"{name} can't be played!")
                return False
        except IndexError:
            LogHandler.printLog(f"{name} can't be played!")
            return False

    def getSongDirectory(songname):
        found = False
        songname = songname.lower()
        for f in os.listdir("assets//songs"):
            if f == songname:
                found = True
                break
        if not found:
            LogHandler.printWarning(f"Song {songname} not found.")
            return None
        return os.path.join("assets", "songs", songname)

    def loadChart(fn):
        difficulty = None
        song = None
        rsong = None
        LogHandler.printLog(f"Loading song: {fn}")
        if fn.isupper():
            LogHandler.printWarning("Chart is not lowercase! Can't continue loading!")
            return None
        found = False
        for song in os.listdir("assets//songs"):
            LogHandler.printLog(f"Checking: assets//songs//{song}")
            if found:
                break
            for difficulty in os.listdir(f"assets//songs//{song}//data"):
                LogHandler.printLog(
                    f"Checking: assets//songs//{song}//data//{difficulty}"
                )
                if difficulty == fn:
                    LogHandler.printLog(
                        f"Found requested difficulty and chart: {difficulty}"
                    )
                    found = True
                    fsong = song
                    break

        if not found:
            LogHandler.printWarning(
                f"vvv Song {fn.split('-')[0]} can't be loaded >> {fn} not found! vvv\nMaybe the chart file is not actually lowercase?"
            )
            return None
        rsong = f"assets//songs//{fsong}//data//{difficulty}"
        chart = {}
        with open(rsong) as chart_file:
            chart = json.load(chart_file)
        LogHandler.printLog("Got file >> getting to work to return value!!")

        return chart
