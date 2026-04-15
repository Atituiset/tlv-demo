"""手机模拟器"""

from tlv_codec import TLVCodec
import messages

class MobilePhone:
    """手机类"""

    def __init__(self):
        self.attached = False
        self.codec = TLVCodec()

    def send_attach_request(self) -> bytes:
        """发送附着请求"""
        data = b'\x00\x01'
        self.attached = True
        print(f"  [手机] 发送: AttachRequest, 数据={data.hex()}")
        return self.codec.encode(messages.MSG_ATTACH_REQUEST, data)

    def send_attach_complete(self) -> bytes:
        """发送附着完成消息"""
        data = b'\x00\x00'
        print(f"  [手机] 发送: AttachComplete")
        return self.codec.encode(messages.MSG_ATTACH_COMPLETE, data)

    def send_data_uplink(self, payload: bytes) -> bytes:
        """发送上行数据"""
        print(f"  [手机] 发送: DataUplink, 数据={payload.hex()}")
        return self.codec.encode(messages.MSG_DATA_UPLINK, payload)

    def send_detach_request(self) -> bytes:
        """发送去附着请求"""
        self.attached = False
        data = b'\x00\x00'
        print(f"  [手机] 发送: DetachRequest")
        return self.codec.encode(messages.MSG_DETACH_REQUEST, data)

    def process_response(self, data: bytes) -> str:
        """处理基站响应"""
        msg_type, value = self.codec.decode(data)
        name = messages.get_msg_name(msg_type)
        print(f"  [手机] 收到: {name}, value={value.hex()}")
        return name
