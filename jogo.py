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

pygame.init()       # Inicializa módulos do pygame (tela, fontes, eventos, áudio, etc.)
try:        # Inicia um código que pode dar erro. Se der erro, pula para o except
    pygame.mixer.init()     # Inicializa o módulo de som
except pygame.error:        # Captura apenas erros do pygame. Se for outro erro, aparece normalmente
    # Sem dispositivo de áudio (ex.: WSL): usa driver "dummy" e o jogo roda sem som
    import os       # Biblioteca que dá acesso a recursos do sistema operacional
    os.environ['SDL_AUDIODRIVER'] = 'dummy'     # Define o driver de áudio (SDL é uma biblioteca) como "dummy" (driver "falso")
    pygame.mixer.quit()     # Encerra o módulo de som para evitar problemas anteriores
    pygame.mixer.init()     # Reinicia o módulo de som

# ----- Gera tela principal     display.set define 
window = pygame.display.set_mode((WIDTH, HEIGHT))       # Define o tamanho (modo) da janela (1280 x 720 px)
            # A função retornou uma variável do tipo Surface, armazenada na variável window. window é uma tela, onde é desenhado o jogo
pygame.display.set_caption(TITULO)      # Define o título da janela (Coletando - Central de Triagem)

# ----- Inicia assets
assets = load_assets()      # load_assets carrega imagens, cenários e sons em um dicionário e aí é armazenado em assets

# ----- Inicia estruturas de dados
# Dicionário com as informações que passam de uma tela para outra
dados = {
    'progresso': carrega_progresso(),  # fases desbloqueadas, estrelas e recordes
                # Retorna um dicionário semelhante ao do progresso.json, mas atualizado de acordo com o momento do jogo
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
