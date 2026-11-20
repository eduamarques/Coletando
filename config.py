from os import path

# Estabelece a pasta que contem os sons e o arquivo de progresso.
SND_DIR = path.join(path.dirname(__file__), 'assets', 'sons')
ARQUIVO_PROGRESSO = path.join(path.dirname(__file__), 'progresso.json')

# Dados gerais do jogo.
TITULO = 'Coletando - Central de Triagem'
WIDTH = 1280  # Largura da tela
HEIGHT = 720  # Altura da tela
FPS = 60  # Frames por segundo

# Define algumas variáveis com as cores usadas no jogo (R, G, B)
BRANCO = (255, 255, 255)
PRETO = (20, 20, 30)
CINZA = (120, 125, 135)
CINZA_ESCURO = (60, 64, 72)
AMARELO_OURO = (255, 205, 40)
VERDE_OK = (60, 190, 90)
VERMELHO_ERRO = (230, 70, 70)
AZUL_UI = (40, 120, 220)
LARANJA_UI = (250, 150, 40)
CREME = (255, 250, 235)

# Cores das letras do título "COLETANDO" (as mesmas das lixeiras)
CORES_TITULO = [(225, 50, 50), (40, 110, 220), (40, 170, 70), (245, 195, 30), (135, 85, 45)]

# Lixeiras: as cores seguem o padrão brasileiro da coleta seletiva (Resolução CONAMA 275).
LIXEIRAS = {
    'plastico': {'nome': 'PLÁSTICO', 'cor': (225, 50, 50)},
    'papel': {'nome': 'PAPEL', 'cor': (40, 110, 220)},
    'vidro': {'nome': 'VIDRO', 'cor': (40, 170, 70)},
    'metal': {'nome': 'METAL', 'cor': (245, 195, 30)},
    'organico': {'nome': 'ORGÂNICO', 'cor': (135, 85, 45)},
}
ORDEM_LIXEIRAS = ['plastico', 'papel', 'vidro', 'metal', 'organico']
LIXEIRA_LARGURA = 170
LIXEIRA_ALTURA = 200

# Fases: velocidade da esteira em pixels por segundo; espacamento = distância entre os lixos
FASES = {
    1: {'itens': 10, 'velocidade': 75, 'espacamento': 260, 'ajudas': 2, 'conjunto': 'facil',
        'subtitulo': 'Vamos aprender a separar o lixo!'},
    2: {'itens': 10, 'velocidade': 110, 'espacamento': 250, 'ajudas': 2, 'conjunto': 'facil',
        'subtitulo': 'A esteira ficou mais rápida!'},
    3: {'itens': 15, 'velocidade': 140, 'espacamento': 240, 'ajudas': 2, 'conjunto': 'dificil',
        'subtitulo': 'Desafio final: objetos difíceis!'},
}
TOTAL_FASES = 3
ESTRELAS_PARA_PASSAR = 2
PONTOS_ACERTO = 100

# Dificuldades: muda quantas ajudas a criança tem em cada fase
#   facil   = todas as ajudas da fase
#   medio   = metade das ajudas da fase
#   dificil = nenhuma ajuda
DIFICULDADES = {
    'facil': {'nome': 'FÁCIL', 'cor': (60, 190, 90), 'descricao': 'Todas as ajudas'},
    'medio': {'nome': 'MÉDIO', 'cor': (250, 150, 40), 'descricao': 'Metade das ajudas'},
    'dificil': {'nome': 'DIFÍCIL', 'cor': (230, 70, 70), 'descricao': 'Nenhuma ajuda'},
}
ORDEM_DIFICULDADES = ['facil', 'medio', 'dificil']

# Esteira
ESTEIRA_Y = 300  # topo da esteira
ESTEIRA_ALTURA = 110
ESTEIRA_X_INICIO = 0
ESTEIRA_X_FIM = WIDTH - 60  # o lixo cai quando passa daqui

# Tamanho (em pixels) da imagem de cada lixo
TAMANHO_ITEM = 84

# Estados para controle do fluxo da aplicação (qual tela está aberta)
INIT = 0  # menu principal
ESCOLHA = 1  # escolha de fases
GAME = 2  # partida
RESULTADO = 3  # estrelas no fim da fase
PARABENS = 4  # animação final
QUIT = 5
DIFICULDADE = 6  # escolha da dificuldade (antes da fase 1)
