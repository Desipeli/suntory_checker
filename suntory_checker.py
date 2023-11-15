from logger import Logger
import requests
import re
import json


class SuntoryChecker:
    def __init__(self, logger: "Logger", event_dates, url_list, url):
        self.session = requests.Session()
        self.logger = logger
        self.event_dates = event_dates
        self.url_list = url_list
        self.url = url

    def check_tour(self):
        # Get cookie, does not work without
        self.session.get(self.url_list, allow_redirects=True)

        the_page = self.session.get(self.url, allow_redirects=True)

        match = re.search(r'var\s+seminars\s*=\s*(\[{.*}\])', the_page.text)

        if match:
            seminars_json = match.group(1)
            seminars_list = json.loads(seminars_json)

        for seminar in seminars_list:
            event_date = seminar["eventDate"]
            if event_date in self.event_dates:
                self.logger.log(f"Event date found: {event_date}")
                return True

        self.logger.log("Didn't find valid dates")
        return False

    def set_event_dates(self, dates: list):
        self.event_dates.clear()

        try:
            for date in dates:
                self.event_dates.append(date)
        except Exception as error:
            self.logger.error(error)

    def get_dates(self):
        return self.event_dates
