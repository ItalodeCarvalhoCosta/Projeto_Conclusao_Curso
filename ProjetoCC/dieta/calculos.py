from decimal import Decimal


FATOR_ATIVIDADE = {
    'sedentario': Decimal('1.2'),
    'leve': Decimal('1.375'),
    'moderado': Decimal('1.55'),
    'intenso': Decimal('1.725'),
    'muito_intenso': Decimal('1.9'),
}

# Ajuste calórico sobre o TDEE conforme o objetivo (em kcal/dia).
# Déficit/superávit moderados, dentro do que é considerado seguro
# para a maioria dos adultos saudáveis.
AJUSTE_OBJETIVO = {
    'emagrecer': Decimal('-500'),
    'manter': Decimal('0'),
    'ganhar_massa': Decimal('400'),
}

# % de calorias por macro, conforme objetivo (dentro da faixa AMDR).
# Emagrecer: mais proteína pra preservar massa magra durante o déficit.
# Ganhar massa: mais carboidrato pra sustentar o volume de treino.
DISTRIBUICAO_MACROS = {
    'emagrecer':     {'proteina': Decimal('0.30'), 'carboidrato': Decimal('0.40'), 'gordura': Decimal('0.30')},
    'manter':        {'proteina': Decimal('0.20'), 'carboidrato': Decimal('0.50'), 'gordura': Decimal('0.30')},
    'ganhar_massa':  {'proteina': Decimal('0.25'), 'carboidrato': Decimal('0.50'), 'gordura': Decimal('0.25')},
}

# Piso de segurança: nunca sugerir menos que isso, mesmo em déficit
# agressivo, para não cair em uma dieta perigosamente hipocalórica.
CALORIAS_MINIMAS = {
    'M': 1500,
    'F': 1200,
    'O': 1350,
}


def calcular_imc(peso_kg, altura_m):
    """IMC = peso (kg) / altura (m) ao quadrado."""
    peso_kg = Decimal(str(peso_kg))
    altura_m = Decimal(str(altura_m))
    return round(peso_kg / (altura_m ** 2), 1)


def calcular_bmr(peso_kg, altura_m, idade, genero):
    """
    Taxa metabólica basal pela equação de Mifflin-St Jeor.
    Homem:  BMR = 10*peso + 6.25*altura_cm - 5*idade + 5
    Mulher: BMR = 10*peso + 6.25*altura_cm - 5*idade - 161
    """
    peso_kg = Decimal(str(peso_kg))
    altura_cm = Decimal(str(altura_m)) * 100
    idade = Decimal(str(idade))

    base = (Decimal('10') * peso_kg) + (Decimal('6.25') * altura_cm) - (Decimal('5') * idade)

    if genero == 'M':
        bmr = base + 5
    elif genero == 'F':
        bmr = base - 161
    else:
        # Para "Outro", usamos a média dos dois ajustes (-78) como estimativa neutra.
        bmr = base - Decimal('78')

    return round(bmr)


def calcular_tdee(bmr, nivel_atividade):
    """Gasto calórico total diário = BMR x fator de atividade."""
    fator = FATOR_ATIVIDADE.get(nivel_atividade, Decimal('1.2'))
    return round(Decimal(bmr) * fator)


def calcular_calorias_alvo(tdee, objetivo, genero):
    """Aplica o ajuste do objetivo sobre o TDEE, respeitando um piso mínimo seguro."""
    ajuste = AJUSTE_OBJETIVO.get(objetivo, Decimal('0'))
    calorias = Decimal(tdee) + ajuste
    piso = CALORIAS_MINIMAS.get(genero, 1350)
    return int(max(calorias, piso))


def calcular_macros(calorias_alvo, objetivo):
    """
    Converte a meta de calorias em gramas de proteína, carboidrato e
    gordura, usando a distribuição percentual definida para o objetivo.
    Proteína e carboidrato: 4 kcal/g. Gordura: 9 kcal/g.
    """
    percentuais = DISTRIBUICAO_MACROS.get(objetivo, DISTRIBUICAO_MACROS['manter'])
    calorias_alvo = Decimal(calorias_alvo)

    proteina_g = round((calorias_alvo * percentuais['proteina']) / Decimal('4'))
    carboidrato_g = round((calorias_alvo * percentuais['carboidrato']) / Decimal('4'))
    gordura_g = round((calorias_alvo * percentuais['gordura']) / Decimal('9'))

    return {
        'proteina_g': int(proteina_g),
        'carboidrato_g': int(carboidrato_g),
        'gordura_g': int(gordura_g),
    }


def calcular_metas_completas(perfil):
    """
    Função de conveniência: recebe um PerfilDieta e devolve um dict
    pronto com bmr, tdee, calorias_alvo e macros — é isso que a view
    chama antes de mandar os dados pra IA.
    """
    bmr = calcular_bmr(perfil.peso, perfil.altura, perfil.idade, perfil.genero)
    tdee = calcular_tdee(bmr, perfil.nivel_atividade)
    calorias_alvo = calcular_calorias_alvo(tdee, perfil.objetivo, perfil.genero)
    macros = calcular_macros(calorias_alvo, perfil.objetivo)

    return {
        'imc': calcular_imc(perfil.peso, perfil.altura),
        'bmr': bmr,
        'tdee': tdee,
        'calorias_alvo': calorias_alvo,
        **macros,
    }