import tkinter as tk

def create_text_output_frame(master):
    """
    센서 데이터를 출력하는 텍스트 박스를 포함한 프레임을 생성하여 반환합니다.

    :param master: 상위 tkinter 위젯(예: window)
    :return: text_frame, text_box
    """
    text_frame = tk.Frame(master)
    text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    text_box = tk.Text(text_frame, height=10, font=("Consolas", 11))
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(text_frame, command=text_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_box.config(yscrollcommand=scrollbar.set)

    return text_frame, text_box     # ← 여기서 text_box가 필요한 곳에 쓰이게 됩니다
