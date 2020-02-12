from __future__ import annotations
import socket
from enum import Enum

"""
DingNet Communication Protocol
This is a simple protocol for Communication with the DingNet Server. Messages are send using Sockets
There are four client message types: INIT, ACTION, RESET, END
The server can answer with two different message types: OK, ERROR

The message occur in this sequence: INIT (ACTION* RESET)* END for the client.
The server answeres each message with either a OK or an ERROR message.

Each message begins with a '#' and ends with a '#'. Type definition ends with a ':'.
Data is separated by ','. The data is send as encoded strings.


In the following, the message types are described:

---     Client messages     ---

INIT: Initializes the Simulation and sends parameters to do so.
FORMAT: #INIT:<begin_tp>,<end_tp>,<begin_sf>,<end_sf>,<begin_sr>,<end_sr>#
EXAMPLE: #INIT:-160,-120,7,12,1,16#
The three intervals of parameters tp, sf and sr are defined as [begin_param (inclusive), end_param (exclusive) ).

ACTION: Steps the DingNet Simulation with the action specified by the payload
FORMAT: #ACTION:<tp>,<sf>,<sr>#
EXAMPLE: #ACTION:-160,7,1#

RESET: Reset the Environment. If successful, the DingNet Simulation is in the same state as after the initial INIT message
FORMAT: #RESET:#
EXAMPLE: #RESET:#

END: Ends the communication and closes the DingNet Simulation and the socket
FORMAT: #END:#
EXAMPLE: #END:#

---     Server messages     ---

OK: Command has been accepted and successfully executed. The new state is provided as payload
FORMAT: #OK:<mote_x>,<reward>?#
EXAMPLE: #OK:1424,0.523498657#

ERROR: Command could not be executed. The current state is provided as payload. Also an error message is provided as string
FORMAT: #ERROR:<mote_x>,<error_message>#
EXAMPLE: #ERROR:1224,"Interrupted by Signal SIGINT"#
"""

SYM_HEAD = '#'
SYM_TAIL = '#'


class DingNetMessage:

    _message_header = {
        1: "INIT:",
        2: "ACTION:",
        3: "RESET:",
        4: "END:",
        5: "OK:",
        6: "ERROR:",
    }

    class Type(Enum):
        INIT = 1
        ACTION = 2
        RESET = 3
        END = 4
        OK = 5
        ERROR = 6

    """
    Given the type and payload of the message, retuns the bytes to send to the stream
    """
    @staticmethod
    def encode(msg_type: Type, payload: str = "") -> str:
        return f"{SYM_HEAD}{DingNetMessage._message_header[msg_type]}{payload}{SYM_TAIL}".encode()

    """
    Decodes bytes of a message. Retuns the message type, the observation and the error if an error occured
    """
    @staticmethod
    def decode(message: str):
        msg_str = message.decode()
        error_msg = None
        assert msg_str[0] == '#' and msg_str[-1] == '#'
        [msg_type, payload] = message[1:-1].split(':')
        observation = Observation.from_payload(
            payload) if len(payload) > 0 else None
        return msg_type, observation, error_msg


class Action:

    @staticmethod
    def from_payload(payload: str):
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

    def to_payload(self) -> str:
        return f"{self.xpos},{self.reward}"


class DingNetConnection():

    def __init__(self, host="localhost", port="9002"):
        self._host = host
        self._port = port
        self.socket = socket.socket()

    def connect(self):
        successful = False
        self.socket.connect((self._host, self._port))
        return successful

    def init_env(self, range_str: str):
        self.socket.send(DingNetMessage.encode(
            DingNetMessage.Type.INIT, range_str
        ))

    def send_action(self, action: Action):
        self.socket.send(DingNetMessage.encode(
            DingNetMessage.Type.ACTION, action.to_payload()
        ))

    def reset(self):
        self.socket.send(DingNetMessage.encode(
            DingNetMessage.Type.RESET
        ))

    def get_observation(self) -> Observation:
        message = self.socket.recv()
        msg_type, observation, error = DingNetMessage.decode(message)
        if msg_type == DingNetMessage.Type.ERROR:
            print(error)
            return None
        elif msg_type == DingNetMessage.Type.OK:
            return observation
        else:
            raise Exception("DingNet Protocoal Violation")

    def close(self):
        self.socket.send(DingNetMessage.encode(
            DingNetMessage.Type.END
        ))
        self.socket.close()

