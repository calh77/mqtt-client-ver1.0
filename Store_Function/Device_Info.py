# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-09 09:03:50
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 11:06:45
from collections import defaultdict

device_data = defaultdict(lambda: {
    "count": 0,
    "last_payload": {},
    "last_time": None,
    "on_line": False
})

