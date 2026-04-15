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

    # ========== 阶段4: 嵌套TLV演示 ==========
    print("\n【阶段4】嵌套TLV (Nested TLV)")
    print("-" * 40)

    msg = phone.send_attach_with_capabilities()
    response = bs.receive(msg)
    phone.process_response(response)

    print("\n" + "=" * 60)
    print("Demo完成!")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
