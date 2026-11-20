import math
import random
import pygame
from config import (HEIGHT, PRETO, BRANCO, TAMANHO_ITEM, ESTEIRA_Y, ESTEIRA_ALTURA,
                    LIXEIRA_LARGURA, LIXEIRA_ALTURA, WIDTH)
from desenho import imagem_texto, texto, ajusta_cor, lixeira

CORES_CONFETE = [(255, 90, 90), (90, 160, 255), (90, 210, 110), (255, 210, 60), (220, 120, 255)]


class Botao(pygame.sprite.Sprite):
    # Botão clicável que cresce um pouco quando o mouse passa por cima
    def __init__(self, centro, largura, altura, rotulo, cor, tamanho_fonte=34):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.centro = centro
        self.rotulo = rotulo
        self.cor = cor
        self.tamanho_fonte = tamanho_fonte
        self.escala = 1.0
        # área onde o clique vale (não muda quando o botão cresce)
        self.area = pygame.Rect(0, 0, largura, altura)
        self.area.center = centro
        self.desenha_imagem()

    def clicado(self, event):
        # Devolve True se este evento foi um clique esquerdo em cima do botão
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.area.collidepoint(event.pos)
        return False

    def update(self, dt):
        if self.area.collidepoint(pygame.mouse.get_pos()):
            alvo = 1.08
        else:
            alvo = 1.0
        # só redesenha se o tamanho mudou
        if abs(alvo - self.escala) > 0.002:
            self.escala += (alvo - self.escala) * min(1, dt * 12)
            self.desenha_imagem()

    def desenha_imagem(self):
        largura = int(self.area.width * self.escala)
        altura = int(self.area.height * self.escala)
        # +6 de altura para caber a "sombra" embaixo do botão
        self.image = pygame.Surface((largura, altura + 6), pygame.SRCALPHA)
        r = pygame.Rect(0, 0, largura, altura)
        pygame.draw.rect(self.image, ajusta_cor(self.cor, -60), r.move(0, 6), border_radius=20)
        pygame.draw.rect(self.image, self.cor, r, border_radius=20)
        brilho = r.inflate(-14, -altura * 0.55).move(0, -altura * 0.18)
        pygame.draw.rect(self.image, ajusta_cor(self.cor, 45), brilho, border_radius=12)
        pygame.draw.rect(self.image, PRETO, r, 4, border_radius=20)
        texto(self.image, self.rotulo, int(self.tamanho_fonte * self.escala), BRANCO, r.center, contorno=2)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.centro[0]
        self.rect.top = self.centro[1] - altura / 2


class Lixo(pygame.sprite.Sprite):
    # Um lixo que anda na esteira e pode ser arrastado com o mouse.
    # Valores possíveis de self.estado:
    #   'esteira'    - andando sobre a esteira
    #   'arrastando' - preso no cursor do mouse
    #   'indo'       - voando até uma lixeira (depois de solto)
    #   'caindo'     - caiu no fim da esteira
    def __init__(self, assets, dados_lixo, x):
        pygame.sprite.Sprite.__init__(self)

        self.dados = dados_lixo  # dicionário do lixo (ver dados.py)
        self.lixeira_certa = dados_lixo['lixeira']
        self.imagem_original = assets['itens'][dados_lixo['desenho']]
        self.x = x
        self.y_base = ESTEIRA_Y + ESTEIRA_ALTURA / 2 - 18
        self.y = self.y_base
        self.estado = 'esteira'
        self.angulo = 0
        self.escala = 1.0
        self.tempo = random.uniform(0, 6)
        self.ajuda_vista = False  # já pediu ajuda sobre este lixo?
        self.destino = (0, 0)  # ponto da lixeira para onde está voando
        self.velocidade_y = 0
        self.atualiza_imagem()

    def area_clique(self):
        # Retângulo usado para clicar/arrastar (não gira junto com a imagem)
        area = pygame.Rect(0, 0, TAMANHO_ITEM - 10, TAMANHO_ITEM - 10)
        area.center = (self.x, self.y)
        return area

    def voar_para(self, destino):
        # Começa a animação de entrar numa lixeira
        self.estado = 'indo'
        self.destino = destino

    def cair(self):
        # Começa a animação de cair da ponta da esteira
        self.estado = 'caindo'
        self.velocidade_y = -160

    def update(self, dt, velocidade_esteira):
        # Toda a lógica de movimentação é feita aqui, de acordo com o estado
        self.tempo += dt
        if self.estado == 'esteira':
            self.x += velocidade_esteira * dt
            # balança um pouquinho, como se a esteira tremesse
            self.y = self.y_base + math.sin(self.tempo * 9) * 1.5
            self.angulo = math.sin(self.tempo * 4) * 4
        elif self.estado == 'arrastando':
            self.angulo = math.sin(self.tempo * 12) * 8
        elif self.estado == 'indo':
            passo = min(1, dt * 9)
            self.x += (self.destino[0] - self.x) * passo
            self.y += (self.destino[1] - self.y) * passo
            self.escala -= dt * 2.2
            self.angulo += dt * 400
            if self.escala <= 0.05:
                self.kill()  # entrou na lixeira: some do jogo
                return
        elif self.estado == 'caindo':
            self.velocidade_y += 1300 * dt
            self.y += self.velocidade_y * dt
            self.x += 120 * dt
            self.angulo -= dt * 300
            if self.y > HEIGHT + 80:
                self.kill()  # saiu da tela
                return
        self.atualiza_imagem()

    def atualiza_imagem(self):
        escala = self.escala
        if self.estado == 'arrastando':
            escala = escala * 1.18  # fica maior enquanto está na mão
        self.image = pygame.transform.rotozoom(self.imagem_original, self.angulo, escala)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class Lixeira(pygame.sprite.Sprite):
    # Lixeira colorida que recebe os lixos. Abre a tampa e se mexe ao receber um lixo.
    def __init__(self, chave, centro_x, base_y):
        pygame.sprite.Sprite.__init__(self)

        self.chave = chave
        # posição do corpo da lixeira (a imagem é um pouco maior, para caber tampa, sombra e brilho)
        self.corpo = pygame.Rect(0, 0, LIXEIRA_LARGURA, LIXEIRA_ALTURA)
        self.corpo.midbottom = (centro_x, base_y)
        self.abertura = 0  # 0 = tampa fechada, 1 = aberta
        self.abrir = False  # True quando um lixo arrastado está em cima
        self.tremor = 0  # > 0 quando errou (balança de lado)
        self.pulo = 0  # > 0 quando acertou (dá um pulinho)
        self.destaque = 0  # > 0 quando deve piscar (lixeira certa depois de um erro)
        self.desenha_imagem()

    def boca(self):
        # Ponto para onde os lixos voam ao entrar na lixeira
        return (self.corpo.centerx, self.corpo.y + 30)

    def area_soltar(self):
        # Área (um pouco maior que a lixeira) onde dá para soltar o lixo
        return self.corpo.inflate(16, 60).move(0, -20)

    def update(self, dt):
        if self.abrir or self.pulo > 0:
            alvo = 1
        else:
            alvo = 0
        self.abertura += (alvo - self.abertura) * min(1, dt * 14)
        self.tremor = max(0, self.tremor - dt)
        self.pulo = max(0, self.pulo - dt)
        self.destaque = max(0, self.destaque - dt)
        self.desenha_imagem()

    def desenha_imagem(self):
        largura = LIXEIRA_LARGURA
        altura = LIXEIRA_ALTURA
        self.image = pygame.Surface((largura + 40, altura + 70), pygame.SRCALPHA)
        dx = 0
        dy = 0
        if self.tremor > 0:
            dx = math.sin(self.tremor * 60) * 8
        if self.pulo > 0:
            dy = -abs(math.sin(self.pulo * 10)) * 18
        # sombra no chão
        sombra = pygame.Surface((largura, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 60), sombra.get_rect())
        self.image.blit(sombra, (20, 45 + altura - 14))
        # a lixeira certa pisca depois de um erro
        piscando = self.destaque > 0 and int(self.destaque * 6) % 2 == 0
        lixeira(self.image, (20 + dx, 45 + dy, largura, altura), self.chave, self.abertura, piscando)

        self.rect = self.image.get_rect()
        self.rect.x = self.corpo.x - 20
        self.rect.y = self.corpo.y - 45


class Particula(pygame.sprite.Sprite):
    # Confete que voa, cai com gravidade e some
    def __init__(self, x, y, velocidade=300, gravidade=600, vida=1.0):
        pygame.sprite.Sprite.__init__(self)

        angulo = random.uniform(0, 2 * math.pi)
        v = random.uniform(0.3, 1.0) * velocidade
        self.x = x
        self.y = y
        self.velocidade_x = math.cos(angulo) * v
        self.velocidade_y = math.sin(angulo) * v - velocidade * 0.4
        self.gravidade = gravidade
        self.vida = vida  # segundos até sumir
        self.cor = random.choice(CORES_CONFETE)
        self.tamanho = random.randint(5, 10)
        self.giro = random.uniform(0, 6)
        self.desenha_imagem()

    def update(self, dt):
        self.velocidade_y += self.gravidade * dt
        self.x += self.velocidade_x * dt
        self.y += self.velocidade_y * dt
        self.vida -= dt
        self.giro += dt * 10
        if self.vida <= 0 or self.y > HEIGHT + 20:
            self.kill()
        else:
            self.desenha_imagem()

    def desenha_imagem(self):
        # Um retângulo que fica mais fino e mais largo, como um papelzinho girando
        largura = int(self.tamanho * abs(math.cos(self.giro)))
        if largura < 1:
            largura = 1
        self.image = pygame.Surface((largura, self.tamanho))
        self.image.fill(self.cor)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class TextoFlutuante(pygame.sprite.Sprite):
    # Texto que sobe e desaparece (ex.: "+100", "Muito bem!")
    def __init__(self, conteudo, pos, cor, tamanho=34, vida=1.3):
        pygame.sprite.Sprite.__init__(self)

        self.conteudo = conteudo
        self.x = pos[0]
        self.y = pos[1]
        self.cor = cor
        self.tamanho = tamanho
        self.vida = vida
        self.vida_total = vida
        self.desenha_imagem()

    def update(self, dt):
        self.y -= 45 * dt
        self.vida -= dt
        if self.vida <= 0:
            self.kill()
        else:
            self.desenha_imagem()

    def desenha_imagem(self):
        # cresce rapidinho logo que aparece
        progresso = 1 - self.vida / self.vida_total
        tamanho = int(self.tamanho * min(1.0, 0.6 + progresso * 4))
        self.image = imagem_texto(self.conteudo, tamanho, self.cor, 3)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class LixoCaindo(pygame.sprite.Sprite):
    # Lixinho que cai do céu girando (enfeite da tela de parabéns)
    def __init__(self, assets, todos_lixos):
        pygame.sprite.Sprite.__init__(self)

        self.assets = assets
        self.todos_lixos = todos_lixos  # lista de lixos de dados.py para sortear
        self.sorteia()
        self.desenha_imagem()

    def sorteia(self):
        # Sorteia um lixo novo, acima da tela
        self.chave = random.choice(self.todos_lixos)['desenho']
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(-400, -60)
        self.velocidade = random.uniform(120, 240)
        self.angulo = random.uniform(0, 360)
        self.giro = random.uniform(-180, 180)

    def update(self, dt):
        self.y += self.velocidade * dt
        self.angulo += self.giro * dt
        if self.y > HEIGHT + 60:
            self.sorteia()  # volta lá para cima
        self.desenha_imagem()

    def desenha_imagem(self):
        self.image = pygame.transform.rotozoom(self.assets['itens'][self.chave], self.angulo, 60 / TAMANHO_ITEM)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
