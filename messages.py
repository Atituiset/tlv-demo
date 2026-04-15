"""消息类型定义"""

# 消息类型枚举
MSG_ATTACH_REQUEST = 0x01
MSG_ATTACH_ACCEPT = 0x02
MSG_ATTACH_COMPLETE = 0x03
MSG_DATA_UPLINK = 0x04
MSG_DATA_DOWNLINK = 0x05
MSG_DETACH_REQUEST = 0x06
MSG_DETACH_ACCEPT = 0x07

# 嵌套TLV消息类型
MSG_CAPABILITY_INFO = 0x10      # 能力信息容器
MSG_NETWORK_TYPE = 0x11         # 网络类型
MSG_VOICE_CAPABILITY = 0x12     # 语音能力
MSG_FREQUENCY_BAND_LIST = 0x13   # 频段列表容器
MSG_FREQUENCY_BAND = 0x14        # 单个频段

# 消息类型名称映射
MSG_NAMES = {
    MSG_ATTACH_REQUEST: "AttachRequest",
    MSG_ATTACH_ACCEPT: "AttachAccept",
    MSG_ATTACH_COMPLETE: "AttachComplete",
    MSG_DATA_UPLINK: "DataUplink",
    MSG_DATA_DOWNLINK: "DataDownlink",
    MSG_DETACH_REQUEST: "DetachRequest",
    MSG_DETACH_ACCEPT: "DetachAccept",
    MSG_CAPABILITY_INFO: "CapabilityInfo",
    MSG_NETWORK_TYPE: "NetworkType",
    MSG_VOICE_CAPABILITY: "VoiceCapability",
    MSG_FREQUENCY_BAND_LIST: "FrequencyBandList",
    MSG_FREQUENCY_BAND: "FrequencyBand",
}

def get_msg_name(msg_type: int) -> str:
    """获取消息类型名称"""
    return MSG_NAMES.get(msg_type, f"Unknown(0x{msg_type:02x})")
