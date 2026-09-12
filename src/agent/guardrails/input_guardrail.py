from agent.guardrails.pipeline import GuardrailPipeline
from schemas.guardrail import GuardrailResult


class InputGuardrail:
    # Instância única compartilhada em memória (evita overhead de recriar as regras toda vez)
    _pipeline = GuardrailPipeline()

    @classmethod
    def check(cls, message: str) -> GuardrailResult:
        """
        Executa todas as validações de entrada de forma estática/classe,
        reaproveitando o pipeline instanciado.
        """
        return cls._pipeline.evaluate(message)