from datetime import time

class Market:
    def __init__(self, id, market_name, location, time_open, time_close, timezone):
        self.id = id
        self.market_name = market_name
        self.location = location
        self.time_open = time_open
        self.time_close = time_close
        self.timezone = timezone

    def is_open(self, current_time):
        return self.time_open <= current_time <= self.time_close

    def display_info(self):
        print(f"Market ID: {self.id}")
        print(f"Market Name: {self.market_name}")
        print(f"Location: {self.location}")
        print(f"Time Open: {self.time_open.strftime('%H:%M')} {self.timezone}")
        print(f"Time Close: {self.time_close.strftime('%H:%M')} {self.timezone}")
        print(f"Timezone: {self.timezone}")

