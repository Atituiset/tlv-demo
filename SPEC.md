# TLV Demo - 蜂窝通信系统消息交互演示

## 概述

一个最小的蜂窝通信系统demo，模拟基站（BaseStation）和手机（MobilePhone）之间的TLV消息通信，用于学习协议栈基础知识。

## 系统架构

```
┌─────────────┐         TLV消息         ┌─────────────┐
│ BaseStation │ ◄─────────────────────► │ MobilePhone │
│   (基站)    │      TLVCodec           │   (手机)    │
└─────────────┘                         └─────────────┘
```

## TLV 格式

```
| Type (1字节) | Length (2字节) | Value (变长) |
```

- `Type`: 消息类型 ID（1字节，0x01-0xFF）
- `Length`: Value字段的字节数（2字节，大端序）
- `Value`: 实际数据（变长）

## 消息类型

| Type | 消息名 | 方向 | 说明 |
|------|--------|------|------|
| 0x01 | AttachRequest | 手机→基站 | 附着请求 |
| 0x02 | AttachAccept | 基站→手机 | 附着接受 |
| 0x03 | AttachComplete | 手机→基站 | 附着完成 |
| 0x04 | DataUplink | 手机→基站 | 上行数据 |
| 0x05 | DataDownlink | 基站→手机 | 下行数据 |
| 0x06 | DetachRequest | 手机→基站 | 去附着请求 |
| 0x07 | DetachAccept | 基站→手机 | 去附着接受 |

## 通信阶段

### 阶段1 - 附着流程（Attach）

```
手机 ──AttachRequest(0x01)──► 基站
手机 ◄──AttachAccept(0x02)─── 基站
手机 ──AttachComplete(0x03)──► 基站
```

### 阶段2 - 数据传输（Data Transfer）

```
手机 ──DataUplink(0x04)──────► 基站
手机 ◄──DataDownlink(0x05)─── 基站
(重复指定次数)
```

### 阶段3 - 去附着（Detach）

```
手机 ──DetachRequest(0x06)───► 基站
手机 ◄──DetachAccept(0x07)─── 基站
```

## 文件结构

```
TLV-demo/
├── SPEC.md              # 本规格文档
├── tlv_codec.py         # TLV编解码器
├── messages.py          # 消息类型定义
├── base_station.py      # 基站类
├── mobile_phone.py      # 手机类
└── tlv_demo.py          # 主程序，运行完整demo
```

## 实现步骤

1. `tlv_codec.py` - TLV消息的序列化/反序列化
2. `messages.py` - 消息类型和字段定义
3. `base_station.py` - 基站类
4. `mobile_phone.py` - 手机类
5. `tlv_demo.py` - 整合运行，输出交互日志

## 运行方式

```bash
python tlv_demo.py
```

## 预期输出

程序运行后会输出三个阶段的完整消息交互日志，显示每条TLV消息的原始字节内容和解析后的字段值。
