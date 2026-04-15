"""基站模拟器"""

from tlv_codec import TLVCodec
import messages

class BaseStation:
    """基站类"""

    def __init__(self):
        self.connected = False
        self.codec = TLVCodec()

    def receive(self, data: bytes) -> bytes | None:
        """接收并处理手机发来的消息"""
        msg_type, value = self.codec.decode(data)
        print(f"  [基站] 收到消息: {messages.get_msg_name(msg_type)}, value={value.hex()}")

        if msg_type == messages.MSG_ATTACH_REQUEST:
            self.connected = True
            response = self.codec.encode(messages.MSG_ATTACH_ACCEPT, b'\x00\x01')
            print(f"  [基站] 发送: AttachAccept")
            return response

        elif msg_type == messages.MSG_ATTACH_COMPLETE:
            print(f"  [基站] 附着完成，状态: connected={self.connected}")
            return None

        elif msg_type == messages.MSG_DATA_UPLINK:
            response = self.codec.encode(messages.MSG_DATA_DOWNLINK, value)
            print(f"  [基站] 发送: DataDownlink, 数据={value.hex()}")
            return response

        elif msg_type == messages.MSG_DETACH_REQUEST:
            self.connected = False
            response = self.codec.encode(messages.MSG_DETACH_ACCEPT, b'\x00\x00')
            print(f"  [基站] 发送: DetachAccept, 状态: connected={self.connected}")
            return response

        return None
