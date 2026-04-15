"""嵌套TLV编解码器 - 支持递归编码/解码"""

from tlv_codec import TLVCodec


class NestedTLVCodec:
    """嵌套TLV编解码器，支持容器TLV和递归解析"""

    def __init__(self):
        self.codec = TLVCodec()

    def encode_container(self, tag: int, children: list[bytes]) -> bytes:
        """编码容器TLV（Value是多个TLV的拼接）

        Args:
            tag: 容器标签
            children: 子TLV列表

        Returns:
            bytes: 容器TLV编码结果
        """
        content = b''.join(children)
        return self.codec.encode(tag, content)

    def decode_container(self, data: bytes) -> list[tuple[int, bytes]]:
        """解码容器，提取所有子TLV

        Args:
            data: 容器的内容数据

        Returns:
            list: [(tag, value), ...] 子TLV列表
        """
        result = []
        offset = 0
        while offset < len(data):
            if offset + 3 > len(data):
                break
            tag = data[offset]
            length = int.from_bytes(data[offset+1:offset+3], 'big')
            if offset + 3 + length > len(data):
                break
            value = data[offset+3:offset+3+length]
            result.append((tag, value))
            offset += 3 + length
        return result

    def decode_nested(self, data: bytes) -> list[tuple[int, bytes | list]]:
        """递归解码嵌套TLV（自动识别容器并展开）

        Args:
            data: TLV数据

        Returns:
            list: [(tag, value或子TLV列表), ...]
        """
        result = []
        offset = 0
        while offset < len(data):
            if offset + 3 > len(data):
                break
            tag = data[offset]
            length = int.from_bytes(data[offset+1:offset+3], 'big')
            if offset + 3 + length > len(data):
                break
            value = data[offset+3:offset+3+length]
            # 递归解码容器类型
            if tag in (0x10, 0x13):  # CapabilityInfo, FrequencyBandList
                value = self.decode_nested(value)
            result.append((tag, value))
            offset += 3 + length
        return result
