"""
Gerador das músicas e efeitos sonoros do jogo "Coletando".

Todos os sons do jogo são sintetizados aqui, nota por nota, usando apenas a
biblioteca padrão do Python (módulos ``math``, ``random``, ``array`` e ``wave``).
Assim não dependemos de arquivos de áudio de terceiros (sem problemas de
direitos autorais) e qualquer pessoa do grupo pode alterar as músicas.

Uso (a partir da pasta raiz do projeto):

    python ferramentas/gerar_sons.py

Os arquivos ``.wav`` são gravados em ``assets/sons``.
"""

import array
import math
import os
import random
import wave

TAXA = 22050  # amostras por segundo
PASTA_SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sons")


# ---------------------------------------------------------------------------
# Funções básicas de síntese
# ---------------------------------------------------------------------------

def freq_midi(nota):
    """Converte um número de nota MIDI (60 = Dó central) em frequência (Hz)."""
    return 440.0 * 2 ** ((nota - 69) / 12)


def onda(tipo, fase):
    """Retorna o valor (-1 a 1) de uma forma de onda para uma fase entre 0 e 1."""
    fase -= math.floor(fase)
    if tipo == "seno":
        return math.sin(2 * math.pi * fase)
    if tipo == "quadrada":
        return 1.0 if fase < 0.5 else -1.0
    if tipo == "pulso":  # quadrada "fina", som típico de videogame antigo
        return 1.0 if fase < 0.25 else -1.0
    if tipo == "triangulo":
        return 4 * fase - 1 if fase < 0.5 else 3 - 4 * fase
    if tipo == "serra":
        return 2 * fase - 1
    raise ValueError(tipo)


def envelope(i, total, ataque=0.01, soltura=0.08):
    """Envelope simples de volume (sobe no início e desce no fim da nota)."""
    t = i / TAXA
    dur = total / TAXA
    if t < ataque:
        return t / ataque
    if t > dur - soltura:
        return max(0.0, (dur - t) / soltura)
    return 1.0


def adicionar_nota(buffer, inicio, duracao, freq, tipo, volume, ataque=0.01, soltura=0.08, vibrato=0.0, deslize=0.0):
    """Soma uma nota ao buffer (lista de floats) a partir do segundo ``inicio``."""
    ini = int(inicio * TAXA)
    total = int(duracao * TAXA)
    fase = 0.0
    for i in range(total):
        if ini + i >= len(buffer):
            break
        t = i / TAXA
        f = freq * (1 + deslize * t / max(duracao, 1e-6))
        if vibrato:
            f *= 1 + vibrato * math.sin(2 * math.pi * 5.5 * t)
        fase += f / TAXA
        buffer[ini + i] += onda(tipo, fase) * volume * envelope(i, total, ataque, soltura)


def adicionar_ruido(buffer, inicio, duracao, volume, decaimento=30.0, grave=False):
    """Soma um ruído curto (usado para chimbal, caixa e efeitos)."""
    ini = int(inicio * TAXA)
    total = int(duracao * TAXA)
    anterior = 0.0
    for i in range(total):
        if ini + i >= len(buffer):
            break
        r = random.uniform(-1, 1)
        if grave:  # filtro passa-baixa bem simples
            r = anterior = anterior * 0.85 + r * 0.15
            r *= 3
        buffer[ini + i] += r * volume * math.exp(-decaimento * i / TAXA)


def adicionar_bumbo(buffer, inicio, volume=0.9):
    """Bumbo: seno que cai rapidamente de frequência."""
    ini = int(inicio * TAXA)
    total = int(0.18 * TAXA)
    fase = 0.0
    for i in range(total):
        if ini + i >= len(buffer):
            break
        t = i / TAXA
        f = 130 * math.exp(-t * 18) + 45
        fase += f / TAXA
        buffer[ini + i] += math.sin(2 * math.pi * fase) * volume * math.exp(-t * 14)


def salvar(nome, buffer, volume_final=0.85):
    """Normaliza o buffer e grava como WAV mono de 16 bits."""
    pico = max(1e-6, max(abs(v) for v in buffer))
    escala = volume_final * 32767 / pico
    dados = array.array("h", (int(v * escala) for v in buffer))
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    caminho = os.path.join(PASTA_SAIDA, nome)
    with wave.open(caminho, "wb") as arq:
        arq.setnchannels(1)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        arq.writeframes(dados.tobytes())
    print("gerado:", caminho)


# ---------------------------------------------------------------------------
# Músicas
# ---------------------------------------------------------------------------

# Melodia do jogo: (nota MIDI ou None para pausa, duração em colcheias)
MELODIA_JOGO = [
    (72, 1), (76, 1), (79, 1), (76, 1), (74, 1), (76, 1), (72, 2),
    (77, 1), (76, 1), (74, 1), (72, 1), (69, 1), (72, 1), (74, 2),
    (74, 1), (76, 1), (77, 1), (79, 1), (77, 1), (76, 1), (74, 1), (71, 1),
    (72, 2), (76, 2), (79, 4),
    (69, 1), (72, 1), (76, 1), (72, 1), (69, 1), (72, 1), (76, 1), (79, 1),
    (77, 2), (76, 2), (74, 2), (72, 2),
    (79, 1), (77, 1), (76, 1), (74, 1), (76, 1), (74, 1), (71, 1), (74, 1),
    (72, 4), (67, 2), (72, 2),
]
# Fundamental de cada compasso (Dó, Fá, Sol, Dó, Lá, Fá, Sol, Dó)
BAIXO_JOGO = [48, 41, 43, 48, 45, 41, 43, 48]

MELODIA_MENU = [
    (76, 4), (79, 4),
    (81, 2), (79, 2), (76, 4),
    (77, 4), (74, 2), (72, 2),
    (74, 8),
    (72, 2), (76, 2), (79, 4),
    (81, 4), (84, 4),
    (81, 2), (79, 2), (77, 2), (76, 2),
    (74, 4), (72, 4),
]
# Acordes do menu (tríades, em notas MIDI)
ACORDES_MENU = [
    (60, 64, 67), (57, 60, 64), (53, 57, 60), (55, 59, 62),
    (60, 64, 67), (57, 60, 64), (53, 57, 60), (55, 59, 62),
]


def musica_jogo(bpm, nome, repeticoes=2):
    """Música animada da partida. Quanto maior o ``bpm``, mais rápida."""
    colcheia = 60 / bpm / 2
    compasso = colcheia * 8
    total = compasso * 8 * repeticoes
    buf = [0.0] * int(total * TAXA)
    for r in range(repeticoes):
        base = r * compasso * 8
        # melodia
        t = base
        for nota, dur in MELODIA_JOGO:
            if nota is not None:
                adicionar_nota(buf, t, dur * colcheia * 0.95, freq_midi(nota), "pulso", 0.20, soltura=0.05)
                # eco uma oitava acima, bem baixinho, para dar brilho
                adicionar_nota(buf, t, dur * colcheia * 0.6, freq_midi(nota + 12), "triangulo", 0.06)
            t += dur * colcheia
        # baixo e bateria
        for c, raiz in enumerate(BAIXO_JOGO):
            ini = base + c * compasso
            for k, salto in enumerate((0, 12, 7, 12, 0, 12, 7, 12)):
                adicionar_nota(buf, ini + k * colcheia, colcheia * 0.9, freq_midi(raiz + salto), "triangulo", 0.30, soltura=0.03)
            for k in range(8):
                tk = ini + k * colcheia
                if k in (0, 4):
                    adicionar_bumbo(buf, tk, 0.55)
                if k in (2, 6):
                    adicionar_ruido(buf, tk, 0.12, 0.22, decaimento=25)
                adicionar_ruido(buf, tk, 0.04, 0.07, decaimento=90)
    salvar(nome, buf, 0.75)


def musica_menu(bpm=92, nome="musica_menu.wav", repeticoes=2):
    """Música calma do menu, com arpejos suaves."""
    colcheia = 60 / bpm / 2
    compasso = colcheia * 8
    total = compasso * 8 * repeticoes
    buf = [0.0] * int(total * TAXA)
    for r in range(repeticoes):
        base = r * compasso * 8
        t = base
        for nota, dur in MELODIA_MENU:
            adicionar_nota(buf, t, dur * colcheia, freq_midi(nota), "seno", 0.28, ataque=0.03, soltura=0.2, vibrato=0.004)
            adicionar_nota(buf, t, dur * colcheia, freq_midi(nota), "triangulo", 0.08, ataque=0.03, soltura=0.2)
            t += dur * colcheia
        for c, acorde in enumerate(ACORDES_MENU):
            ini = base + c * compasso
            arpejo = [acorde[0], acorde[1], acorde[2], acorde[1] + 12, acorde[2], acorde[1], acorde[0] + 12, acorde[1]]
            for k, nota in enumerate(arpejo):
                adicionar_nota(buf, ini + k * colcheia, colcheia * 1.6, freq_midi(nota), "triangulo", 0.10, soltura=0.15)
            adicionar_nota(buf, ini, compasso, freq_midi(acorde[0] - 12), "seno", 0.22, ataque=0.05, soltura=0.3)
            adicionar_ruido(buf, ini + colcheia * 2, 0.05, 0.03, decaimento=60)
            adicionar_ruido(buf, ini + colcheia * 6, 0.05, 0.03, decaimento=60)
    salvar(nome, buf, 0.6)


# ---------------------------------------------------------------------------
# Efeitos sonoros
# ---------------------------------------------------------------------------

def efeito_arpejo(nome, notas, passo, tipo="quadrada", volume=0.3, dur_nota=None):
    """Toca uma sequência rápida de notas (usado em vários efeitos)."""
    dur_nota = dur_nota or passo * 1.5
    total = passo * len(notas) + dur_nota + 0.05
    buf = [0.0] * int(total * TAXA)
    for i, n in enumerate(notas):
        adicionar_nota(buf, i * passo, dur_nota, freq_midi(n), tipo, volume, soltura=dur_nota * 0.6)
    salvar(nome, buf)


def gerar_efeitos():
    """Gera todos os efeitos sonoros curtos do jogo."""
    efeito_arpejo("acerto.wav", [72, 76, 79, 84], 0.06, "pulso")
    # erro: duas notas graves e "desafinadas"
    buf = [0.0] * int(0.5 * TAXA)
    adicionar_nota(buf, 0.0, 0.18, freq_midi(52), "serra", 0.3)
    adicionar_nota(buf, 0.2, 0.28, freq_midi(47), "serra", 0.3, deslize=-0.2)
    salvar("erro.wav", buf)
    efeito_arpejo("pegar.wav", [79, 86], 0.035, "triangulo", 0.4)
    efeito_arpejo("clique.wav", [84], 0.04, "pulso", 0.25, dur_nota=0.05)
    efeito_arpejo("dica.wav", [84, 88, 91, 96, 91, 96], 0.07, "seno", 0.35, dur_nota=0.25)
    efeito_arpejo("estrela.wav", [88, 93, 100], 0.05, "triangulo", 0.4, dur_nota=0.3)
    efeito_arpejo("contagem.wav", [72], 0.1, "pulso", 0.3, dur_nota=0.15)
    efeito_arpejo("vai.wav", [84], 0.1, "pulso", 0.3, dur_nota=0.35)
    efeito_arpejo("pausa.wav", [76, 72], 0.07, "triangulo", 0.4)
    # caiu da esteira: apito descendo
    buf = [0.0] * int(0.6 * TAXA)
    adicionar_nota(buf, 0, 0.55, freq_midi(84), "seno", 0.4, deslize=-0.6)
    adicionar_ruido(buf, 0.45, 0.15, 0.3, decaimento=20, grave=True)
    salvar("caiu.wav", buf)
    # fanfarra de vitória
    buf = [0.0] * int(2.2 * TAXA)
    seq = [(72, 0.0, 0.15), (72, 0.15, 0.15), (72, 0.3, 0.15), (76, 0.45, 0.45), (74, 0.9, 0.15),
           (76, 1.05, 0.15), (79, 1.2, 0.9)]
    for nota, ini, dur in seq:
        adicionar_nota(buf, ini, dur, freq_midi(nota), "pulso", 0.25)
        adicionar_nota(buf, ini, dur, freq_midi(nota - 12), "triangulo", 0.25)
    for n in (60, 64, 67, 72):
        adicionar_nota(buf, 1.2, 0.9, freq_midi(n), "triangulo", 0.12)
    salvar("vitoria.wav", buf)
    # derrota: frase descendente triste
    efeito_arpejo("derrota.wav", [67, 66, 65, 64], 0.22, "triangulo", 0.35, dur_nota=0.3)


if __name__ == "__main__":
    random.seed(7)
    gerar_efeitos()
    musica_menu()
    # A música da partida fica mais rápida a cada fase
    musica_jogo(118, "musica_fase1.wav")
    musica_jogo(140, "musica_fase2.wav")
    musica_jogo(166, "musica_fase3.wav")
