"""基站模拟器"""

from tlv_codec import TLVCodec
from nested_tlv_codec import NestedTLVCodec
import messages


class BaseStation:
    """基站类"""

    def __init__(self):
        self.connected = False
        self.codec = TLVCodec()
        self.nested_codec = NestedTLVCodec()

    def receive(self, data: bytes) -> bytes | None:
        """接收并处理手机发来的消息"""
        msg_type, value = self.codec.decode(data)
        print(f"  [基站] 收到消息: {messages.get_msg_name(msg_type)}, value={value.hex()}")

        if msg_type == messages.MSG_ATTACH_REQUEST:
            self.connected = True
            # 解析嵌套的CapabilityInfo
            nested_items = self.nested_codec.decode_nested(value)
            self._print_nested_structure(nested_items, indent=4)
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

    def _print_nested_structure(self, items: list, indent: int = 4):
        """打印嵌套TLV结构"""
        prefix = " " * indent
        for tag, value in items:
            name = messages.get_msg_name(tag)
            if isinstance(value, list):
                print(f"{prefix}├── {name}:")
                self._print_nested_structure(value, indent + 4)
            else:
                # 检查是否为可打印ASCII
                if all(0x20 <= b < 0x7f for b in value):
                    print(f"{prefix}├── {name}: {value.decode('ascii')}")
                else:
                    print(f"{prefix}├── {name}: 0x{value.hex()}")

