EN_INJECTION_PATTERNS = [

    # ============================================================
    # IGNORE PREVIOUS INSTRUCTIONS
    # ============================================================

    (
        r"\b(ignore|disregard|forget)\b.{0,50}"
        r"\b(previous|prior|above|all)\b.{0,30}"
        r"\b(instructions|rules|prompt|commands)\b"
    ),

    # ============================================================
    # ROLE / PERSONA OVERRIDE
    # ============================================================

    (
        r"\b(you\s+are\s+now|act\s+as|"
        r"pretend\s+(to\s+be|you\s+are)|behave\s+as)\b"
        r".{0,50}"
        r"\b(an?\s+)?"
        r"\b(assistant|ai|model)\b.{0,30}"
        r"\b(with\s+no\s+restrictions|unrestricted|"
        r"without\s+rules|free)\b"
    ),

    # ============================================================
    # SYSTEM PROMPT EXTRACTION
    # ============================================================

    (
        r"\b(show|reveal|repeat|print|what\s+is)\b"
        r".{0,50}"
        r"\b(your|the)\b.{0,20}"
        r"\b(system\s+prompt|initial\s+instructions)\b"
    ),

    # ============================================================
    # FAKE SYSTEM INSTRUCTIONS
    # ============================================================

    (
        r"\b(system|admin|developer|dev)"
        r"\s*[:\-]\s*"
        r"\b(disregard|ignore|set|change|apply)\b"
    ),

    # ============================================================
    # DIRECT OVERRIDE
    # ============================================================

    (
        r"\b(new\s+instruction|new\s+command|"
        r"override\s+(the\s+)?instructions?)\b"
    ),

    # ============================================================
    # REMOVE RESTRICTIONS
    # ============================================================

    (
        r"\byou\s+(no\s+longer\s+)?have\s+no\s+restrictions\b"
    ),

    # ============================================================
    # PRICE / DISCOUNT MANIPULATION
    # ============================================================

    (
        r"\b(set|change|force)\b.{0,30}"
        r"\b(price|discount|value)\b.{0,30}"
        r"\b(to|as)\b.{0,20}"
        r"(\$?\s*0|free|zero)"
    ),
]
