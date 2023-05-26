class LanguageCheck:
    LANGUAGES = {
        "EN-US": "English",
        "EN-GB": "English (British)",
        "ES": "Spanish",
        "ZH": "Chinese (Simplified)",
        "FR": "French",
        "UK": "Ukrainian",
        "BG": "Bulgarian",
        "CS": "Czech",
        "DA": "Danish",
        "DE": "German",
        "EL": "Greek",
        "ET": "Estonian",
        "FI": "Finnish",
        "HU": "Hungarian",
        "ID": "Indonesian",
        "IT": "Italian",
        "JA": "Japanese",
        "KO": "Korean",
        "LT": "Lithuanian",
        "LV": "Latvian",
        "NB": "Norwegian (Bokmål)",
        "NL": "Dutch",
        "PL": "Polish",
        "RO": "Romanian",
        "RU": "Russian",
        "SK": "Slovak",
        "SL": "Slovenian",
        "SV": "Swedish",
        "TR": "Turkish",
        "PT-BR": "Brazilian Portuguese",
        "PT-PT": "Portuguese"
    }

    def check_language(self: str):
        return LanguageCheck.LANGUAGES.get(self, "Unknown language")