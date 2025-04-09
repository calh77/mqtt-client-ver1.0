# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-08 15:28:08
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 16:42:53
import tkinter as tk
from tkinter import scrolledtext
import queue

class DeviceDisplayManager:
    """
    각 디바이스 ID 별로 별도 tkinter Toplevel 윈도우와
    텍스트 영역(ScrolledText)을 관리하면서
    Queue에 들어온 데이터(센서값)를 주기적으로 창에 표시해주는 매니저 클래스
    """

    def __init__(self):
        self.windows = {}  # {device_id: (window, text_area)}
        self.queues = {}   # {device_id: queue.Queue()}

    def create_or_update_window(self, device_id, data):
        # 만약 해당 device_id에 대한 창이 없다면 먼저 생성
        if device_id not in self.windows:
            self._create_window(device_id)
        # 해당 device_id의 큐에 데이터 저장
        self.queues[device_id].put(data)

    def _create_window(self, device_id):
        window = tk.Toplevel()
        window.title(f"Device: {device_id}")
        window.geometry("400x300")

        text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled')
        text_area.pack(expand=True, fill='both')

        q = queue.Queue()
        self.windows[device_id] = (window, text_area)
        self.queues[device_id] = q

        def process_queue():
            try:
                while True:
                    data = q.get_nowait()
                    text_area.configure(state='normal')
                    text_area.insert(tk.END, data + "\n")
                    text_area.see(tk.END)
                    text_area.configure(state='disabled')
            except queue.Empty:
                pass
            window.after(100, process_queue)  # 100ms마다 재호출

        window.after(100, process_queue)  # 초기 호출


    def _update_window(self, device_id):
        window, text_area = self.windows[device_id]
        q = self.queues[device_id]

        def process_queue():
            # 큐에 쌓인 데이터 모두 처리
            while not q.empty():
                data = q.get_nowait()
                text_area.configure(state='normal')
                text_area.insert(tk.END, data + "\n")
                text_area.see(tk.END)
                text_area.configure(state='disabled')
            # 일정 주기로 다시 큐를 확인
            window.after(100, process_queue)

        # 최초 1회 실행
        window.after(100, process_queue)


# 👇 전역 인스턴스 및 함수 정의 추가
display_manager = DeviceDisplayManager()

def display_sensor_data(device_id, temperature, average_temp, humidity, pressure):
    """
    센서 데이터를 받아 디바이스 별 창에 출력하는 함수.

    :param device_id: 각 디바이스를 식별하기 위한 ID
    :param temperature: 현재 온도
    :param average_temp: 평균 온도
    :param humidity: 습도
    :param pressure: 기압
    """
    msg = f"Temp={temperature}°C, AvrTemp={average_temp}°C, Humidity={humidity}%, Pressure={pressure}hPa"
    display_manager.create_or_update_window(device_id, msg)


    # ✅ 메인 루프 실행 (필수!)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 루트 창을 숨김 (필요시 표시 가능)

    # 테스트 데이터 전송
    display_sensor_data("Device_001", 25.3, 24.1, 45, 1013)
    display_sensor_data("Device_002", 26.5, 25.0, 50, 1012)
    
    root.mainloop()  # 이벤트 루프 시작
