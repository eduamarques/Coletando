import json
from os import path
from config import ARQUIVO_PROGRESSO, FASES, TOTAL_FASES, ESTRELAS_PARA_PASSAR

# O progresso é um dicionário:
#   {'desbloqueada': 2, 'estrelas': {1: 3, 2: 0, 3: 0}, 'recordes': {1: 1200, 2: 0, 3: 0}}
# recordes = maior pontuação feita em cada fase (Eduardo)
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
    # Eduardo
    # 'recordes' guarda a maior pontuação já feita em cada fase
    progresso = {'desbloqueada': 1, 'estrelas': {}, 'recordes': {}}
    for fase in FASES:
        progresso['estrelas'][fase] = 0     # Acrescenta ou altera a chave fase pelo valor 0
        # Eduardo
        progresso['recordes'][fase] = 0     # Acrescenta ou altera a chave progresso pelo valor 0

    # Se já existir um arquivo salvo, lê o que está nele
    if path.exists(ARQUIVO_PROGRESSO):      # path.exists retorna True se o arquivo existir
                    # ARQUIVO_PROGRESSO já foi definido como um endereço até o progresso.json
        with open(ARQUIVO_PROGRESSO, 'r', encoding='utf-8') as arquivo:
                        # with fecha o arquivo após a execução do bloco
                        # open() abre o arquivo
                        # "r" significa modo leitura
                        # utf-8 define interpretar caracteres com acentos
                        # define o nome do arquivo acessado como "arquivo"
            salvo = json.load(arquivo)      # Lê o arquivo json e carrega o texto na variável "salvo". Logo, "salvo" possui um dicionário
        progresso['desbloqueada'] = salvo['desbloqueada']
        for fase in FASES:
            # no arquivo JSON as chaves do dicionário viram texto ('1', '2', '3')
            if str(fase) in salvo['estrelas']:
                progresso['estrelas'][fase] = salvo['estrelas'][str(fase)]
            # Eduardo
            # arquivos salvos antes do recorde existir não têm a chave 'recordes'
            if 'recordes' in salvo and str(fase) in salvo['recordes']:
                progresso['recordes'][fase] = salvo['recordes'][str(fase)]
    return progresso


def salva_progresso(progresso):
    with open(ARQUIVO_PROGRESSO, 'w', encoding='utf-8') as arquivo:
        json.dump(progresso, arquivo, indent=2)


# Eduardo
# agora também recebe os pontos da partida para atualizar o recorde
def registra_resultado(progresso, fase, estrelas, pontos):
    # Guarda o recorde de estrelas e desbloqueia a próxima fase se passou
    if estrelas > progresso['estrelas'][fase]:
        progresso['estrelas'][fase] = estrelas
    # Eduardo
    # só troca o recorde se a pontuação nova for maior
    if pontos > progresso['recordes'][fase]:
        progresso['recordes'][fase] = pontos
    if estrelas >= ESTRELAS_PARA_PASSAR and fase < TOTAL_FASES:
        if fase + 1 > progresso['desbloqueada']:
            progresso['desbloqueada'] = fase + 1
    salva_progresso(progresso)
