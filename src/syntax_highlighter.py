import tkinter as tk
import json
import os
import re


class SyntaxHighlighter:
    def __init__(self, text_field, text_editor):
        self.text_field = text_field
        self.language_rules = {}
        self.text_editor = text_editor

    def load_language(self, language):
        script_directory = os.path.dirname(__file__)
        config_file_path = os.path.join(script_directory, 'config.json')
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
            if language in config['languages']:
                self.language_rules[language] = config['languages'][language]
                self.highlight_syntax(language)

    def highlight_syntax(self, language):
        self.clear_tags()
        self.text_editor.current_language = language
        rules = self.language_rules[language]
        self.highlight_items(
            rules['operators'],
            rules['styles']['operators'],
            'operator')
        self.highlight_items(
            rules['keywords'],
            rules['styles']['keywords'],
            'keyword')
        self.highlight_items(
            rules['builtins'],
            rules['styles']['builtins'],
            'builtin')

    def highlight_items(self, items, style, tag_name):
        for item in items:
            start = '1.0'
            while True:
                start = self.text_field.search(
                    rf'{re.escape(item)}',
                    start, tk.END,
                    regexp=True
                )
                if not start:
                    break
                end = f"{start}+{len(item)}c"
                self.text_field.tag_add(tag_name, start, end)
                self.text_field.tag_config(tag_name, **style)
                start = end

    # Очистка правил подсветки после смены языка
    def clear_tags(self):
        for tag in self.text_field.tag_names():
            self.text_field.tag_delete(tag)
