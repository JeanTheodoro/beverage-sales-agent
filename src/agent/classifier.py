import logging

from typing import Any, Dict, List, Optional

from langfuse import observe

from agent.prompts.system_prompt import SYSTEM_PROMPT
from agent.provider.llm_provider import llm_provider
from schemas.nlu import ClassificationResult


logger = logging.getLogger("bar_do_jaum")


class Classifier:

    @staticmethod
    @observe(name="classifier")
    async def classify_message(
        raw_message: str,
        history: Optional[List[Dict[str, str]]] = None,
        session_state: Optional[Dict[str, Any]] = None,
    ) -> ClassificationResult:

        logger.info(
            f"Iniciando classificação com provedor: "
            f"{llm_provider.provider} "
            f"(modelo: {llm_provider.model})"
        )

        formatted_history = "Nenhum histórico anterior."

        if history:
            history_lines = [
                f"- {msg.get('role', 'user').upper()}: "
                f"{msg.get('content', '')}"
                for msg in history
            ]

            formatted_history = "\n".join(history_lines)

        session_state = session_state or {}

        formatted_state = f"""
        - Nome Cadastrado: {session_state.get('customer_name') or 'None'}
        - Endereço Cadastrado: {session_state.get('address') or 'None'}
        - Método de Pagamento: {session_state.get('payment_method') or 'None'}
        - Troco para: {session_state.get('cash_received') or 'None'}
        """

        user_content = f"""
        HISTÓRICO RECENTE DA CONVERSA:

        {formatted_history}

        ESTADO ATUAL DO CADASTRO DO CLIENTE NA SESSÃO:

        {formatted_state}

        ÚLTIMA MENSAGEM DO CLIENTE:

        "{raw_message}"
        """

        try:

            result = await (
                llm_provider.client.chat.completions.create(
                    model=llm_provider.model,
                    response_model=ClassificationResult,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": user_content,
                        },
                    ],
                    temperature=0.0,
                )
            )

            logger.info(
                f"[CLASSIFIER] Intent detectada: "
                f"{result.intent}"
            )

            return result

        except Exception as error:

            logger.error(
                "[CLASSIFIER] Erro detalhado na classificação",
                exc_info=True,
            )

            raise ValueError(
                "Não consegui processar as informações, "
                "tente novamente"
            ) from error