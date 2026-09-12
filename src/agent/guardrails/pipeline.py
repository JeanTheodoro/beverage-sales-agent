from agent.guardrails.rules.base_rule import GuardrailRule
from agent.guardrails.rules.human import HumanRule
from agent.guardrails.rules.prompt_injection import PromptInjectionRule

from schemas.guardrail import (
    GuardrailDecision,
    GuardrailResult,
)


class GuardrailPipeline:
    """
    Executa as regras de guardrail em ordem.

    A primeira regra que gerar BLOCK ou HUMAN
    interrompe a execução.
    """

    def __init__(self) -> None:
        self.rules: list[GuardrailRule] = [
            PromptInjectionRule(),
            HumanRule(),
        ]

    def evaluate(self, message: str) -> GuardrailResult:

        for rule in self.rules:

            result = rule.evaluate(message)

            if result.decision in {
                GuardrailDecision.BLOCK,
                GuardrailDecision.HUMAN,
            }:
                return result

        return GuardrailResult(
            decision=GuardrailDecision.ALLOW,
            reason="Nenhuma regra acionada.",
            category="SAFE",
        )

