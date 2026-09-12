from abc import ABC, abstractmethod
from schemas.guardrail import GuardrailResult


class GuardrailRule(ABC):
    """
    Interface base para todas as regras de guardrail.
    """

    @abstractmethod
    def evaluate(self, message: str) -> GuardrailResult:
        """
        Avalia uma mensagem e retorna o resultado da regra.
        """
        raise NotImplementedError
