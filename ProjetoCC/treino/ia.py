import json
import logging

from django.conf import settings
from google import genai
from google.genai import types


logger = logging.getLogger(__name__)


# Cria o cliente do Gemini usando a chave definida no settings.py
client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# Modelo utilizado para gerar os treinos
MODEL_NAME = 'gemini-3.6-flash'


def montar_prompt(perfil):
    """
    Monta o texto que será enviado para a IA
    usando os dados do PerfilTreino.
    """

    return f"""
Você é um personal trainer experiente.

Monte um plano de treino semanal personalizado, dividido por dia,
com exercícios, séries, repetições e tempo de descanso.

Dados da pessoa:

- Peso: {perfil.peso} kg
- Altura: {perfil.altura} m
- Idade: {perfil.idade} anos
- Gênero: {perfil.get_genero_display()}
- Percentual de gordura: {perfil.percentual_gordura or 'não informado'}
- Nível de experiência: {perfil.get_nivel_experiencia_display()}
- Objetivo principal: {perfil.get_objetivo_display()}
- Problemas de saúde: {perfil.problemas_saude or 'nenhum informado'}
- Frequência semanal desejada: {perfil.frequencia_semanal} dias por semana
- Tempo disponível por sessão: {perfil.tempo_por_sessao} minutos
- Lesões ou dores: {perfil.lesoes_dores or 'nenhuma informada'}

Regras importantes:

- Leve em consideração o nível de experiência da pessoa.
- Respeite o tempo disponível por sessão.
- Respeite a quantidade de dias disponíveis na semana.
- Considere o objetivo principal.
- Leve em conta lesões, dores e problemas de saúde.
- Evite exercícios que possam agravar lesões ou problemas relatados.
- Distribua os grupos musculares de maneira equilibrada.
- Não coloque exercícios desnecessariamente avançados para iniciantes.

Responda em português do Brasil.

Retorne SOMENTE um JSON válido seguindo exatamente esta estrutura:

{{
    "dias": [
        {{
            "dia": "Dia 1 - Peito e Tríceps",
            "exercicios": [
                {{
                    "nome": "Supino reto",
                    "series": "4",
                    "repeticoes": "10-12",
                    "descanso": "60s"
                }}
            ]
        }}
    ],
    "observacoes": "Orientações gerais e cuidados."
}}

Não escreva nenhum texto antes ou depois do JSON.
""".strip()


def gerar_treino_ia(perfil):
    """
    Recebe um PerfilTreino e chama a API do Gemini.

    Retorna:

    (
        texto_bruto,
        dados_json
    )

    texto_bruto:
        resposta original da IA.

    dados_json:
        dicionário Python com o treino estruturado.

        Caso não seja possível converter a resposta
        para JSON, retorna None.
    """

    prompt = montar_prompt(perfil)

    try:

        resposta = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
            response_mime_type='application/json',

             automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
                    )
                )
            )

        texto = resposta.text

        if not texto:
            raise ValueError(
                'O Gemini retornou uma resposta vazia.'
            )

    except Exception:

        logger.exception(
            'Erro ao chamar a API do Gemini'
        )

        raise


    # =========================
    # CONVERTER RESPOSTA PARA JSON
    # =========================

    dados_json = None

    try:

        texto_limpo = texto.strip()

        # Segurança caso o modelo ainda envie ```
        if texto_limpo.startswith('```json'):
            texto_limpo = texto_limpo[7:]

        elif texto_limpo.startswith('```'):
            texto_limpo = texto_limpo[3:]

        if texto_limpo.endswith('```'):
            texto_limpo = texto_limpo[:-3]

        texto_limpo = texto_limpo.strip()

        dados_json = json.loads(texto_limpo)

    except json.JSONDecodeError:

        logger.warning(
            'Resposta do Gemini não veio em JSON válido. '
            'Salvando apenas o texto bruto.'
        )


    return texto, dados_json