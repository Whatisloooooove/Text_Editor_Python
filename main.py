import tkinter as tk
from src.text_editor import TextEditor

if __name__ == '__main__':
    root = tk.Tk()
    TextEditor(root).run(root)
