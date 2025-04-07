# -*- coding: utf-8 -*-
# @Author: Chang SeungHyeock
# @Date:   2025-04-07 14:03:27
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-07 16:37:01
import json
import base64
from dateutil import parser
from collections import defaultdict

device_data = defaultdict(lambda: {
    "count": 0,
    "last_payload": {},
    "last_time": None
})


def mqtt_uplink_message_handler(client, msg):
    try:
        uplinkData = json.loads(msg.payload)
        if not uplinkData.get("uplink_message"):
            print("ignoring uplink message..")
            return
        
        device_info = uplinkData.get("end_device_ids", {})
        de