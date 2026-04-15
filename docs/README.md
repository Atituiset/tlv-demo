# TLV Demo 模块详细介绍文档

## 目录

- [概述](#概述)
- [架构图](#架构图)
- [模块详解](#模块详解)
  - [tlv_codec.py - TLV编解码器](#tlv_codecpy---tlv编解码器)
  - [messages.py - 消息类型定义](#messagespy---消息类型定义)
  - [base_station.py - 基站类](#base_stationpy---基站类)
  - [mobile_phone.py - 手机类](#mobile_phonepy---手机类)
  - [tlv_demo.py - 主程序](#tlv_demopy---主程序)
- [TLV格式详解](#tlv格式详解)
- [通信流程详解](#通信流程详解)

---

## 概述

本项目是一个用于学习蜂窝通信系统基础概念的最小demo。通过模拟基站（BaseStation）和手机（MobilePhone）之间的消息交互，展示：

1. **TLV (Type-Length-Value) 消息格式** - 无线通信中广泛使用的编码方式
2. **附着流程 (Attach Procedure)** - 手机入网的基本过程
3. **数据传输 (Data Transfer)** - 双向数据通信
4. **去附着流程 (Detach Procedure)** - 手机离网过程

---

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        手机 (MobilePhone)                    │
│  ┌─────────────┐                                           │
│  │ TLVCodec    │  ←──  encode(msg_type, value)              │
│  │             │  ──→  decode(data) → (msg_type, value)     │
│  └─────────────┘                                           │
│                                                              │
│  方法:                                                       │
│  • send_attach_request()  → 0x01                           │
│  • send_attach_complete() → 0x03                           │
│  • send_data_uplink()     → 0x04                           │
│  • send_detach_request()  → 0x06                           │
│  • process_response()     ←  解析基站响应                    │
└─────────────────────────────────────────────────────────────┘
                            │
                   TLV 字节流 (bytes)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       基站 (BaseStation)                      │
│  ┌─────────────┐                                           │
│  │ TLVCodec    │  ←──  encode(msg_type, value)              │
│  │             │  ──→  decode(data) → (msg_type, value)     │
│  └─────────────┘                                           │
│                                                              │
│  状态: connected (bool)                                      │
│                                                              │
│  receive(data) 处理:                                        │
│  • 0x01 (AttachRequest)  → 回复 0x02 (AttachAccept)         │
│  • 0x03 (AttachComplete) → 无响应                           │
│  • 0x04 (DataUplink)     → 回复 0x05 (DataDownlink)         │
│  • 0x06 (DetachRequest)  → 回复 0x07 (DetachAccept)         │
└─────────────────────────────────────────────────────────────┘
```

---

## 模块详解

### tlv_codec.py - TLV编解码器

**文件路径**: `tlv_codec.py`

**职责**: 负责将消息编码为TLV格式，以及从TLV格式解码还原消息。

#### TLV格式

```
┌─────────┬─────────┬───────────────────┐
│  Type   │ Length  │      Value         │
│ 1字节   │ 2字节   │   Length字节       │
└─────────┴─────────┴───────────────────┘
```

- **Type** (1字节): 消息类型ID，范围1-255
- **Length** (2字节): Value字段的字节数，**大端序**（Big Endian）
- **Value** (变长): 实际负载数据

#### 类定义

```python
class TLVCodec:
    @staticmethod
    def encode(msg_type: int, value: bytes) -> bytes

    @staticmethod
    def decode(data: bytes) -> tuple[int, bytes]
```

#### encode() 方法

将消息编码为TLV字节流。

**参数**:
- `msg_type: int` - 消息类型 (1-255)
- `value: bytes` - 消息体字节数据

**返回值**: `bytes` - 完整的TLV字节串

**示例**:
```python
codec = TLVCodec()
encoded = codec.encode(0x01, b'\x00\x01')
# 结果: b'\x01\x00\x01' (Type=0x01, Length=0x0001, Value=0x0001)
# 十六进制: 0100010001
```

#### decode() 方法

从TLV字节流中解析出消息类型和负载。

**参数**:
- `data: bytes` - 完整的TLV字节数据

**返回值**: `tuple[int, bytes]` - (消息类型, 负载数据)

**异常**:
- `ValueError` - 数据格式错误（太短、不完整）

**示例**:
```python
codec = TLVCodec()
msg_type, value = codec.decode(b'\x01\x00\x01')
# msg_type = 1
# value = b'\x00\x01'
```

---

### messages.py - 消息类型定义

**文件路径**: `messages.py`

**职责**: 定义项目中使用的所有消息类型常量，提供类型到名称的映射。

#### 消息类型常量

| 常量名 | 值 | 方向 | 说明 |
|--------|-----|------|------|
| `MSG_ATTACH_REQUEST` | 0x01 | 手机→基站 | 附着请求 |
| `MSG_ATTACH_ACCEPT` | 0x02 | 基站→手机 | 附着接受 |
| `MSG_ATTACH_COMPLETE` | 0x03 | 手机→基站 | 附着完成 |
| `MSG_DATA_UPLINK` | 0x04 | 手机→基站 | 上行数据 |
| `MSG_DATA_DOWNLINK` | 0x05 | 基站→手机 | 下行数据 |
| `MSG_DETACH_REQUEST` | 0x06 | 手机→基站 | 去附着请求 |
| `MSG_DETACH_ACCEPT` | 0x07 | 基站→手机 | 去附着接受 |

#### MSG_NAMES 字典

类型ID到类型名称的映射表，用于日志输出。

```python
MSG_NAMES = {
    0x01: "AttachRequest",
    0x02: "AttachAccept",
    # ...
}
```

#### get_msg_name() 函数

根据消息类型ID返回可读的名称字符串。

**签名**:
```python
def get_msg_name(msg_type: int) -> str
```

**示例**:
```python
get_msg_name(0x01)  # 返回 "AttachRequest"
get_msg_name(0xFF)  # 返回 "Unknown(0xff)"
```

---

### base_station.py - 基站类

**文件路径**: `base_station.py`

**职责**: 模拟基站行为，接收手机消息并返回响应，维护连接状态。

#### 类定义

```python
class BaseStation:
    def __init__(self)
    def receive(self, data: bytes) -> bytes | None
```

#### 构造函数

```python
def __init__(self)
```

初始化基站实例，创建TLVCodec实例，初始连接状态为 `False`。

#### receive() 方法

接收并处理手机发来的TLV消息，根据消息类型返回响应。

**参数**:
- `data: bytes` - 手机发送的TLV字节数据

**返回值**:
- `bytes | None` - 响应消息（TLV格式），无需响应时返回 `None`

**消息处理逻辑**:

| 收到的消息类型 | 处理动作 | 返回响应 |
|---------------|----------|----------|
| `MSG_ATTACH_REQUEST` (0x01) | 设置 `connected=True` | `MSG_ATTACH_ACCEPT` (0x02) |
| `MSG_ATTACH_COMPLETE` (0x03) | 打印完成状态 | `None` |
| `MSG_DATA_UPLINK` (0x04) | 将收到的数据作为响应返回 | `MSG_DATA_DOWNLINK` (0x05) |
| `MSG_DETACH_REQUEST` (0x06) | 设置 `connected=False` | `MSG_DETACH_ACCEPT` (0x07) |
| 其他 | 无处理 | `None` |

**使用示例**:
```python
bs = BaseStation()
response = bs.receive(tlv_bytes)
if response:
    # 发送响应给手机
    pass
```

---

### mobile_phone.py - 手机类

**文件路径**: `mobile_phone.py`

**职责**: 模拟手机行为，生成各类请求消息，处理基站响应，维护附着状态。

#### 类定义

```python
class MobilePhone:
    def __init__(self)
    def send_attach_request(self) -> bytes
    def send_attach_complete(self) -> bytes
    def send_data_uplink(self, payload: bytes) -> bytes
    def send_detach_request(self) -> bytes
    def process_response(self, data: bytes) -> str
```

#### 构造函数

```python
def __init__(self)
```

初始化手机实例，创建TLVCodec实例，初始附着状态为 `False`。

#### send_attach_request() 方法

生成附着请求消息。

**返回值**: `bytes` - TLV格式的AttachRequest消息

**发送的数据**: `b'\x00\x01'` (示例负载)

**状态变更**: 设置 `self.attached = True`

#### send_attach_complete() 方法

生成附着完成消息。

**返回值**: `bytes` - TLV格式的AttachComplete消息

**发送的数据**: `b'\x00\x00'`

#### send_data_uplink() 方法

生成上行数据消息。

**参数**:
- `payload: bytes` - 要发送的数据负载

**返回值**: `bytes` - TLV格式的DataUplink消息

**示例**:
```python
phone = MobilePhone()
msg = phone.send_data_uplink(b'\x00\x01')
# 生成 TLV: Type=0x04, Length=2, Value=0001
```

#### send_detach_request() 方法

生成去附着请求消息。

**返回值**: `bytes` - TLV格式的DetachRequest消息

**发送的数据**: `b'\x00\x00'`

**状态变更**: 设置 `self.attached = False`

#### process_response() 方法

解析基站返回的响应消息。

**参数**:
- `data: bytes` - 基站响应的TLV字节数据

**返回值**: `str` - 消息类型名称

---

### tlv_demo.py - 主程序

**文件路径**: `tlv_demo.py`

**职责**: 整合所有模块，运行完整的三个阶段演示。

#### run_demo() 函数

按顺序执行三个通信阶段：

**阶段1: 附着流程 (Attach)**
```
手机 ──AttachRequest(0x01)──► 基站
手机 ◄──AttachAccept(0x02)─── 基站
手机 ──AttachComplete(0x03)──► 基站
```

**阶段2: 数据传输 (Data Transfer)**
```
for i in range(3):
    手机 ──DataUplink(0x04)──► 基站
    手机 ◄──DataDownlink(0x05)─── 基站
```

**阶段3: 去附着 (Detach)**
```
手机 ──DetachRequest(0x06)───► 基站
手机 ◄──DetachAccept(0x07)─── 基站
```

#### 运行输出示例

```
============================================================
蜂窝通信系统 - TLV消息交互Demo
============================================================

【阶段1】附着流程 (Attach)
----------------------------------------
  [手机] 发送: AttachRequest, 数据=0001
  [基站] 收到消息: AttachRequest, value=0001
  [基站] 发送: AttachAccept
  [手机] 收到: AttachAccept, value=0001
  [手机] 发送: AttachComplete
  [基站] 收到消息: AttachComplete, value=0000
  [基站] 附着完成，状态: connected=True

【阶段2】数据传输 (Data Transfer)
----------------------------------------
  [手机] 发送: DataUplink, 数据=0001
  [基站] 收到消息: DataUplink, value=0001
  [基站] 发送: DataDownlink, 数据=0001
  ...

【阶段3】去附着 (Detach)
----------------------------------------
  ...
============================================================
Demo完成!
============================================================
```

---

## TLV格式详解

### 为什么无线通信使用TLV？

| 特性 | 固定字段格式 | TLV格式 |
|------|-------------|---------|
| **可扩展性** | ❌ 新字段需改协议 | ✅ 随时添加新字段 |
| **可选字段** | ❌ 必须填默认值 | ✅ 可完全省略 |
| **版本兼容** | ❌ 旧代码无法识别新字段 | ✅ 忽略未知Type |
| **解析复杂度** | ✅ 简单 | ❌ 稍复杂 |
| **编码效率** | ✅ 紧凑 | ❌ 有Type/Length开销 |

### 本项目TLV字节流示例

**AttachRequest 消息**:
```
原始数据: Type=0x01, Length=2, Value=0001
字节流:   01    00 01    00 01
          ^^^^ ^^^^ ^^^^^^
          |    |    |
          |    |    +-- Value (2字节: 00 01)
          |    +------- Length (2字节大端: 表示Value有2字节)
          +---------- Type (1字节: 0x01 = AttachRequest)
```

**DataUplink 消息** (payload = `\x00\x02`):
```
字节流:   04    00 01    00 02
          ^^^^ ^^^^ ^^^^^^
          |    |    +-- Value (1字节: 02)
          |    +------- Length (2字节大端: 表示Value有1字节)
          +---------- Type (1字节: 0x04 = DataUplink)
```

---

## 通信流程详解

### 阶段1: 附着流程 (Attach)

```
┌────────┐                      ┌────────┐
│  手机  │                      │  基站  │
└───┬────┘                      └───┬────┘
    │                                │
    │  1. AttachRequest (0x01)       │
    │───────────────────────────────►│
    │  [手机发起附着请求]              │
    │                                │
    │  2. AttachAccept (0x02)        │
    │◄──────────────────────────────│
    │  [基站批准附着请求]              │
    │                                │
    │  3. AttachComplete (0x03)      │
    │───────────────────────────────►│
    │  [手机确认附着完成]              │
    │                                │
    │           [连接建立]            │
    │                                │
```

**真实LTE中的附着流程** (简化版):
1. 手机发送 RRC Connection Request → 基站
2. 基站发送 RRC Connection Setup → 手机
3. 手机发送 RRC Connection Setup Complete (含NAS Attach Request)
4. 基站发送 RRC Connection Reconfiguration (含NAS Attach Accept)
5. 手机发送 RRC Connection Reconfiguration Complete

### 阶段2: 数据传输 (Data Transfer)

```
┌────────┐                      ┌────────┐
│  手机  │                      │  基站  │
└───┬────┘                      └───┬────┘
    │                                │
    │  DataUplink (0x04) + payload  │
    │───────────────────────────────►│
    │  [用户数据上行传输]              │
    │                                │
    │  DataDownlink (0x05) + payload│
    │◄──────────────────────────────│
    │  [基站响应/确认]                │
    │                                │
    │  (重复多次)                    │
```

### 阶段3: 去附着 (Detach)

```
┌────────┐                      ┌────────┐
│  手机  │                      │  基站  │
└───┬────┘                      └───┬────┘
    │                                │
    │  DetachRequest (0x06)          │
    │───────────────────────────────►│
    │  [手机请求断开连接]              │
    │                                │
    │  DetachAccept (0x07)           │
    │◄──────────────────────────────│
    │  [基站确认断开]                 │
    │                                │
    │       [连接断开]               │
    │                                │
```

---

## 扩展建议

如果你想继续学习，可以尝试以下扩展：

1. **添加更多消息类型**
   - 在 `messages.py` 中定义新常量
   - 在 `base_station.py` 和 `mobile_phone.py` 中实现处理逻辑

2. **添加消息字段验证**
   - 在 `messages.py` 中定义每种消息的字段结构
   - 添加字段级编解码

3. **模拟错误场景**
   - 基站拒绝附着
   - 数据传输丢包
   - 超时重传

4. **添加加密/解密**
   - 在 `TLVCodec` 中添加 `encrypt()` / `decrypt()` 方法

5. **使用更真实的协议**
   - 学习 ASN.1 PER 编码
   - 研究 3GPP TS 36.335 (LTE NAS)
