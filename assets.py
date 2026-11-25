import pygame
import os
from config import SND_DIR, TAMANHO_ITEM
from desenho_itens import DESENHOS
from cenarios import FundoExterno, FundoInterno

# Nomes dos efeitos sonoros (cada um é um arquivo .wav em assets/sons)
EFEITOS = ['acerto', 'erro', 'pegar', 'clique', 'dica', 'estrela', 'contagem', 'vai',
           'pausa', 'caiu', 'vitoria', 'derrota']       # Mesmos nomes dos arquivos .wav
VOLUME_MUSICA = 0.45


def load_assets():      # Carrega imagens, cenários e sons em um dicionário
    assets = {}

    # ----- Imagens dos lixos
    # Os lixos são desenhados pelo próprio código (desenho_itens.py).
    # Desenhamos cada um uma vez só, aqui, e guardamos a imagem no dicionário.
    assets['itens'] = {}  # tamanho normal (quando o item tá na esteira)
    assets['itens_grandes'] = {}  # tamanho grande (quando o item aparece na janela de ajuda)
    for nome in DESENHOS:
        base = pygame.Surface((100, 100), pygame.SRCALPHA)      # Cria uma Surface 100x100 px com fundo transparente
                    # SRCALPHA define ser transparente
        funcao_desenho = DESENHOS[nome]     # DESENHOS tem string como chave e função como valor
        funcao_desenho(base)        # Printa o desenho desejado na base (na surface)
        assets['itens'][nome] = pygame.transform.smoothscale(base, (TAMANHO_ITEM, TAMANHO_ITEM))        # cria uma versão redimensionada do item, mas com bordas suavizadas
        assets['itens_grandes'][nome] = pygame.transform.smoothscale(base, (200, 200))

    # ----- Cenários animados
    assets['fundo_externo'] = FundoExterno()  # Classe da central vista de fora (menus)
    assets['fundo_interno'] = FundoInterno()  # Classe do galpão por dentro (partida)

    # ----- Sons
    assets['sons'] = {}
    for nome in EFEITOS:
        som = pygame.mixer.Sound(os.path.join(SND_DIR, nome + '.wav'))
        som.set_volume(0.6)
        assets['sons'][nome] = som
    assets['som_ligado'] = True
    assets['musica_atual'] = ''

    """
    --- RESULTADO ---
    assets = {
        "itens" : {
            desenho1 : surface1 ;
            ...
        };
        "itens_grandes" = {
            desenho2 : surface2 ;
            ...
        };
        "fundo_externo" : FundoExterno() ;
        "fundo_interno" : FundoInterno() ;
        "sons" : {
            "som1" : som1.wav ;
            ...
        } ;
        "som_ligado" : True ;
        "musica_atual" : ""
    }
    """

    return assets


def tocar_som(assets, nome):
    # Toca um efeito sonoro curto
    if assets['som_ligado']:
        assets['sons'][nome].play()


def tocar_musica(assets, nome):
    # Troca a música de fundo (fica tocando em loop). Se já estiver tocando, não reinicia.
    if nome != assets['musica_atual']:
        assets['musica_atual'] = nome
        pygame.mixer.music.load(os.path.join(SND_DIR, nome + '.wav'))
        if assets['som_ligado']:
            pygame.mixer.music.set_volume(VOLUME_MUSICA)
        else:
            pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1, fade_ms=600)
                    # Argumento -1 --> Quantidade de vezes que a música toca. -1 implica em loop infinito
                    # Argumento fade_ms --> Ao invés da música começar em 600 ms, ela começa no 0 no mudo e vai aumentando o volume até 600 ms


def pausar_musica():
    pygame.mixer.music.pause()


def continuar_musica():
    pygame.mixer.music.unpause()


def liga_desliga_som(assets):
    # Chamado quando o jogador aperta a tecla M
    assets['som_ligado'] = not assets['som_ligado']
    if assets['som_ligado']:
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
    else:
        pygame.mixer.music.set_volume(0)
