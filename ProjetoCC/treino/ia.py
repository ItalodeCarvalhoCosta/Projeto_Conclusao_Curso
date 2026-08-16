import json
import requests
from django.conf import settings


def montar_prompt(solicitacao):
    return f"""
Você é um personal trainer. Gere um plano de treino personalizado para a pessoa abaixo.

Dados:
- Peso: {solicitacao.peso} kg
- Altura: {solicitacao.altura} m
- Idade: {solicitacao.idade}
- Gênero biológico: {solicitacao.get_genero_display()}
- Percentual de gordura: {solicitacao.percentual_gordura or 'não informado'}
- Nível de experiência: {solicitacao.get_nivel_experiencia_display()}
- Objetivo principal: {solicitacao.get_objetivo_principal_display()}
- Frequência semanal: {solicitacao.frequencia_semanal}x por semana
- Tempo por sessão: {solicitacao.tempo_por_sessao} minutos
- Lesões/dores: {solicitacao.lesoes_dores or 'nenhuma'}

Responda APENAS com JSON puro, sem texto fora dele, no formato:
{{
  "nome": "string",
  "objetivo": "string",
  "nivel": "iniciante|intermediario|avancado",
  "exercicios": [
    {{"nome": "string", "series": int, "repeticoes": int}}
  ]
}}
"""


def chamar_ia(prompt):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
        },
        timeout=30,
    )
    response.raise_for_status()
    texto = response.json()["choices"][0]["message"]["content"]
    return json.loads(texto)