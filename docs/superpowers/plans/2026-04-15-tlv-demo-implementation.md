# TLV Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现一个最小的蜂窝通信系统demo，模拟基站和手机之间的TLV消息交互

**Architecture:** 使用纯Python实现，两个核心类（BaseStation、MobilePhone）通过TLVCodec进行消息编解码。消息流分为三个阶段：附着、数据传输、去附着。

**Tech Stack:** Python 3（无外部依赖）

---

## 文件结构

```
TLV-demo/
├── tlv_codec.py         # TLV编解码器
├── messages.py          # 消息类型定义
├── base_station.py      # 基站类
├── mobile_phone.py      # 手机类
└── tlv_demo.py          # 主程序
```

---

## Task 1: TLV 编解码器

**Files:**
- Create: `tlv_codec.py`

- [ ] **Step 1: 编写 TLV 编码/解码实现**

```python
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
```

- [ ] **Step 2: 验证编码解码正确性**

```python
import tlv_codec

codec = TLVCodec()
original_type = 0x01
original_value = b'\x00\x01\x02\x03'
encoded = codec.encode(original_type, original_value)
decoded_type, decoded_value = codec.decode(encoded)
assert decoded_type == original_type
assert decoded_value == original_value
print(f"编码后: {encoded.hex()}")
print(f"解码后 type={decoded_type}, value={decoded_value.hex()}")
```

Run: `python -c "import tlv_codec; c = tlv_codec.TLVCodec(); e = c.encode(1, b'hello'); print(c.decode(e))"`
Expected: `(1, b'hello')`

- [ ] **Step 3: 提交**

```bash
git add tlv_codec.py
git commit -m "feat: 实现TLV编解码器"
```

---

## Task 2: 消息类型定义

**Files:**
- Create: `messages.py`

- [ ] **Step 1: 定义消息类型和辅助函数**

```python
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
```

- [ ] **Step 2: 验证消息类型定义**

Run: `python -c "import messages; print(messages.get_msg_name(0x01))"`
Expected: `AttachRequest`

- [ ] **Step 3: 提交**

```bash
git add messages.py
git commit -m "feat: 定义消息类型常量"
```

---

## Task 3: 基站类

**Files:**
- Create: `base_station.py`

- [ ] **Step 1: 实现基站类**

```python
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
```

- [ ] **Step 2: 验证基站类可以正常接收消息**

Run: `python -c "from base_station import BaseStation; from tlv_codec import TLVCodec; bs = BaseStation(); c = TLVCodec(); r = bs.receive(c.encode(0x01, b'Hello')); print('Response:', r.hex() if r else None)"`
Expected: `Response: 020001` (AttachAccept)

- [ ] **Step 3: 提交**

```bash
git add base_station.py
git commit -m "feat: 实现基站类"
```

---

## Task 4: 手机类

**Files:**
- Create: `mobile_phone.py`

- [ ] **Step 1: 实现手机类**

```python
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
```

- [ ] **Step 2: 验证手机类基本功能**

Run: `python -c "from mobile_phone import MobilePhone; m = MobilePhone(); d = m.send_attach_request(); print(d.hex())"`
Expected: `0100010001`

- [ ] **Step 3: 提交**

```bash
git add mobile_phone.py
git commit -m "feat: 实现手机类"
```

---

## Task 5: 主程序 - 完整Demo

**Files:**
- Create: `tlv_demo.py`

- [ ] **Step 1: 实现主程序**

```python
"""TLV Demo - 蜂窝通信系统消息交互演示"""

from base_station import BaseStation
from mobile_phone import MobilePhone

def run_demo():
    print("=" * 60)
    print("蜂窝通信系统 - TLV消息交互Demo")
    print("=" * 60)

    bs = BaseStation()
    phone = MobilePhone()

    # ========== 阶段1: 附着流程 ==========
    print("\n【阶段1】附着流程 (Attach)")
    print("-" * 40)

    # 手机发送附着请求
    msg = phone.send_attach_request()
    response = bs.receive(msg)

    # 手机处理基站响应
    phone.process_response(response)

    # 手机发送附着完成
    msg = phone.send_attach_complete()
    bs.receive(msg)

    # ========== 阶段2: 数据传输 ==========
    print("\n【阶段2】数据传输 (Data Transfer)")
    print("-" * 40)

    for i in range(3):
        data = bytes([0x00, i + 1])
        msg = phone.send_data_uplink(data)
        response = bs.receive(msg)
        phone.process_response(response)

    # ========== 阶段3: 去附着 ==========
    print("\n【阶段3】去附着 (Detach)")
    print("-" * 40)

    msg = phone.send_detach_request()
    response = bs.receive(msg)
    phone.process_response(response)

    print("\n" + "=" * 60)
    print("Demo完成!")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
```

- [ ] **Step 2: 运行完整Demo**

Run: `python tlv_demo.py`
Expected: 输出包含三个阶段的完整交互日志

- [ ] **Step 3: 提交**

```bash
git add tlv_demo.py
git commit -m "feat: 实现完整demo主程序"
```

---

## 自检清单

- [ ] 所有文件路径正确
- [ ] Task顺序正确（codec -> messages -> base_station -> mobile_phone -> demo）
- [ ] 每个Task都有测试验证
- [ ] 代码无placeholder/TODO
- [ ] 符合SPEC.md所有要求

---

**Plan complete.** 文件已保存到 `docs/superpowers/plans/2026-04-15-tlv-demo-implementation.md`

两个执行选项：

**1. Subagent-Driven (推荐)** - 每个Task分配一个subagent执行，任务间有检查点

**2. Inline Execution** - 在当前session中按顺序执行所有Task

选择哪个方式？