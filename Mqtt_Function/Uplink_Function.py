# -*- coding: utf-8 -*-
# @Author: Chang SeungHyeock
# @Date:   2025-04-07 14:03:27
# @Last Modified by:   Your name
# @Last Modified time: 2025-05-07 15:04:50
import json
import base64
from dateutil import parser
import pytz
from collections import defaultdict

import Define_Value.Constan_Value

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
        moduleInfo = decodedUplinkPayload.get("moduleType", "N/A")
        moduleInfoByte = int(moduleInfo, 16)
        alarmInfo = decodedUplinkPayload.get("alarmInfo", "N/A")
        alarmInfoByte = int(alarmInfo, 16)
        operationMode = decodedUplinkPayload.get("sensorOpMode", "N/A")
        utcTime = parser.isoparse(uplinkData.get("received_at", "1970-01-01T00:00:00Z"))

        # 한국 시간대 설정
        kst = pytz.timezone("Asia/Seoul")
        # 한국 시간대로 변환
        koreaTime = utcTime.astimezone(kst)

        device_data[deviceId]["count"] += 1
        device_data[deviceId]["last_payload"] = decodedUplinkPayload
        device_data[deviceId]["last_time"] = koreaTime
        device_data[deviceId]["on_line"] = True

        if alarmInfo == "0x00":
            count = device_data[deviceId]["count"]
            temperature = decodedUplinkPayload.get("temperature", "N/A")
            humidity = decodedUplinkPayload.get("humidity", "N/A")
            pressure = decodedUplinkPayload.get("pressure", "N/A")
            if operationMode == "single sensing":
                sensingGas = decodedUplinkPayload.get("measureGas", "N/A")
                concentration = decodedUplinkPayload.get('concentration', 'N/A')
                print(koreaTime.strftime("%Y-%m-%d %H:%M:%S"))
                print(f"[{deviceId}] Count={count}, Module Type=0x{moduleInfo}, Alarm Info=0x{alarmInfo}")
                print(f"Temp={temperature:.2f}°C, Humidity={humidity:.2f}%, Pressure={pressure:.0f}hPa, {sensingGas} Concentration={concentration:.2f}%")
                result = (
                    f"Device ID      : {deviceId}\n"
                    f"Receiving Time : {koreaTime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"Module and Alarm Info(HEX) : 0x{moduleInfo}, 0x{alarmInfo}\n"
                    f"T/H/P : {temperature:.2f}°C, {humidity:.2f}%, {pressure:.0f}hpa\n"
                    f"{sensingGas} Concentration: {concentration:.2f}%\n"
                )
            else:
                O2Concentration = decodedUplinkPayload.get("O2Concentration", "N/A")
                COConcentration = decodedUplinkPayload.get("COConcentration", "N/A")
                H2SConcentration = decodedUplinkPayload.get("H2SConcentration", "N/A")
                CH4Concentration = decodedUplinkPayload.get("CH4Concentration", "N/A")

                print(koreaTime.strftime("%Y-%m-%d %H:%M:%S"))
                print(f"[{deviceId}] Count={count}, Module Type=0x{moduleInfo}, Alarm Info=0x{alarmInfo}")
                print(f"Temp={temperature:.2f}°C, Humidity={humidity:.2f}%, Pressure={pressure:.0f}hPa")
                printTextPart = []
                if O2Concentration != "N/A":
                    printTextPart.append(f"O2={O2Concentration:.2f}%")
                if COConcentration != "N/A":
                    printTextPart.append(f", CO={COConcentration:.2f}%")
                if H2SConcentration != "N/A":
                    printTextPart.append(f", H2S={H2SConcentration:.2f}%")
                if CH4Concentration != "N/A":
                    printTextPart.append(f", CH4={CH4Concentration:.2f}%")
                print(" ".join(printTextPart))

                result = (
                    f"Device ID      : {deviceId}\n"
                    f"Receiving Time : {koreaTime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"Module and Alarm Info(HEX) : 0x{moduleInfo}, 0x{alarmInfo}\n"
                    f"T/H/P : {temperature:.2f}°C, {humidity:.2f}%, {pressure:.0f}hpa\n"
                )
                if O2Concentration != "N/A":
                    result += f"O2 Con. : {O2Concentration:.2f}%"
                if COConcentration != "N/A":
                    result += f", CO Con. : {COConcentration:.2f}%"
                if H2SConcentration != "N/A":
                    result += f", H2S Con. : {H2SConcentration:.2f}%"
                if CH4Concentration != "N/A":
                    result += f", CH4 Con. : {CH4Concentration:.2f}%\n"
#        else:

        # Text box 가져오기 또는 새로 만들기
        if deviceId not in device_text_boxes:
            from Display_Function.Data_Display import create_text_and_graph_frame
            create_text_and_graph_frame(root, deviceId, device_text_boxes, device_graphs)

        text_box = device_text_boxes[deviceId]
        text_box.insert("end", result)
        text_box.see("end")

        # 특정 값 예: O2, CH4
#        if O2Voltage is not None:
#            update_device_o2_graph(deviceId, O2Voltage, device_graphs)
#        if CH4Value is not None:
#            update_device_ch4_graph(deviceId, CH4Value, device_graphs)


#        if count % 3 == 0 or count == 1:
#            mqtt_downlink_message_sender(client, deviceId, count)
#        else:
#            mqtt_downlink_message_sender(client, deviceId, count)
#                print("")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
