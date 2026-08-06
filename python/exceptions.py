import os, sys


class NoMonitorFound(Exception):
    def __init__(self):
        super().__init__(
            "No monitors found which means that a virus blocker is not giving access or this computer doesn't run with a monitor!"
        )
