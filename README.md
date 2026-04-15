# TLV Demo - 蜂窝通信系统消息交互演示

一个最小的蜂窝通信系统demo，模拟基站（BaseStation）和手机（MobilePhone）之间的TLV消息交互。

## 快速开始

```bash
# 安装依赖（无外部依赖，使用uv管理）
uv sync

# 运行demo
uv run python tlv_demo.py
```

## 项目结构

| 文件 | 说明 |
|------|------|
| `tlv_codec.py` | TLV消息编解码器 |
| `messages.py` | 消息类型定义 (0x01-0x07) |
| `base_station.py` | 基站类 |
| `mobile_phone.py` | 手机类 |
| `tlv_demo.py` | 主程序入口 |
| `docs/README.md` | 详细模块文档 |

## 通信流程

```
阶段1: 附着 (Attach)
  手机 ──AttachRequest──► 基站
  手机 ◄──AttachAccept─── 基站
  手机 ──AttachComplete──► 基站

阶段2: 数据传输 (Data Transfer)
  手机 ──DataUplink──────► 基站
  手机 ◄──DataDownlink─── 基站
  (重复多次)

阶段3: 去附着 (Detach)
  手机 ──DetachRequest───► 基站
  手机 ◄──DetachAccept─── 基站
```

## TLV 格式

```
| Type (1字节) | Length (2字节大端) | Value (变长) |
```

详细说明请参阅 [docs/README.md](docs/README.md)
