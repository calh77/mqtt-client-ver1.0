# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-03-28 10:38:44
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-07 08:50:44
import paho.mqtt.client as mqtt
import json
import base64
from dateutil import parser
from zoneinfo import ZoneInfo
from collections import defaultdict
device_message_count = defaultdict(int)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("v3/shchang-bme280-test@ttn/devices/+/up")  # 실제 구독 토픽으로 수정 필요

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        
        # 메시지 타입 확인
        if not data.get("uplink_message"):
            print("Ignoring non-uplink message")
            return

        # 안전한 필드 추출
        device_info = data.get("end_device_ids", {})
        decoded = data.get("uplink_message", {}).get("decoded_payload", {})
       
        # 필수 필드 존재 여부 확인
        if not all([device_info, decoded]):
            print("Invalid message structure")
            return

        # 데이터 추출 (기본값 설정)
        device_id = device_info.get("device_id", "N/A")
        utc_time = parser.isoparse(data.get("time", "1970-01-01T00:00:00Z"))
        # Up-Link Header
        up_link_header = decoded.get("dataType", "N/A")
        if up_link_header == "0x01":
            device_message_count[device_id] += 1
            msg_count = device_message_count[device_id]

    
        # 출력
        print(f"Device ID       : {device_id}")
        print(f"Message Count   : {msg_count}")
        print(f"Up-Link Header  : {up_link_header}")
        print(f"Temperature     : {decoded.get('temperature', 'N/A')}°C")
        print(f"Avr Temperature : {decoded.get('averageTemperature', 'N/A')}°C")
        print(f"Humidity        : {decoded.get('humidity', 'N/A')}%")
        print(f"Pressure        : {decoded.get('pressure', 'N/A')} hPa")
        print()

        # ─────────────────────────────────────────────────────────────
        # Up-Link Header가 0x01이면, 다운링크(0x11)를 포트 2번으로 전송
        # ─────────────────────────────────────────────────────────────
        if msg_count%3 == 0 or msg_count == 1:
            # msg_count가 1인 경우 0x21, 그 외(3의 배수) 0x11 사용 -> Base64로 인코딩
            payload_byte = b'\x21' if msg_count == 1 else b'\x11'

            downlink_payload = {
                "downlinks": [
                    {
                        # \x11 바이너리 -> Base64("EQ==")
                        "frm_payload": base64.b64encode(payload_byte).decode('utf-8'),
                        "f_port": 2,              # 다운링크 포트 = 2
                        "confirmed": False,       # True로 설정하면 Confirmed Downlink
                        "priority": "NORMAL"      # 우선순위
                    }
                ]
            }

            # 다운링크 전송 토픽: v3/<앱ID>@ttn/devices/<디바이스ID>/down/push
            topic = f"v3/shchang-bme280-test@ttn/devices/{device_id}/down/push"

            # MQTT로 다운링크 발행
            client.publish(topic, json.dumps(downlink_payload))
            print(f"[Downlink Sent] 0x{payload_byte.hex()} on FPort=2")


    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# TTN 인증 정보 설정 (수정 필요)
client.username_pw_set(
    username="shchang-bme280-test@ttn",  # 앱 ID + 테넌트
    password="NNSXS.OYD3BA3LOBYUDFIYHLSZQB3ZAHBRC2PLY5IMKAQ.DT5IK2FRQKJZ2V7FEXC76N4PKUW7FPRSQ54EWV7OPYXS7TLHDYKQ"  # 실제 API 키 입력
)
client.tls_set()  # TLS 활성화

# 브로커 연결
client.connect("au1.cloud.thethings.network", 8883, 60)
client.loop_forever()