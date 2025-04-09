# -*- coding: utf-8 -*-
# @Author: Chang SeungHyeock
# @Date:   2025-04-07 14:03:27
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 11:09:36
import json
import base64
from dateutil import parser
from collections import defaultdict

from Mqtt_Function.Downlink_Function import mqtt_downlink_message_sender
from Store_Function.Device_Info import device_data

def mqtt_uplink_message_handler(client, userdata, msg):
    try:
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
        utcTime = parser.isoparse(uplinkData.get("received_at", "1970-01-01T00:00:00Z"))
        uplinkDataHeader = decodedUplinkPayload.get("dataType", "N/A")

        if uplinkDataHeader == "0x01":
            device_data[deviceId]["count"] += 1
            device_data[deviceId]["last_payload"] = decodedUplinkPayload
            device_data[deviceId]["last_time"] = utcTime
            device_data[deviceId]["on_line"] = True

            count = device_data[deviceId]["count"]
            temperature = decodedUplinkPayload.get('temperature', 'N/A')
            averageTemperature = decodedUplinkPayload.get('averageTemperature', 'N/A')
            humidity = decodedUplinkPayload.get('humidity', 'N/A')
            pressure = decodedUplinkPayload.get('pressure', 'N/A')
            print(f"[{deviceId}] Count={count}, Header=0x{uplinkDataHeader}, Temp={temperature}°C, AvrTemp={averageTemperature}°C, Humidity={humidity}%, Pressure={pressure}hPa")

            if count % 3 == 0 or count == 1:
                mqtt_downlink_message_sender(client, deviceId, count)

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
