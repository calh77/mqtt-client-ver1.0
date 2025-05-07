# -*- coding: utf-8 -*-
# @Author: Chang SeungHyeock
# @Date:   2025-04-07 14:03:27
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 16:57:19
import json
import base64
from dateutil import parser
import pytz
from collections import defaultdict

from Mqtt_Function.Downlink_Function import mqtt_downlink_message_sender
from Store_Function.Device_Info import device_data
from Display_Function.Data_Display import update_device_o2_graph
from Display_Function.Data_Display import update_device_ch4_graph

def mqtt_uplink_message_handler(client, userdata, msg):
    try:
        root = userdata["root"]     # 안전하게 가져옴
        device_text_boxes = userdata["device_text_boxes"]
        device_graphs = userdata["device_graphs"]

        # MQTT 메시지 파싱
        uplinkData = json.loads(msg.payload)
        if not uplinkData.get("uplink_message"):
            print("Ignoring uplink message..")
            return
        
        deviceInfo = uplinkData.get("end_device_ids", {})
        decodedUplinkPayload = uplinkData.get("uplink_message", {}).get("decoded_payload", {})
        if not all([deviceInfo, decodedUplinkPayload]):
            print("Invalid message structure..")
            return
        
        deviceId = deviceInfo.get("device_id", "N/A")
        uplinkDataHeader = decodedUplinkPayload.get("dataType", "N/A")
        utcTime = parser.isoparse(uplinkData.get("received_at", "1970-01-01T00:00:00Z"))

        # 한국 시간대 설정
        kst = pytz.timezone("Asia/Seoul")
        # 한국 시간대로 변환
        koreaTime = utcTime.astimezone(kst)

        if uplinkDataHeader == "0x01":
            device_data[deviceId]["count"] += 1
            device_data[deviceId]["last_payload"] = decodedUplinkPayload
            device_data[deviceId]["last_time"] = koreaTime
            device_data[deviceId]["on_line"] = True

            count = device_data[deviceId]["count"]
            temperature = decodedUplinkPayload.get('temperature', 'N/A')
            averageTemperature = decodedUplinkPayload.get('aveTemp', 'N/A')
            humidity = decodedUplinkPayload.get('humidity', 'N/A')
            pressure = decodedUplinkPayload.get('pressure', 'N/A')
            CH4Value = decodedUplinkPayload.get('CH4Value', 'N/A')
            O2Voltage = decodedUplinkPayload.get('O2Voltage', 'N/A')
            print(koreaTime.strftime("%Y-%m-%d %H:%M:%S"))
            print(f"[{deviceId}] Count={count}, Header=0x{uplinkDataHeader}, Temp={temperature}°C, AvrTemp={averageTemperature}°C, Humidity={humidity}%, Pressure={pressure}hPa, CH4={CH4Value}, O2={O2Voltage}V")

            result = (
                f"Data Received!!\n"
                f"Device ID      : {deviceId}\n"
                f"Receiving Time : {koreaTime.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Data Type(HEX) : {uplinkDataHeader}\n"
                f"Temperature    : {temperature:.1f}\n"
                f"Avg Temperature: {averageTemperature:.1f}\n"
                f"Humidity       : {humidity:.1f}\n"
                f"Pressure       : {pressure:.0f}\n"
                f"CH4            : {CH4Value:.0f}\n"
                f"O2             : {O2Voltage:.3f}\n\n"
            )

            # Text box 가져오기 또는 새로 만들기
            if deviceId not in device_text_boxes:
                from Display_Function.Data_Display import create_text_and_graph_frame
                create_text_and_graph_frame(root, deviceId, device_text_boxes, device_graphs)

            text_box = device_text_boxes[deviceId]
            text_box.insert("end", result)
            text_box.see("end")

            # 특정 값 예: O2, CH4
            if O2Voltage is not None:
                update_device_o2_graph(deviceId, O2Voltage, device_graphs)
            if CH4Value is not None:
                update_device_ch4_graph(deviceId, CH4Value, device_graphs)


            if count % 3 == 0 or count == 1:
                mqtt_downlink_message_sender(client, deviceId, count)
            else:
                mqtt_downlink_message_sender(client, deviceId, count)
#                print("")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
