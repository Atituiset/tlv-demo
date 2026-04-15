# Nested TLV 嵌套消息设计

## 目标

在现有 TLV-demo 项目中增加嵌套TLV的演示，作为教学用途，让用户理解复杂协议中嵌套结构的编解码方式。

## 扩展消息类型

| Type | 消息 | 说明 |
|------|------|------|
| 0x10 | CapabilityInfo | 能力信息容器（嵌套TLV） |
| 0x11 | NetworkType | 网络类型 (4G/5G) |
| 0x12 | VoiceCapability | 语音能力 (VoNR/VoLTE) |
| 0x13 | FrequencyBandList | 频段列表容器（嵌套容器） |
| 0x14 | FrequencyBand | 单个频段 |

## 嵌套结构示例

```
AttachRequest (0x01)
└── Value: 嵌套的 CapabilityInfo
    ├── NetworkType (0x11): "5G"
    ├── VoiceCapability (0x12): "VoNR"
    └── FrequencyBandList (0x13)
        ├── FrequencyBand (0x14): 2100
        └── FrequencyBand (0x14): 3500
```

## 新增文件

### nested_tlv_codec.py

`NestedTLVCodec` 类：
- `encode_nested(msg_type, tlvs)` - 编码嵌套TLV
- `decode_nested(data)` - 递归解码，返回 (type, value, remaining)
- `encode_container(tag, children)` - 编码容器TLV
- `decode_container(data)` - 解码容器，提取所有子TLV

## 修改文件

### messages.py

新增消息类型常量。

### mobile_phone.py

新增方法：
- `send_attach_with_capabilities()` - 发送带嵌套能力的附着请求

### base_station.py

修改 `receive()` 方法：
- 处理 `MSG_ATTACH_REQUEST` 时，递归解析嵌套的 CapabilityInfo
- 打印解析后的嵌套结构

### tlv_demo.py

新增**阶段4**演示流程。

## 演示流程

```
手机 ──AttachRequest (带嵌套)──► 基站
手机 ◄──AttachAccept─────────── 手机处理响应
```

基站收到后打印嵌套结构：
```
[基站] 收到: AttachRequest
  ├── NetworkType: 5G
  ├── VoiceCapability: VoNR
  └── FrequencyBandList:
      ├── Band: 2100
      └── Band: 3500
```
