from agent.guardrails.rules.base_rule import GuardrailRule
from schemas.guardrail import (
    GuardrailDecision,
    GuardrailResult,
)


class HumanRule(GuardrailRule):

    TRIGGERS = [
        "atendente",
        "atendimento humano",
        "falar com uma pessoa",
        "falar com humano",
        "quero falar com alguém",
        "quero falar com uma pessoa",
        "quero um atendente",
        "preciso de um atendente",
        "humano",
        "atendente humano",
    ]

    def evaluate(self, message: str) -> GuardrailResult:

        normalized = message.lower().strip()

        for trigger in self.TRIGGERS:

            if trigger in normalized:

                return GuardrailResult(
                    decision=GuardrailDecision.HUMAN,
                    reason=(
                        "Cliente solicitou atendimento humano."
                    ),
                )

        return GuardrailResult(
            decision=GuardrailDecision.ALLOW,
        )
