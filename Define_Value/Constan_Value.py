# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-09 09:57:24
# @Last Modified by:   Your name
# @Last Modified time: 2025-05-07 15:09:26

class constantValue:
    def __init__(self):
        self.CHECK_INTERVAL = 60            # 센서 노드 연결을 확인하기 위한 주기 (sec)
        self.TIMEOUT_LIMIT = 200            # 센서 노드를 연결상테에 제거하기 위한 대기 시간

constant = constantValue()                  # 싱글톤 객체 생성