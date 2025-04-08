# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-08 15:28:08
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-08 15:54:23
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import queue

class DeviceDisplayManager:
    def __init__(self):
        self.windows = {}
        self.queues = {}

    def create_or_update_window(self, device_id, data):
        if device_id not in self.windows:
            self._create_window(device_id)
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

        # Start update thread
        thread = Thread(target=self._update_window, args=(device_id,), daemon=True)
        thread.start()

    def _update_window(self, device_id):
        window, text_area = self.windows[device_id]
        q = self.queues[device_id]

        def process_queue():
            while not q.empty():
                data = q.get_nowait()
                text_area.configure(state='normal')
                text_area.insert(tk.END, data + "\n")
                text_area.see(tk.END)
                text_area.configure(state='disabled')
            # 100ms 뒤에 다시 실행 (계속 큐 체크)
            window.after(100, process_queue)

        # 최초 실행
        window.after(100, process_queue)


# 👇 전역 인스턴스 및 함수 정의 추가
display_manager = DeviceDisplayManager()

def display_sensor_data(device_id, temperature, average_temp, humidity, pressure):
    msg = f"Temp={temperature}°C, AvrTemp={average_temp}°C, Humidity={humidity}%, Pressure={pressure}hPa"
    display_manager.create_or_update_window(device_id, msg)
