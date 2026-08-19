import json
import logging

from django.conf import settings
from google import genai
from google.genai import types

from .calculos import calcular_metas_completas


logger = logging.getLogger(__name__)


# Cliente da API Gemini
client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# Modelo utilizado
MODEL_NAME = 'gemini-3.6-flash'


def montar_prompt(perfil, metas):
    """
    Monta o prompt em texto a partir do PerfilDieta
    e das metas nutricionais calculadas.
    """

    restricao = perfil.get_restricao_alimentar_display()

    if (
        perfil.restricao_alimentar == 'outra'
        and perfil.restricao_outra_descricao
    ):
        restricao = perfil.restricao_outra_descricao


    return f"""
Você é um nutricionista experiente.

Monte um cardápio diário completo, dividido em
{perfil.refeicoes_por_dia} refeições.

As metas de calorias e macronutrientes abaixo JÁ FORAM CALCULADAS
e devem ser respeitadas com margem de até 5%.

Distribua os alimentos entre as refeições para se aproximar dessas
metas. Não recalcule nem substitua as metas informadas.


DADOS DA PESSOA:

- Peso: {perfil.peso} kg
- Altura: {perfil.altura} m
- Idade: {perfil.idade} anos
- Gênero: {perfil.get_genero_display()}
- Nível de atividade: {perfil.get_nivel_atividade_display()}
- Objetivo: {perfil.get_objetivo_display()}
- Restrição alimentar: {restricao}
- Alergias: {perfil.alergias or 'nenhuma informada'}
- Alimentos que prefere evitar:
  {perfil.alimentos_que_nao_gosta or 'nenhum informado'}
- Condições de saúde:
  {perfil.condicoes_saude or 'nenhuma informada'}
- Orçamento semanal:
  R$ {perfil.orcamento_semanal}


REGRAS IMPORTANTES:

- Nunca inclua alimentos relacionados às alergias informadas.
- Respeite as restrições alimentares.
- Evite alimentos que a pessoa informou não gostar.
- Considere as condições de saúde informadas.
- Priorize alimentos acessíveis e comuns no Brasil.
- Considere o orçamento semanal informado.
- Evite alimentos caros ou importados quando existir alternativa
  nutricionalmente semelhante e mais acessível.
- Distribua as calorias e macronutrientes entre as refeições.
- Use quantidades realistas de alimentos.


METAS DIÁRIAS:

- Calorias: {metas['calorias_alvo']} kcal
- Proteína: {metas['proteina_g']} g
- Carboidrato: {metas['carboidrato_g']} g
- Gordura: {metas['gordura_g']} g


Responda em português do Brasil.

Retorne SOMENTE um JSON válido seguindo exatamente esta estrutura:

{{
    "refeicoes": [
        {{
            "nome": "Café da manhã",
            "horario_sugerido": "07:00",

            "alimentos": [
                {{
                    "item": "Ovos mexidos",
                    "quantidade": "3 unidades",
                    "calorias": 210
                }}
            ],

            "calorias_refeicao": 210
        }}
    ],

    "resumo_diario": {{
        "calorias": {metas['calorias_alvo']},
        "proteina_g": {metas['proteina_g']},
        "carboidrato_g": {metas['carboidrato_g']},
        "gordura_g": {metas['gordura_g']}
    }},

    "estimativa_custo_semanal":
        "estimativa em R$ dos alimentos sugeridos",

    "observacoes":
        "orientações gerais, substituições possíveis e cuidados"
}}

Não escreva nenhum texto antes ou depois do JSON.
""".strip()


def gerar_dieta_ia(perfil):
    """
    Recebe um PerfilDieta.

    1. Calcula as metas nutricionais.
    2. Monta o prompt.
    3. Envia o prompt ao Gemini.
    4. Converte a resposta JSON.
    5. Retorna:

       (
           metas,
           texto_bruto,
           dados_json
       )
    """

    # ===============================
    # CALCULAR METAS
    # ===============================

    metas = calcular_metas_completas(perfil)


    # ===============================
    # MONTAR PROMPT
    # ===============================

    prompt = montar_prompt(
        perfil,
        metas
    )


    # ===============================
    # CHAMAR GEMINI
    # ===============================

    try:

        resposta = client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(
                response_mime_type='application/json'
            )
        )


        texto = resposta.text


        if not texto:
            raise ValueError(
                'O Gemini retornou uma resposta vazia.'
            )


    except Exception:

        logger.exception(
            'Erro ao chamar a API do Gemini para gerar dieta'
        )

        raise


    # ===============================
    # CONVERTER PARA JSON
    # ===============================

    dados_json = None


    try:

        texto_limpo = texto.strip()


        # Segurança adicional caso venha
        # ```json ... ```
        if texto_limpo.startswith('```json'):
            texto_limpo = texto_limpo[7:]

        elif texto_limpo.startswith('```'):
            texto_limpo = texto_limpo[3:]


        if texto_limpo.endswith('```'):
            texto_limpo = texto_limpo[:-3]


        texto_limpo = texto_limpo.strip()


        dados_json = json.loads(
            texto_limpo
        )


    except json.JSONDecodeError:

        logger.warning(
            'A resposta do Gemini não veio em JSON válido. '
            'Será salvo apenas o texto bruto.'
        )


    return (
        metas,
        texto,
        dados_json
    )