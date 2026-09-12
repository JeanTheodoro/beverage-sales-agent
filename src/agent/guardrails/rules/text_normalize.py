import re
import unicodedata


def normalize(text: str) -> str:
    """
    Normaliza texto para facilitar a detecção de padrões.

    Operações:
    - converte para lowercase;
    - remove acentos;
    - normaliza espaços;
    - remove caracteres de controle.
    """

    if not text:
        return ""

    text = text.lower().strip()

    # Remove acentos.
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    # Remove caracteres de controle.
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)

    # Normaliza espaços.
    text = re.sub(r"\s+", " ", text)

    return text

