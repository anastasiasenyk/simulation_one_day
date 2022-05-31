import random, time


def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class Events:
    def __init__(self):
        self.rain = self.raining()
        self.meet = self.new_meeting()
        self.bombing = self.bomb_attack()

        self.current_event = self.start()
        self.stopped = False

    def send(self, char):
        try:
            self.current_event.send(char)
        except StopIteration:
            self.stopped = True

    @prime
    def start(self):
        while True:
            char = yield
            if char:
                self.current_event = random.choice([
                    self.rain,
                    self.meet,
                    self.bombing
                ])
            else:
                break

    @prime
    def raining(self):
        while True:
            char = yield
            if char:
                self.current_event = self.rain
                print("It's raining, but I don't have an umbrella. Well, then I will stay at home\n")
                time.sleep(2)
            else:
                break

    @prime
    def new_meeting(self):
        while True:
            char = yield
            if char:
                self.current_event = self.meet
                print("A new unexpected meeting! The following plans are canceled!\n")
                time.sleep(2)
            else:
                break

    @prime
    def bomb_attack(self):
        while True:
            char = yield
            if char:
                self.current_event = self.bombing
                print("There was news that our city is under bomb attack, now I definitely need to go to shelter.\n"
                      "Don't neglect air alarms!\n")
                time.sleep(2)
            else:
                break
