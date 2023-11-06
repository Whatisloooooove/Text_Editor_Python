import tkinter as tk
from tkinter import filedialog


class FileEditor:
    def __init__(self, text_field):
        self.text_field = text_field

    # Открытие файла
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title='Выбор файла',
            filetypes=(('Текстовые документы (*.txt)', '*.txt'),
                       ('Все файлы', '*.*')))
        if file_path:
            self.text_field.delete('1.0', tk.END)
            self.text_field.insert(
                '1.0', open(
                    file_path, encoding='utf-8').read())

    # Сохранение файла
    def save_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=(
            ('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        file = open(file_path, 'w', encoding='utf-8')
        text = self.text_field.get('1.0', tk.END)
        file.write(text)
        file.close()

    # Функция для перемещения на один символ влево
    def move_cursor_left(self):
        current_index = self.text_field.index("insert")
        line, col = map(int, current_index.split("."))
        if col > 0:
            new_index = f"{line}.{col}"
            self.text_field.mark_set("insert", new_index)
            self.text_field.see("insert")

    # Функция для перемещения на один символ вправо
    def move_cursor_right(self):
        current_index = self.text_field.index("insert")
        line, col = map(int, current_index.split("."))
        max_col = len(self.text_field.get(f"{line}.0", f"{line}.end-1c"))
        if col < max_col:
            new_index = f"{line}.{col}"
            self.text_field.mark_set("insert", new_index)
            self.text_field.see("insert")

    # Функция для перемещения в начало
    def move_to_start_of_line(self):
        self.text_field.mark_set("insert", "1.0")
        self.text_field.see("insert")

    # Функция для перемещения в конец
    def move_to_end_of_line(self):
        self.text_field.mark_set("insert", "end-1c")
        self.text_field.see("insert")

    # Фунция для удаления строки
    def delete_line(self):
        current_index = self.text_field.index("insert")
        line = int(current_index.split(".")[0])
        self.text_field.delete(f"{line}.0", f"{line + 1}.0")

    # Функция для удаления слова
    def delete_word(self):
        current_index = self.text_field.index("insert")
        line, col = map(int, current_index.split("."))
        current_line_text = self.text_field.get(f"{line}.0", f"{line}.end")

        start_col = col
        while start_col > 0 and current_line_text[start_col - 1].isalnum():
            start_col -= 1

        end_col = col
        while end_col < len(
                current_line_text) and current_line_text[end_col].isalnum():
            end_col += 1

        self.text_field.delete(f"{line}.{start_col}", f"{line}.{end_col}")

    def select_all(self):
        self.text_field.tag_add(tk.SEL, '1.0', tk.END)
        self.text_field.mark_set(tk.INSERT, '1.0')
        self.text_field.see(tk.INSERT)

    # Функция для поиска и замены
    def search_replace(self, search_text, replace_text):
        text = self.text_field.get('1.0', tk.END)

        updated_text = text.replace(search_text, replace_text)

        self.text_field.delete('1.0', tk.END)
        self.text_field.insert('1.0', updated_text)
