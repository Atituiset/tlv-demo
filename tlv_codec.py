"""TLV Codec - 基站与手机消息的序列化/反序列化"""

class TLVCodec:
    """TLV编解码器"""

    @staticmethod
    def encode(msg_type: int, value: bytes) -> bytes:
        """将消息编码为TLV格式

        Args:
            msg_type: 消息类型 (1-255)
            value: 消息体字节数据

        Returns:
            bytes: Type(1字节) + Length(2字节大端) + Value
        """
        type_byte = bytes([msg_type])
        length_bytes = len(value).to_bytes(2, 'big')
        return type_byte + length_bytes + value

    @staticmethod
    def decode(data: bytes) -> tuple[int, bytes]:
        """解码TLV消息

        Args:
            data: 完整的TLV字节数据

        Returns:
            tuple: (msg_type, value)
        """
        if len(data) < 3:
            raise ValueError(f"TLV数据太短: 需要至少3字节, 实际{len(data)}字节")
        msg_type = data[0]
        length = int.from_bytes(data[1:3], 'big')
        if len(data) < 3 + length:
            raise ValueError(f"TLV数据不完整: 声明长度{length}, 实际可用{len(data)-3}字节")
        value = data[3:3+length]
        return msg_type, value
