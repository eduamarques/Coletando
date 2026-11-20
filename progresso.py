import json
from os import path
from config import ARQUIVO_PROGRESSO, FASES, TOTAL_FASES, ESTRELAS_PARA_PASSAR

# O progresso é um dicionário:
#   {'desbloqueada': 2, 'estrelas': {1: 3, 2: 0, 3: 0}}
# desbloqueada = maior fase que o jogador já pode jogar
# estrelas = melhor número de estrelas conquistado em cada fase


def calcula_estrelas(acertos, total):
    # Para 10 lixos: 10 = 3 estrelas, 8 ou 9 = 2, de 4 a 7 = 1, menos de 4 = 0.
    # Para 15 lixos (fase 3) usamos a mesma proporção: 100% = 3, 80% = 2, 40% = 1.
    if total <= 0:
        return 0
    if acertos >= total:
        return 3
    proporcao = acertos / total
    if proporcao >= 0.8:
        return 2
    if proporcao >= 0.4:
        return 1
    return 0


def carrega_progresso():
    # Começa do zero
    progresso = {'desbloqueada': 1, 'estrelas': {}}
    for fase in FASES:
        progresso['estrelas'][fase] = 0

    # Se já existir um arquivo salvo, lê o que está nele
    if path.exists(ARQUIVO_PROGRESSO):
        with open(ARQUIVO_PROGRESSO, 'r', encoding='utf-8') as arquivo:
            salvo = json.load(arquivo)
        progresso['desbloqueada'] = salvo['desbloqueada']
        for fase in FASES:
            # no arquivo JSON as chaves do dicionário viram texto ('1', '2', '3')
            if str(fase) in salvo['estrelas']:
                progresso['estrelas'][fase] = salvo['estrelas'][str(fase)]
    return progresso


def salva_progresso(progresso):
    with open(ARQUIVO_PROGRESSO, 'w', encoding='utf-8') as arquivo:
        json.dump(progresso, arquivo, indent=2)


def registra_resultado(progresso, fase, estrelas):
    # Guarda o recorde de estrelas e desbloqueia a próxima fase se passou
    if estrelas > progresso['estrelas'][fase]:
        progresso['estrelas'][fase] = estrelas
    if estrelas >= ESTRELAS_PARA_PASSAR and fase < TOTAL_FASES:
        if fase + 1 > progresso['desbloqueada']:
            progresso['desbloqueada'] = fase + 1
    salva_progresso(progresso)
