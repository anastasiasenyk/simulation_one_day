"""5 станів, між якими відбуваються переходи. Також повинно бути як мінімум 3 рандомні івенти"""
import random
import time
from actions import Events


def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class Simulation:
    def __init__(self):
        self.alive = True
        self.hour = 0
        self.energy = 65
        self.once_sport = False  # once for day
        self.once_friends = False  # once for day

        self.sleep = self._sleeping()
        self.study = self._studying()
        self.sport = self._do_sport()
        self.procrastination = self._procrastinating()
        self.friends = self._time_with_friends()

        self.tasks = []
        self.current_state = self.alive
        self.phrases = [False, False, False]

    def _user_interface(self, action, phrase=None):
        if self.hour > 24:
            self._end()
        elif self.alive:
            print(f'-> alive status: {str(self.alive)}, energy: {self.energy}%')
            print(f'-> time: {str(self.hour) if self.hour>=10 else "0"+ str(self.hour)}:00, '
                  f'action: {action}')
            if phrase:
                time.sleep(2)
                print(phrase)
                print()
            print()
            time.sleep(2)

    def start(self):
        unexpected_events = Events()
        while self.alive and self.hour <= 24:

            if random.randint(1, 5) == 1:
                unexpected_events.start().send(True)
                self.tasks.append(unexpected_events.current_event)
            self._choose_event()

            if len(self.tasks) > 1:
                if self.tasks[1] == self.study:
                    continue
                elif self.tasks[0] == unexpected_events.meet:
                    self.tasks = []
                    self.tasks.append(self._time_with_friends())
                    self.tasks.append(unexpected_events.meet)
                elif self.tasks[0] == unexpected_events.rain:
                    if self.tasks[1] != self.friends or self.tasks != self.sport:
                        self.tasks.pop()
                        self.tasks.append(random.choice([self._studying(), self._procrastinating()]))
                elif self.tasks[0] == unexpected_events.bombing:
                    self.tasks.pop()
                    self.tasks.pop().send(True)
                    print(f'-> time: {str(self.hour) if self.hour>=10 else "0"+ str(self.hour)}:00')
                    print()
                    self._change_time()
                else:
                    self.tasks.pop()

                while self.tasks:
                    self.tasks.pop().send(True)
            else:
                self.tasks.pop().send(True)
        return False

    def _choose_event(self):
        while True:
            number = random.randint(0, 10)
            if self.hour <= 4:
                if number <= 7 and self.energy <= 70:
                    return self.tasks.append(self._sleeping())
                elif number <= 9 and self.energy >= 35:
                    return self.tasks.append(self._studying())
                else:
                    return self.tasks.append(self._procrastinating())
            elif self.hour <= 9:
                if number <= 9:
                    return self.tasks.append(self._studying())
                else:
                    return self.tasks.append(self._procrastinating())
            elif self.hour <= 15:
                if number <= 3 and self.energy >= 20:
                    return self.tasks.append(self._studying())
                elif number <= 4:
                    return self.tasks.append(self._procrastinating())
                else:
                    if self.energy >= 80 and not self.once_friends:
                        return self.tasks.append(self._time_with_friends())
            elif self.hour <= 18:
                if number <= 5 and not self.once_sport:
                    return self.tasks.append(self._do_sport())
                elif number <= 7:
                    if self.energy >= 70 and not self.once_friends:
                        return self.tasks.append(self._time_with_friends())
                else:
                    return self.tasks.append(random.choice([self._studying(), self._procrastinating()]))
            elif self.hour <= 21:
                if number <= 8:
                    return self.tasks.append(self._studying())
                else:
                    return self.tasks.append(self._procrastinating())
            else:
                if number <= 7:
                    return self.tasks.append(self._studying())
                elif number <= 9:
                    return self.tasks.append(self._procrastinating())
                else:
                    return self.tasks.append(self._sleeping())

    @prime
    def _sleeping(self):
        while True:
            char = yield
            if char:
                self.sleep = True
                for index in range(random.randint(4, 9)):
                    self._user_interface('sleeping')
                    self._change_time()
                    self._change_energy(22)
                self.sleep = False
            else:
                break

    @prime
    def _studying(self):
        while True:
            char = yield
            if char:
                self._user_interface(random.choice([
                    'doing OP',
                    'coding this laboratory',
                    'meticulously studying a course from block «Svitohlyadne yadro»',
                    'studying',
                    'reading about CB-therapy',
                    'preparation for the exam',
                    'reading a book'
                ]))
                self._change_time()
                self._change_energy(-7)
            else:
                break

    @prime
    def _procrastinating(self):
        while True:
            char = yield
            if char:
                self._user_interface('procrastinating')
                self._change_time()
                self._change_energy(-3)
            else:
                break

    @prime
    def _do_sport(self):
        while True:
            char = yield
            if char:
                self.once_sport = True
                for index in range(random.randint(1, 2)):
                    self._user_interface('MMA time!!')
                    self._change_time()
                    self._change_energy(-15)
            else:
                break

    @prime
    def _time_with_friends(self):
        while True:
            char = yield
            if char:
                self.once_friends = True
                for index in range(random.randint(1, 2)):
                    self._user_interface('spending time with friends',
                                         'friends? finally' if self.phrases[1] else None)
                    self._change_time()
                    self._change_energy(-1)
            else:
                break

    def _change_time(self):
        if self.alive:
            self.hour += 1
            if self.hour >= 24:
                self._end()

    def _change_energy(self, number):
        if self.alive and self.energy >= 100 and number > 0:
            if not self.phrases[0]:
                self.phrases[0] = True
                print("Sleeping Beauty\n")
                time.sleep(2)
        else:
            self.energy += number
        if self.energy <= 0:
            self._end()
        elif self.energy > 100:
            self.energy = 100

    def _end(self):
        if self.alive:
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
            if self.energy <= 0:
                print('alive status: False')
                print('energy<0, ha-ha')
                print("You`re dead, luckily it was only a simulation...but..check it anyway")
            else:
                print(random.choice([
                    'Thank you for the day with me, but now I have a feeling that I am constantly watched ..',
                    'Was it fun? Anyway, I hope so',
                    'Bye!'
                    ]))
                print('-> New day <-')
            self.alive = False


if __name__ == '__main__':
    Simulation().start()
