"""手机模拟器"""

from tlv_codec import TLVCodec
from nested_tlv_codec import NestedTLVCodec
import messages


class MobilePhone:
    """手机类"""

    def __init__(self):
        self.attached = False
        self.codec = TLVCodec()
        self.nested_codec = NestedTLVCodec()

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

    def send_attach_with_capabilities(self) -> bytes:
        """发送带嵌套能力的附着请求"""
        # 构建嵌套的频段列表
        band1 = self.codec.encode(messages.MSG_FREQUENCY_BAND, b'\x08\x34')  # 2100MHz
        band2 = self.codec.encode(messages.MSG_FREQUENCY_BAND, b'\x0D\xA4')  # 3500MHz
        freq_band_list = self.nested_codec.encode_container(
            messages.MSG_FREQUENCY_BAND_LIST, [band1, band2]
        )

        # 构建嵌套的能力信息
        network_type = self.codec.encode(messages.MSG_NETWORK_TYPE, b'5G')
        voice_cap = self.codec.encode(messages.MSG_VOICE_CAPABILITY, b'VoNR')
        capability_info = self.nested_codec.encode_container(
            messages.MSG_CAPABILITY_INFO,
            [network_type, voice_cap, freq_band_list]
        )

        # 构建完整的附着请求
        data = capability_info
        self.attached = True
        print(f"  [手机] 发送: AttachRequest (带嵌套能力)")
        return self.codec.encode(messages.MSG_ATTACH_REQUEST, data)

    def process_response(self, data: bytes) -> str:
        """处理基站响应"""
        msg_type, value = self.codec.decode(data)
        name = messages.get_msg_name(msg_type)
        print(f"  [手机] 收到: {name}, value={value.hex()}")
        return name
