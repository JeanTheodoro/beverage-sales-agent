from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GuardrailDecision(Enum):
    BLOCK = "block"
    HUMAN = "human"
    ALLOW = "allow"


@dataclass
class GuardrailResult:
    decision: GuardrailDecision
    category: Optional[str] = None
    reason: Optional[str] = None

