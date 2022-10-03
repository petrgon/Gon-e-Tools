from random import randint
from multiprocessing import Process, Queue

from window import Window

NAME = "Mugwungs"

class State:
    mugwungs = []

class Mugwungs:
    _state = State()
    _window: Window = None

    def __init__(self, director):
        self._window = director._window
        self._window.Register(NAME, self.exec)

    def getNumberOfMugwungs(self):
        while True:
            numberOfMugwungs = input(f'How many {NAME} you want to look for? ')
            numberOfMugwungs = numberOfMugwungs.replace(" ", "")
            if(numberOfMugwungs.isnumeric() and int(numberOfMugwungs) > 0):
                return int(numberOfMugwungs)

    def initMugwungs(self, numberOfMugwungs):
        self._state.mugwungs = []
        for x in range(numberOfMugwungs):
            self._state.mugwungs.append([randint(0, 9),  randint(0, 9)])

    def waitForNextGame(self):
        while True:
            anotherGame = input('Another game? [Y/n] ')
            if anotherGame in ['n', 'N']:
                quit()
            if anotherGame in ['Y', '', 'y']:
                break

    def getDistance(self, coordArr):
        # Get distances
        shortestRange = 100
        for x in range(len(self._state.mugwungs)):
            mugwungCoord = self._state.mugwungs[x]
            if mugwungCoord[0] == coordArr[0] and mugwungCoord[1] == coordArr[1]:
                self._state.mugwungs.pop(x)
                shortestRange = 0
                break
            else:
                distance = abs(mugwungCoord[0] - coordArr[0]) + abs(mugwungCoord[1] - coordArr[1])
                if distance < shortestRange:
                    shortestRange = distance
        return shortestRange

    def update(self):
        print(f"Welcome to {NAME}. In this game you need to find coords of hidden {NAME}.\n")
        numberOfMugwungs = self.getNumberOfMugwungs()
        self.initMugwungs(numberOfMugwungs)
        print(f"\nTo find a {NAME} just type two numbers in range 0-9. Try it now!")

        numberOfAttempts = 0
        # game loop
        while len(self._state.mugwungs) > 0:
            coordStr = input(f'Where is {NAME}? ')
            numberOfAttempts += 1
            coordStr = coordStr.replace(" ", "")
            if len(coordStr) < 2 or not coordStr.isnumeric():
                continue

            coordArr = [int(x) for x in str(coordStr)]
            shortestRange = self.getDistance(coordArr)

            if shortestRange == 0:
                print(f"Found it! {len(self._state.mugwungs)} left.")
            else:
                print(f"You are {shortestRange} away")
        
        print(f"You found them all in {numberOfAttempts} attempts! Congrats!")
        
        self.waitForNextGame()

    def exec(self):
        p = Process(target=self._exec, args=(self,))
        p.start()
        p.join()

    def _exec(self):
        # main loop
        while True:
            self.update()