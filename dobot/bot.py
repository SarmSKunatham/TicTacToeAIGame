from pydobot import Dobot

import os
import pickle
from typing import Optional
from .types.dobot_position import DobotPosition
from .utils.ports import get_port


class Bot:
    def __init__(self, port=None, board_size=120, rise_height=50):
        self.port = get_port(port)
        self.bot = Dobot(self.port)
        self.board_size = board_size
        self.bot.speed(150, 150)
        self.rise_height = rise_height
        self.initial_position: Optional[DobotPosition] = self.__load_marker_position("initial")
        self.black_position: Optional[DobotPosition] = self.__load_marker_position("black")
        self.red_position: Optional[DobotPosition] = self.__load_marker_position("red")

    def __move_to(self, pos: DobotPosition):
        x = pos.x if pos.x is not None else self.bot.pose()[0]
        y = pos.y if pos.y is not None else self.bot.pose()[1]
        z = pos.z if pos.z is not None else self.bot.pose()[2]
        r = pos.r if pos.r is not None else self.bot.pose()[3]
        self.bot.move_to(x, y, z, r, wait=True)

    def __suck(self, suck: bool):
        self.bot.suck(suck)

    def __move_to_number(self, number: int):
        if not (1 <= number <= 9):
            raise Exception(f'Number must be between 1 and 9, got {number}')
        if self.initial_position is None:
            raise Exception('Initial position is not set')
        x = self.initial_position.x + ((number - 1) % 3) * self.board_size // 3
        y = self.initial_position.y - ((number - 1) // 3) * self.board_size // 3
        self.__move_to(DobotPosition(z=self.initial_position.z))
        self.__move_to(DobotPosition(x=x, y=y, z=self.initial_position.z))
        self.__move_to(DobotPosition(x=x, y=y))

    def __pick_up(self):
        current_z = self.bot.pose()[2]
        self.__move_to(DobotPosition(z=current_z - self.rise_height))
        self.__suck(True)
        self.__move_to(DobotPosition(z=current_z))

    def __put_down(self):
        current_z = self.bot.pose()[2]
        self.__move_to(DobotPosition(z=current_z - self.rise_height))
        self.__suck(False)
        self.__move_to(DobotPosition(z=current_z))

    def set_marker_position(self, marker: str):
        if (marker != "red") and (marker != "black") and (marker != "initial"):
            raise Exception(f'Marker must be either "red" or "black", got {marker}')
        (x, y, z, r, _, _, _, _) = self.bot.pose()
        pickle.dump(DobotPosition(x=x, y=y, z=z + self.rise_height, r=r), open(f"{os.path.abspath('dobot')}/positions/{marker}.p", "wb"))
        print(f"Marker position for {marker} set to {x}, {y}, {z}, {r}")

    def __load_marker_position(self, marker: str) -> Optional[DobotPosition]:
        if (marker != "red") and (marker != "black") and (marker != "initial"):
            raise Exception(f'Marker must be either "red" or "black", got {marker}')
        marker_path = f"{os.path.abspath('dobot')}/positions/{marker}.p"
        if os.path.isfile(marker_path):
            return pickle.load(open(marker_path, "rb"))
        print(f"WARNING: No marker position for {marker} found")
        return None

    def move_marker_to(self, marker: str, number: int):
        if self.initial_position is None:
            raise Exception('Initial position is not set')
        if self.red_position is None:
            raise Exception('Red position is not set')
        if self.black_position is None:
            raise Exception('Black position is not set')

        marker_pos = self.red_position if marker == "red" else self.black_position

        self.__move_to(marker_pos)
        self.__pick_up()
        self.__move_to_number(number)
        self.__put_down()
