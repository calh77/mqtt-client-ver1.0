# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-08 07:51:06
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 09:10:26
import json
import base64

def mqtt_downlink_message_sender(client, deviceId, count):
    if count == 1:
        downlinkPayloadByte = b'\x21'
    else:
        downlinkPayloadByte = b'\x11'
    downlinkPayload = {
        "downlinks": [
            {
                "frm_payload": base64.b64encode(downlinkPayloadByte).decode('utf-8'),
                "f_port": 2,
                "confirmed": False,
                "priority": "NORMAL"
            }
        ]
    }

    topic = f"v3/shchang-bme280-test@ttn/devices/{deviceId}/down/push"
    client.publish(topic, json.dumps(downlinkPayload))
    print(f"[Downlink to {deviceId}] 0x{downlinkPayloadByte.hex()}\n")

