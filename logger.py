import datetime


class Logger:
    def __init__(self):
        self.log("Logger created")

    def log(self, msg):
        print(f"{datetime.datetime.now()} - {msg}")

    def error(self, msg):
        print(f"{datetime.datetime.now()} - ERROR - {msg}")
