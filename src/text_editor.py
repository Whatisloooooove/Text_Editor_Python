import tkinter as tk
import json
import os
from tkinter import messagebox
from src.file_editor import FileEditor
from src.syntax_highlighter import SyntaxHighlighter


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title('Текстовый редактор')
        self.root.geometry('960x1080')

        self.main_menu = tk.Menu(root)
        self.main_menu.config(bg="#434144")

        self.f_text = tk.Frame(root)
        self.f_text.pack(fill=tk.BOTH, expand=1)

        self.current_language = "python"
        self.add_text_field()
        self.add_scroll()
        self.view_data()
        self.file_editor = FileEditor(self.text_field)
        self.syntax_highlighter = SyntaxHighlighter(self.text_field, self)
        self.create_menu()
        self.add_keys()

    def add_text_field(self):
        self.text_field = tk.Text(self.f_text,
                                  bg='#2d2a2e',
                                  fg='white',
                                  padx=10,
                                  pady=10,
                                  wrap=tk.WORD,
                                  insertbackground='white',
                                  selectbackground='#808080',
                                  spacing3=10, width=30,
                                  font='Arial 14 bold')
        self.text_field.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)
        self.text_field.config(highlightthickness=0)

    def add_scroll(self):
        self.scroll = tk.Scrollbar(self.f_text,
                                   command=self.text_field.yview,
                                   troughcolor="#2d2a2e",
                                   width=20, relief="flat",
                                   bg="#434144",
                                   activebackground="#4c4a4d",
                                   highlightthickness=0
                                   )
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.text_field.config(yscrollcommand=self.scroll.set)

    def add_keys(self):
        # Добавляю кнопки для перемещения по тексту
        self.root.bind("<Left>",
                       lambda event: self.file_editor.move_cursor_left())
        self.root.bind("<Right>",
                       lambda event: self.file_editor.move_cursor_right())
        self.root.bind("<Home>",
                       lambda event: self.file_editor.move_to_start_of_line())
        self.root.bind("<End>",
                       lambda event: self.file_editor.move_to_end_of_line())

        # Добавляю хоткеи для сохранения,открытия и выхода
        self.root.bind("<Control-s>",
                       lambda event: self.file_editor.save_file())
        self.root.bind("<Control-o>",
                       lambda event: self.file_editor.open_file())
        self.root.bind("<Control-q>", lambda event: self.button_exit())

        # Хоткеи для удаления строки/слов, выделения текста и поиска по тексту
        self.root.bind("<Control-d>",
                       lambda event: self.file_editor.delete_line())
        self.root.bind("<Control-w>",
                       lambda event: self.file_editor.delete_word())
        self.root.bind("<Control-a>",
                       lambda event: self.file_editor.select_all())
        self.root.bind("<Control-f>",
                       lambda event: self.show_search_replace_dialog())

        # Делаю так , чтобы слово подсвечивалось сразу после ввода
        self.text_field.bind(
            '<KeyRelease>',
            lambda event: self.syntax_highlighter.load_language(
                self.current_language))

    def create_menu(self):
        self.root.config(bg="#434144", menu=self.main_menu)
        self.create_file_menu()
        self.create_view_menu()
        self.create_search_and_replace()
        self.create_syntax_highlight()

    def create_file_menu(self):
        file_menu = tk.Menu(self.main_menu, tearoff=0)
        file_menu.add_command(
            label='Открыть',
            command=self.file_editor.open_file)
        file_menu.add_command(
            label='Сохранить',
            command=self.file_editor.save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Закрыть', command=self.button_exit)
        file_menu.configure(bg='#434144')

        file_menu.entryconfig(
            "Открыть",
            background='#434144',
            foreground='white')
        file_menu.entryconfig(
            "Сохранить",
            background='#434144',
            foreground='white')
        file_menu.entryconfig(
            "Закрыть",
            background='#434144',
            foreground='white')

        self.main_menu.add_cascade(label='File', menu=file_menu)
        self.main_menu.entryconfig('File', foreground='white')

    def create_view_menu(self):
        view_menu = tk.Menu(self.main_menu, tearoff=0)
        self.create_view_sub(view_menu)
        self.create_font_sub(view_menu)

        self.main_menu.add_cascade(label='View', menu=view_menu)
        self.main_menu.entryconfig('View', foreground='white')

    # Выбор шрифта
    def create_font_sub(self, view_menu):
        font_menu_sub = tk.Menu(view_menu, tearoff=0)
        font_menu_sub.add_command(label='Arial',
                                  command=lambda: self.change_font('Arial'))
        font_menu_sub.add_command(
            label='ComicSans MS',
            command=lambda: self.change_font('ComicSans MS'))
        font_menu_sub.add_command(
            label='Times New Roman',
            command=lambda: self.change_font('Times New Roman'))

        font_menu_sub.entryconfig(
            'Arial',
            background='#434144',
            foreground='white')
        font_menu_sub.entryconfig(
            'ComicSans MS',
            background='#434144',
            foreground='white')
        font_menu_sub.entryconfig(
            'Times New Roman',
            background='#434144',
            foreground='white')

        view_menu.add_cascade(label='Шрифт', menu=font_menu_sub)
        view_menu.entryconfig(
            'Шрифт',
            background='#434144',
            foreground='white')

    # Выбор темы
    def create_view_sub(self, view_menu):
        view_menu_sub = tk.Menu(view_menu, tearoff=0)
        view_menu_sub.add_command(
            label='Тёмная тема',
            command=lambda: self.change_theme('dark'))
        view_menu_sub.add_command(
            label='Светлая тема',
            command=lambda: self.change_theme('light'))

        view_menu_sub.entryconfig(
            'Светлая тема',
            background='#434144',
            foreground='white')
        view_menu_sub.entryconfig(
            'Тёмная тема',
            background='#434144',
            foreground='white')

        view_menu.add_cascade(label='Тема', menu=view_menu_sub)
        view_menu.entryconfig('Тема', background='#434144', foreground='white')

    def create_search_and_replace(self):
        search_replace_menu = tk.Menu(self.main_menu, tearoff=0)
        search_replace_menu.add_command(
            label='Найти и заменить',
            command=self.show_search_replace_dialog)
        search_replace_menu.entryconfig(
            'Найти и заменить',
            background='#434144',
            foreground='white')
        self.main_menu.add_cascade(
            label='Search and replace',
            menu=search_replace_menu)
        self.main_menu.entryconfig('Search and replace', foreground='white')

    def create_syntax_highlight(self):
        language_menu = tk.Menu(self.main_menu, tearoff=0)
        script_directory = os.path.dirname(__file__)
        config_file_path = os.path.join(script_directory, 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
            for language in config["languages"]:
                language_menu.add_command(
                    label=f'{language}',
                    command=lambda lang=language: self.change_language(lang))
                language_menu.entryconfig(
                    f'{language}', background='#434144', foreground='white')
        self.main_menu.add_cascade(label='Language', menu=language_menu)
        self.main_menu.entryconfig('Language', foreground='white')

    def view_data(self):
        self.view_colour = {
            'dark': {
                'text_bg': '#2d2a2e',
                'text_fg': 'white',
                'cursor': 'white',
                'select': '#434144'
            },
            'light': {
                'text_bg': '#F2F3F4',
                'text_fg': 'black',
                'cursor': 'black',
                'select': '#434144'
            }
        }

        self.fonts = {
            'Arial': {
                'font': 'Arial 14 bold'
            },
            'ComicSans MS': {
                'font': ('ComicSans MS', 14, 'bold')
            },
            'Times New Roman': {
                'font': ('Times New Roman', 14, 'bold')
            }
        }

    # Метод для изменения темы
    def change_theme(self, theme):
        self.text_field['bg'] = self.view_colour[theme]['text_bg']
        self.text_field['fg'] = self.view_colour[theme]['text_fg']
        self.text_field['insertbackground'] = self.view_colour[theme]['cursor']
        self.text_field['selectbackground'] = self.view_colour[theme]['select']

        scrollbar_troughcolor = "#434144" if theme == "dark" else "white"
        self.scroll.config(troughcolor=scrollbar_troughcolor)

        scrollbar_bg = "#434144" if theme == "dark" else "gray"
        self.scroll.config(bg=scrollbar_bg)

        menu_bg = "#434144" if theme == "dark" else "gray"
        self.main_menu.config(bg=menu_bg)

    # Метод для изменения шрифта
    def change_font(self, sel_font):
        self.text_field['font'] = self.fonts[sel_font]['font']

    # Метод для завершения программы
    def button_exit(self):
        answer = messagebox.askokcancel('Выход', 'Выйти из программы')
        if answer:
            self.root.destroy()

    # Метод для вызова окна поиска и замены
    def show_search_replace_dialog(self):
        # Окно для поиска и замены
        search_replace_window = tk.Toplevel(self.root)
        search_replace_window.title('Найти и Заменить')

        # Текстовые поля и кнопки для ввода слов для поиска и замены
        search_label = tk.Label(search_replace_window, text='Найти:')
        search_label.pack()
        search_entry = tk.Entry(search_replace_window)
        search_entry.pack()
        replace_label = tk.Label(search_replace_window, text='Заменить на:')
        replace_label.pack()
        replace_entry = tk.Entry(search_replace_window)
        replace_entry.pack()
        search_button = tk.Button(search_replace_window,
                                  text='Найти и Заменить',
                                  command=lambda: self.perform_search_replace(
                                      search_entry.get(),
                                      replace_entry.get()))
        search_button.pack()

    # Метод для выполнения поиска и замены
    def perform_search_replace(self, search_text, replace_text):
        file_editor = FileEditor(self.text_field)
        file_editor.search_replace(search_text, replace_text)

    # Смена текущего ЯП
    def change_language(self, new_language):
        self.current_language = new_language
        self.syntax_highlighter.load_language(new_language)

    def run(self, root):
        root.mainloop()
