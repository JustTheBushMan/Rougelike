class EventHandler:
    EVENT_STORAGE = 10
    def __init__(self):
        self.tick = 0
        self.events = {}
    def advanceTick(self):
        self.tick += 1
        del self.events[self.tick-10]

eventHandler = EventHandler()
