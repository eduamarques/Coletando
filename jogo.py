# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
# Mateus
from config import WIDTH, HEIGHT, TITULO, INIT, ESCOLHA, GAME, RESULTADO, PARABENS, QUIT, DIFICULDADE
# Fim Mateus
from assets import load_assets
from progresso import carrega_progresso
from init_screen import init_screen
from fases_screen import fases_screen
# Mateus
from dificuldade_screen import dificuldade_screen
# Fim Mateus
from game_screen import game_screen
from resultado_screen import resultado_screen
from parabens_screen import parabens_screen

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    # Sem dispositivo de áudio (ex.: WSL): usa driver "dummy" e o jogo roda sem som
    import os
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.mixer.quit()
    pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)

# ----- Inicia assets
assets = load_assets()

# ----- Inicia estruturas de dados
# Dicionário com as informações que passam de uma tela para outra
dados = {
    'progresso': carrega_progresso(),  # fases desbloqueadas e estrelas
    'fase': 1,  # fase que vai ser jogada
    # Mateus
    'dificuldade': 'facil',  # 'facil', 'medio' ou 'dificil'
    # Fim Mateus
    'acertos': 0,  # resultado da última partida
    'total': 0,
    'pontos': 0,
}

# ===== Loop principal =====
# Cada tela é uma função que tem o seu próprio loop e devolve qual é a próxima tela
state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window, assets, dados)
    elif state == ESCOLHA:
        state = fases_screen(window, assets, dados)
    # Mateus
    elif state == DIFICULDADE:
        state = dificuldade_screen(window, assets, dados)
    # Fim Mateus
    elif state == GAME:
        state = game_screen(window, assets, dados)
    elif state == RESULTADO:
        state = resultado_screen(window, assets, dados)
    elif state == PARABENS:
        state = parabens_screen(window, assets, dados)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
