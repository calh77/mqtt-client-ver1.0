# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2025-04-09 17:05:42
# @Last Modified by:   Your name
# @Last Modified time: 2025-04-09 17:06:12
import sys
import tkinter as tk

class stdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

def redirect_stdout_to(text_widget):
    sys.stdout = stdoutRedirector(text_widget)
