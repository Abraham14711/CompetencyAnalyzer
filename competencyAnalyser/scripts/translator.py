import importlib
from typing import Any, Dict
from googletrans import Translator

from competencyAnalyser.scripts.ai import ai_translate_text


class TranslatorI18n:
    _instances: Dict[str, 'TranslatorI18n'] = {}

    def __new__(cls, lang: str) -> 'TranslatorI18n':
        if lang not in cls._instances:
            cls._instances[lang] = super(TranslatorI18n, cls).__new__(cls)
        return cls._instances[lang]

    def __init__(self, lang: str):
        self.lang = lang

    def t(self, key: str, **kwargs: Dict[str, Any]) -> str:
        file_key, *translation_keys = key.split('.')

        locale_module = importlib.import_module(
            f'competencyAnalyser.languages'
            f'.{self.lang}.{file_key}')
        translation = locale_module.locale
        for translation_key in translation_keys:
            translation = translation.get(translation_key, None)
            if translation is None:
                return f'Key {key} not found in {self.lang} locale'
        if kwargs.keys():
            translation = translation.format(**kwargs)

        return translation

    def translate_text(self, text: str) -> str:
        if self.lang == 'ru':
            return text
        else:
            translator = Translator()
            return translator.translate(text, dest=self.lang).text
