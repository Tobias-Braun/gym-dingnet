from __future__ import annotations
from typing import List
import sys
import socket
import os
from enum import Enum
from time import sleep

"""
DingNet Communication Protocol
This is a simple protocol for Communication with the DingNet Server. Messages are send using stdin and stdout
There are four client message types: INIT, ACTION, RESET, END
The server can answer with two different message types: OK, ERROR

The message occur in this sequence: INIT (ACTION* RESET)* END for the client.
The server answeres each message with either a OK or an ERROR message.

Each message begins with a '#' and ends with a '#'. Type definition ends with a ':'.
Data is separated by ','. The data is send as encoded strings.


In the following, the message types are described:

---     Client messages     ---

ACTION: Steps the DingNet Simulation with the action specified by the payload
FORMAT: ACTION:<tp>,<sf>,<sr>
EXAMPLE: ACTION:-160,7,1

RESET: Reset the Environment. If successful, the DingNet Simulation is in the same state as after the initial INIT message
FORMAT: RESET:
EXAMPLE: RESET:

END: Ends the communication and closes the DingNet Simulation
FORMAT: END:
EXAMPLE: END:

---     Server messages     ---

OK: Command has been accepted and successfully executed. The new state is provided as payload
FORMAT: OK:<mote_x>,<reward>
EXAMPLE: "0K:200,0.43545"
"""

SYM_HEAD = '#'
SYM_TAIL = '#'
BUFFER_SIZE = 1000


class Configuration:

    def __init__(self, tp_begin, tp_end, sf_begin, sf_end, sr_begin, sr_end):
        self.range = [tp_begin, tp_end, sf_begin, sf_end, sr_begin, sf_end]


class DingNetMessage:

    class Type(Enum):
        INIT = 1
        ACTION = 2
        RESET = 3
        END = 4
        OK = 5
        ERROR = 6

    _message_header = {
        Type.INIT: "INIT:",
        Type.ACTION: "ACTION:",
        Type.RESET: "RESET:",
        Type.END: "END:",
        Type.OK: "OK:",
        Type.ERROR: "ERROR:",
    }

    """
    Given the type and payload of the message, retuns the bytes to send to the stream
    """
    @staticmethod
    def encode(msg_type: Type, payload: str = "") -> str:
        return f"{DingNetMessage._message_header[msg_type]}{payload}\n"

    """
    Decodes bytes of a message. Retuns the message type, the observation and the error if an error occured
    """
    @staticmethod
    def decode(message: str):
        msg_str = message
        error_msg = None
        [msg_type, payload] = msg_str[:-1].split(':')
        if msg_type != 'ERROR':
            observation = Observation.from_payload(payload)
        else:
            error_payload = payload.split(',')
            observation = Observation.from_payload(error_payload[0] + ',0')
            error_msg = error_payload[1]
        return msg_type, observation, error_msg


class Action:

    @staticmethod
    def from_payload(payload: str):
        if not payload:
            return None
        params = payload.split(',')
        return Action(int(params[0]), int(params[1]), int(params[2]))

    def __init__(self, tp: int, sf: int, sr: int):
        self.tp = tp
        self.sf = sf
        self.sr = sr

    def to_payload(self) -> str:
        return f"{self.tp},{self.sf},{self.sr}"


class Observation:

    @staticmethod
    def from_payload(payload: str) -> Observation:
        params = payload.split(',')
        return Observation(int(params[0]), float(params[1]))

    def __init__(self, xpos, reward):
        self.xpos = xpos
        self.reward = reward

    def __eq__(self, other):
        return self.xpos == other.xpos and self.reward == other.reward

    def to_payload(self) -> str:
        return f"{self.xpos},{self.reward}"


class DingNetConnection():

    def __init__(self, host="localhost", port=9002):
        self._host = host
        self._port = port
        self._out = open("/Users/tobiasbraun/dingnet_in", "w")
        self._in = open("/Users/tobiasbraun/dingnet_out", "r")

    def send_action(self, action: Action):
        self._out.write(DingNetMessage.encode(
            DingNetMessage.Type.ACTION, action.to_payload()
        ))
        self._out.flush()

    def reset(self):
        self._out.write(DingNetMessage.encode(
            DingNetMessage.Type.RESET, payload="----"
        ))
        self._out.flush()

    def get_observation(self) -> Observation:
        message = None
        while message is None or message == "" or message == "\n":
            sleep(0.01)
            message = self._in.readline()
        msg_type, observation, error = DingNetMessage.decode(message)
        if msg_type == "ERROR":
            print(error)
            return None
        elif msg_type == "OK":
            return observation
        else:
            raise Exception("DingNet Protocoal Violation")

    def __del__(self):
        try:
            self._out.close()
            self._in.close()
        except:
            print("could not close streams")
