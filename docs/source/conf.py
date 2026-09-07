# docs/source/conf.py

import os
import sys
from datetime import datetime

# Путь к проекту (чтобы Sphinx мог импортировать модули)
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------
project = 'Telegram Bot Calculator'
copyright = f'{datetime.now().year}, Твое имя'
author = 'Твое имя'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',      # Автоматическая документация из docstrings
    'sphinx.ext.viewcode',     # Добавляет ссылки на исходный код
    'sphinx.ext.napoleon',     # Поддержка Google и NumPy стилей
    'sphinx.ext.coverage',     # Проверка покрытия документации
    'sphinx.ext.intersphinx',  # Ссылки на другую документацию
]

# Путь к шаблонам
templates_path = ['_templates']
exclude_patterns = []

# Язык документации
language = 'ru'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Тема как у readthedocs.org
html_static_path = ['_static']
html_theme_options = {
    'navigation_depth': 4,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
}

# -- Options for autodoc ----------------------------------------------------
autodoc_member_order = 'bysource'  # Порядок как в коде
autodoc_typehints = 'description'  # Показывать type hints
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'show-inheritance': True,
}