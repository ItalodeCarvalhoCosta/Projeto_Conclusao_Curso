"""
Cálculo da meta nutricional diária do usuário.

Baseado em:
- TMB (Taxa Metabólica Basal): equação de Mifflin-St Jeor (1990), considerada
  pela Academy of Nutrition and Dietetics a equação preditiva mais precisa
  para estimar o gasto energético em repouso.
- GET (Gasto Energético Total): TMB x fator de atividade física (PAL).
- Ajuste calórico por objetivo: déficit de ~20% para emagrecimento e
  superávit de ~350 kcal para hipertrofia (dentro da faixa de 250-500 kcal
  recomendada para ganho de massa muscular controlado).
- Proteína por objetivo: valores dentro das faixas normalmente indicadas em
  nutrição esportiva (emagrecimento: 2,0-2,4 g/kg para preservar massa
  magra em déficit; hipertrofia: 1,6-2,2 g/kg).
- Gordura: 25% do total calórico (dentro da faixa geral de 20-35%).
- Carboidrato: preenche o restante das calorias.
"""

FATOR_ATIVIDADE = {
    'sedentario': 1.2,
    'leve': 1.375,
    'moderado': 1.55,
    'intenso': 1.725,
    'muito_intenso': 1.9,
}

PROTEINA_POR_KG = {
    'emagrecimento': 2.2,
    'hipertrofia': 2.0,
    'manutencao': 1.6,
}

SUPERAVIT_HIPERTROFIA = 350   # kcal
DEFICIT_EMAGRECIMENTO = 0.80  # mantém 80% do GET (déficit de 20%)
PERCENTUAL_GORDURA = 0.25     # 25% das calorias totais


class DadosIncompletos(Exception):
    """Levantada quando faltam dados no perfil do usuário para calcular a dieta."""
    pass


def calcular_tmb(peso_kg, altura_cm, idade, sexo):
    """Taxa Metabólica Basal pela equação de Mifflin-St Jeor."""
    base = (10 * float(peso_kg)) + (6.25 * float(altura_cm)) - (5 * idade)
    return base + 5 if sexo == 'M' else base - 161


def calcular_meta_nutricional(usuario, peso_atual):
    """
    Retorna um dicionário com a meta diária de calorias e macronutrientes
    calculada para o usuário, a partir do peso mais recente registrado.
    """
    faltando = []

    if not usuario.altura:
        faltando.append('altura')
    if not usuario.data_nascimento:
        faltando.append('data de nascimento')
    if not usuario.sexo:
        faltando.append('sexo')
    if not usuario.nivel_atividade:
        faltando.append('nível de atividade')
    if not usuario.objetivo:
        faltando.append('objetivo')

    if faltando:
        raise DadosIncompletos(
            'Complete no seu perfil: ' + ', '.join(faltando) + '.'
        )

    if not peso_atual:
        raise DadosIncompletos(
            'Registre seu peso em "Registrar dados de hoje" antes de gerar a dieta.'
        )

    idade = usuario.idade
    altura_cm = float(usuario.altura) * 100

    tmb = calcular_tmb(peso_atual, altura_cm, idade, usuario.sexo)
    get = tmb * FATOR_ATIVIDADE[usuario.nivel_atividade]

    if usuario.objetivo == 'hipertrofia':
        calorias = get + SUPERAVIT_HIPERTROFIA
    elif usuario.objetivo == 'emagrecimento':
        calorias = get * DEFICIT_EMAGRECIMENTO
    else:
        calorias = get

    proteina_g = PROTEINA_POR_KG[usuario.objetivo] * float(peso_atual)
    gordura_g = (calorias * PERCENTUAL_GORDURA) / 9
    carboidrato_g = (calorias - (proteina_g * 4) - (gordura_g * 9)) / 4

    return {
        'tmb': round(tmb),
        'get': round(get),
        'calorias': round(calorias),
        'proteina': round(proteina_g),
        'carboidrato': round(max(carboidrato_g, 0)),
        'gordura': round(gordura_g),
    }