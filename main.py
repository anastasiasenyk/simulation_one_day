"""5 станів, між якими відбуваються переходи. Також повинно бути як мінімум 3 рандомні івенти"""
import random


class Simulation:
    def __init__(self):
        self.alive = True
        self.hour = 0
        self.energy = 65

        self.sleep = False
        self.study = False
        self.sport = False
        self.procrastination = False
        self.friends = False

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
                print(phrase)
                print()
            print()
            # time.sleep(1)

    def start(self):
        while self.alive and self.hour <= 24:
            self._choose_event()
        return False

    def _choose_event(self):
        while True:
            number = random.randint(0, 10)
            if self.hour <= 4:
                if number <= 7 and self.energy <= 50:
                    return self._sleeping()
                elif number <= 9 and self.energy >= 35:
                    return self._studying()
                else:
                    return self._procrastinating()
            elif self.hour <= 9:
                if number <= 5:
                    return self._studying()
                else:
                    return self._procrastinating()
            elif self.hour <= 15:
                if number <= 3 and self.energy >= 20:
                    return self._studying()
                elif number <= 5:
                    return self._procrastinating()
                else:
                    if self.energy >= 80 and not self.friends:
                        return self._time_with_friends()
            elif self.hour <= 18:
                if number <= 5 and not self.sport:
                    return self._do_sport()
                elif number <= 7:
                    if self.energy >= 70 and not self.friends:
                        return self._time_with_friends()
                else:
                    return random.choice([self._studying(), self._procrastinating()])
            elif self.hour <= 21:
                if number <= 8:
                    return self._studying()
                else:
                    return self._procrastinating()
            else:
                if number <= 7:
                    return self._studying()
                elif number <= 9:
                    return self._procrastinating()
                else:
                    return self._sleeping()

    def _sleeping(self):
        self.sleep = True
        for index in range(random.randint(4, 9)):
            self._user_interface('sleeping')
            self._change_time()
            self._change_energy(22)
        self.sleep = False

    def _studying(self):
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

    def _procrastinating(self):
        self._user_interface('procrastinating')
        self._change_time()
        self._change_energy(-3)

    def _do_sport(self):
        self.sport = True
        for index in range(random.randint(1, 2)):
            self._user_interface('MMA time!!')
            self._change_time()
            self._change_energy(-15)

    def _time_with_friends(self):
        self.friends = True
        for index in range(random.randint(2, 3)):
            self._user_interface('spending time with friends', 'friends? finally' if self.phrases[1] else None)
            self._change_time()
            self._change_energy(-1)

    def _change_time(self):
        if self.alive:
            self.hour += 1
            if self.hour >= 24:
                self._end()

    def _change_energy(self, number):
        if self.alive and self.energy >= 100 and number > 0:
            if not self.phrases[0]:
                self.phrases[0] = True
                print('you will soon explode from that energy, be calmer')
                print()
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
