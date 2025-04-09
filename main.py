# -*- coding: utf-8 -*-
# @Author: Chang SeungHyeock
# @Date:   2025-03-28 10:38:44
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 10:07:01
import paho.mqtt.client as mqtt

from Mqtt_Function.Uplink_Function import mqtt_uplink_message_handler
from Display_Function.Device_Display_Manager import display_manager, display_sensor_data
from Store_Function.Device_Info import device_data
from Etc_Function.Device_Connection_Check import connectionManager
from Define_Value.Constan_Value import constant

# DataManager를 생성할 때, device_data를 "밖에서" 인자로 주입
data_manager = connectionManager(device_data=device_data, check_interval=constant.CHECK_INTERVAL, timeout_seconds=constant.TIMEOUT_LIMIT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("v3/shchang-bme280-test@ttn/devices/+/up")  # 실제 구독 토픽으로 수정 필요


# MQTT 클라이언트 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = mqtt_uplink_message_handler

# TTN 인증 정보 설정 (수정 필요)
client.username_pw_set(
    username="shchang-bme280-test@ttn",  # 앱 ID + 테넌트
    password="NNSXS.OYD3BA3LOBYUDFIYHLSZQB3ZAHBRC2PLY5IMKAQ.DT5IK2FRQKJZ2V7FEXC76N4PKUW7FPRSQ54EWV7OPYXS7TLHDYKQ"  # 실제 API 키 입력
)
client.tls_set()  # TLS 활성화

# 브로커 연결
client.connect("au1.cloud.thethings.network", 8883, 60)

# 오프라인 체크 시작
data_manager.start_offline_checker()

client.loop_forever()