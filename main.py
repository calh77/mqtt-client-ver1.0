# -*- coding: utf-8 -*-
# @Author: Chang SeungHyeock
# @Date:   2025-03-28 10:38:44
# @Last Modified by:   Your name
# @Last Modified time: 2025-05-09 13:26:25
import paho.mqtt.client as mqtt
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Mqtt_Function.Uplink_Function import mqtt_uplink_message_handler
from Store_Function.Device_Info import device_data
from Etc_Function.Device_Connection_Check import connectionManager
from Define_Value.Constan_Value import constant
from Display_Function.Data_Display import create_text_and_graph_frame


# tkinter 창 설정정
root = tk.Tk()
root.title("Receiving Sensor Data from TTN MQTT Broker")
root.geometry("800x600")

# 여기서 안내용 텍스트 출력용 프레임과 텍스트 박스를 생성!
#_, text_box = create_text_and_graph_frame(root)
# 개별 센서 노드별 출력 박스 생성
device_text_boxes = {}

# 디바이스별 그래프 저장할 딕셔너리  (⭐️ 추가 필요)
device_graphs = {}

# DataManager를 생성할 때, device_data를 "밖에서" 인자로 주입
data_manager = connectionManager(device_data=device_data, check_interval=constant.CHECK_INTERVAL, timeout_seconds=constant.TIMEOUT_LIMIT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("v3/shchang-bme280-test@ttn/devices/+/up")  # 실제 구독 토픽으로 수정 필요


# MQTT 클라이언트 설정
client = mqtt.Client(userdata={"device_text_boxes": device_text_boxes,
                               "device_graphs": device_graphs,
                               "root": root})
#client = mqtt.Client()
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

client.loop_start()
root.mainloop()