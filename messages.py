"""消息类型定义"""

# 消息类型枚举
MSG_ATTACH_REQUEST = 0x01
MSG_ATTACH_ACCEPT = 0x02
MSG_ATTACH_COMPLETE = 0x03
MSG_DATA_UPLINK = 0x04
MSG_DATA_DOWNLINK = 0x05
MSG_DETACH_REQUEST = 0x06
MSG_DETACH_ACCEPT = 0x07

# 消息类型名称映射
MSG_NAMES = {
    MSG_ATTACH_REQUEST: "AttachRequest",
    MSG_ATTACH_ACCEPT: "AttachAccept",
    MSG_ATTACH_COMPLETE: "AttachComplete",
    MSG_DATA_UPLINK: "DataUplink",
    MSG_DATA_DOWNLINK: "DataDownlink",
    MSG_DETACH_REQUEST: "DetachRequest",
    MSG_DETACH_ACCEPT: "DetachAccept",
}

def get_msg_name(msg_type: int) -> str:
    """获取消息类型名称"""
    return MSG_NAMES.get(msg_type, f"Unknown(0x{msg_type:02x})")
