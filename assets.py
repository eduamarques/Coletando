import pygame
import os
from config import SND_DIR, TAMANHO_ITEM
from desenho_itens import DESENHOS
from cenarios import FundoExterno, FundoInterno

# Nomes dos efeitos sonoros (cada um é um arquivo .wav em assets/sons)
EFEITOS = ['acerto', 'erro', 'pegar', 'clique', 'dica', 'estrela', 'contagem', 'vai',
           'pausa', 'caiu', 'vitoria', 'derrota']
VOLUME_MUSICA = 0.45


def load_assets():
    assets = {}

    # ----- Imagens dos lixos
    # Os lixos são desenhados pelo próprio código (desenho_itens.py).
    # Desenhamos cada um uma vez só, aqui, e guardamos a imagem no dicionário.
    assets['itens'] = {}  # tamanho normal (na esteira)
    assets['itens_grandes'] = {}  # tamanho grande (janela de ajuda)
    for nome in DESENHOS:
        base = pygame.Surface((100, 100), pygame.SRCALPHA)
        funcao_desenho = DESENHOS[nome]
        funcao_desenho(base)
        assets['itens'][nome] = pygame.transform.smoothscale(base, (TAMANHO_ITEM, TAMANHO_ITEM))
        assets['itens_grandes'][nome] = pygame.transform.smoothscale(base, (200, 200))

    # ----- Cenários animados
    assets['fundo_externo'] = FundoExterno()  # central vista de fora (menus)
    assets['fundo_interno'] = FundoInterno()  # galpão por dentro (partida)

    # ----- Sons
    assets['sons'] = {}
    for nome in EFEITOS:
        som = pygame.mixer.Sound(os.path.join(SND_DIR, nome + '.wav'))
        som.set_volume(0.6)
        assets['sons'][nome] = som
    assets['som_ligado'] = True
    assets['musica_atual'] = ''
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
