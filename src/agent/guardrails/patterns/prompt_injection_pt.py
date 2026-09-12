PT_INJECTION_PATTERNS = [

    # ============================================================
    # IGNORAR INSTRUÇÕES ANTERIORES
    # ============================================================

    (
        r"\b(ignore|ignora|esqueca|desconsidere|"
        r"desconsidera)\b.{0,50}"
        r"\b(instrucoes|regras|comandos|prompt|ordens)\b"
        r".{0,30}"
        r"\b(anteriores|acima|do\s+sistema)?\b"
    ),

    # ============================================================
    # MUDANÇA DE PAPEL / PERSONA
    # ============================================================

    (
        r"\b(voce\s+(agora\s+)?e|aja\s+como|"
        r"finja\s+ser|atue\s+como)\b.{0,50}"
        r"\b(um|uma)?\b.{0,30}"
        r"\b(assistente|ia|ai|modelo)\b.{0,30}"
        r"\b(sem\s+restricoes|sem\s+regras|"
        r"sem\s+filtros|livre)\b"
    ),

    # ============================================================
    # EXTRAÇÃO DE PROMPT DE SISTEMA
    # ============================================================

    (
        r"\b(mostre|revele|repita|exiba|qual\s+e)\b"
        r".{0,50}"
        r"\b(seu|o)\b.{0,20}"
        r"\b(prompt|instrucoes)\s+"
        r"(de\s+)?(sistema|inicial)\b"
    ),

    # ============================================================
    # INSTRUÇÕES EMBUTIDAS / FALSO SISTEMA
    # ============================================================

    (
        r"\b(sistema|system|admin|desenvolvedor|dev)"
        r"\s*[:\-]\s*"
        r"\b(desconsidere|ignore|defina|altere|aplique)\b"
    ),

    # ============================================================
    # OVERRIDE DIRETO
    # ============================================================

    (
        r"\b(nova\s+instrucao|novo\s+comando|"
        r"substitua\s+(a|as)\s+instrucao)\b"
    ),

    # ============================================================
    # REMOÇÃO DE RESTRIÇÕES
    # ============================================================

    (
        r"\bvoce\s+nao\s+tem\s+(mais\s+)?restricoes\b"
    ),

    # ============================================================
    # MANIPULAÇÃO DE PREÇO
    # ============================================================

    (
        r"\b(defina|altere|mude|force)\b.{0,30}"
        r"\b(preco|desconto|valor)\b.{0,30}"
        r"\b(para|como)\b.{0,20}"
        r"(r\$\s*0|gratis|zero|0[,.]0+)"
    ),
]

