from gym_dingnet.envs.protocol import *

INIT_MSG = "#INIT:-160,-120,7,12,1,16#"
ACTION_MSG = "#ACTION:-140,8,14#"
RESET_MSG = "#RESET:#"
END_MSG = "#END:#"

OK_MSG = "#OK:1444,0.348#"
ERROR_MSG = "#ERROR:1220,This did not work#"


class mock_sender:

    def __init__(self):
        self.last_send = None
        self.connected = False
        self.messages = [OK_MSG, ERROR_MSG]

    def connect(self, location):
        self.connected = True

    def close(self):
        self.connected = False

    def recv(self):
        return self.messages.pop()

    def send(self, bytes: bytes):
        self.last_send = bytes.decode()


mock_sender = mock_sender()
connection = DingNetConnection(senddevice=mock_sender)


def test_encode_should_create_bytes():
    assert INIT_MSG == DingNetMessage.encode(
        DingNetMessage.Type.INIT, '-160,-120,7,12,1,16').decode()
    assert ACTION_MSG == DingNetMessage.encode(
        DingNetMessage.Type.ACTION, '-140,8,14').decode()
    assert RESET_MSG == DingNetMessage.encode(
        DingNetMessage.Type.RESET, '').decode()
    assert END_MSG == DingNetMessage.encode(
        DingNetMessage.Type.END, '').decode()


def test_decode_should_provide_information():
    t, o, e = DingNetMessage.decode(OK_MSG.encode())
    assert t == DingNetMessage._message_header[DingNetMessage.Type.OK][:-1]
    assert o == Observation(1444, 0.348)
    assert e == None

    t, o, e = DingNetMessage.decode(ERROR_MSG.encode())
    assert t == DingNetMessage._message_header[DingNetMessage.Type.ERROR][:-1]
    assert o == Observation(1220, 0)
    assert e == "This did not work"


def test_should_connect():
    connection.connect()
    assert mock_sender.connected == True


def test_should_init_env():
    connection.init_env([-160, -120, 7, 12, 1, 16])
    assert mock_sender.last_send == INIT_MSG


def test_should_send_action():
    action = Action(-140, 8, 14)
    connection.send_action(action)
    assert mock_sender.last_send == ACTION_MSG


def test_should_reset():
    connection.reset()


def test_should_close():
    connection.close()
    assert mock_sender.connected == False
