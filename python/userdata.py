import os, sys, pickle, json
from python.loghandle import LogHandler


class DataHandler:
    fn = "assets//userdata.pkl"

    def __check_data__():
        if not os.path.exists(DataHandler.fn):
            LogHandler.printWarning("Not found userdata.pkl, creating new one..")
            with open(DataHandler.fn, "wb") as f:
                pickle.dump(
                    {
                        "VSync": 1,
                        "FrameLimit": 120,
                        "GameKeys": {"left": "d", "down": "f", "up": "j", "right": "k"},
                        "TickingSound": False,
                        "AltKeys": {
                            "left": "left",
                            "down": "down",
                            "up": "up",
                            "right": "right",
                        },
                        "Debug": True,
                        "KeyOffset": 120,
                    },
                    f,
                )
            LogHandler.printLog("Successfully saved userdata.pkl !")

    def saveProperty(key, value):
        data = None
        with open(DataHandler.fn, "rb") as f:
            data = pickle.load(f)
        if not data:
            raise Exception(
                "'data' variable couldn't be loaded >> userdata.pkl was not probably found."
            )
        data.update({key: value})
        with open(DataHandler.fn, "wb") as f:
            pickle.dump(data, f)

        LogHandler.printLog("Successfully saved userdata.pkl !")

    def getProperty(key):
        data = None
        with open(DataHandler.fn, "rb") as f:
            data = pickle.load(f)

        if not data:
            raise Exception(
                "'data' variable couldn't be loaded >> userdata.pkl was not probably found."
            )
        if key in data:
            return data[key]
        else:
            LogHandler.printWarning("getProperty >> Needed key not found.")
