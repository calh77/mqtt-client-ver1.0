# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-29 12:54:54
# @Last Modified by:   Your name
# @Last Modified time: 2025-05-09 15:17:58
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker


def create_text_and_graph_frame(master, device_id, device_text_boxes, device_graphs, max_devices=10):
    """
    특정 디바이스 ID를 위한 텍스트 박스를 포함한 프레임을 생성하여 반환합니다.
    (디바이스별 Text Box를 생성하고, dict에 저장합니다.)

    :param master: 상위 tkinter 위젯 (예: root)
    :param device_id: 생성할 디바이스 ID (예: 'device001')
    :param device_text_boxes: 디바이스별 텍스트박스를 저장하는 dict
    :param max_devices: 최대 생성할 수 있는 디바이스 수
    :return: text_frame, text_box
    """
    if device_id in device_text_boxes:
        # 이미 있으면 새로 안 만든다
        return None, device_text_boxes[device_id]

    if len(device_text_boxes) >= max_devices:
        print(f"최대 {max_devices}개의 디바이스만 지원합니다.")
        return None, None

    # Frame 생성
    frame = tk.Frame(master)
    frame.pack(side=tk.TOP, fill=tk.X, expand=False, pady=5)

    label = tk.Label(frame, text=f"Device: {device_id}", font=("Consolas", 10, "bold"))
    label.pack(anchor="w", padx=5)

    # Text 박스
    text_box = tk.Text(frame, height=6, font=("Consolas", 10))
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0))

#    scrollbar = tk.Scrollbar(frame, command=text_box.yview)
#    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#    text_box.config(yscrollcommand=scrollbar.set)

    # 생성한 text_box를 dict에 등록
    device_text_boxes[device_id] = text_box
    return frame, text_box


def update_device_o2_graph(device_id, value, device_graphs):
    if device_id not in device_graphs:
        return

    o2_graph_info = device_graphs[device_id]["o2"]

    # 데이터 추가
    o2_graph_info["data_x"].append(len(o2_graph_info["data_x"]))  # 시간 대신 카운트
    o2_graph_info["data_y"].append(value)
    print(f"O2 : {value:.3f}\n")


    # 최근 50개만 유지 (메모리 폭발 방지)
    if len(o2_graph_info["data_x"]) > 50:
        o2_graph_info["data_x"] = o2_graph_info["data_x"][-50:]
        o2_graph_info["data_y"] = o2_graph_info["data_y"][-50:]

    # 그래프 업데이트
    o2_graph_info["ax"].clear()
    o2_graph_info["ax"].plot(o2_graph_info["data_x"], o2_graph_info["data_y"], label="O2", color="blue")
    o2_graph_info["ax"].set_title("O2 Voltage")
    o2_graph_info["ax"].set_ylim(0.000, 2.000)
    o2_graph_info["ax"].yaxis.set_major_formatter(ticker.FormatStrFormatter("%.3f"))
    o2_graph_info["ax"].xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    o2_graph_info["fig"].subplots_adjust(left=0.2)

    o2_graph_info["canvas"].draw()


def update_device_ch4_graph(device_id, value, device_graphs):
    if device_id not in device_graphs:
        return

    ch4_graph_info = device_graphs[device_id]["ch4"]

    # 데이터 추가
    ch4_graph_info["data_x"].append(len(ch4_graph_info["data_x"]))  # 시간 대신 카운트
    ch4_graph_info["data_y"].append(value)
    print(f"CH4 : {value:d}\n")


    # 최근 50개만 유지 (메모리 폭발 방지)
    if len(ch4_graph_info["data_x"]) > 50:
        ch4_graph_info["data_x"] = ch4_graph_info["data_x"][-50:]
        ch4_graph_info["data_y"] = ch4_graph_info["data_y"][-50:]

    # 그래프 업데이트
    ch4_graph_info["ax"].clear()
    ch4_graph_info["ax"].plot(ch4_graph_info["data_x"], ch4_graph_info["data_y"], label="CH4", color="blue")
    ch4_graph_info["ax"].set_title("CH4 Concentration")
    ch4_graph_info["ax"].set_ylim(0, 4500)
    ch4_graph_info["ax"].yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ch4_graph_info["ax"].xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ch4_graph_info["fig"].subplots_adjust(left=0.2)

    ch4_graph_info["canvas"].draw()
