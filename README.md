# Coletando ♻️

Jogo educativo para crianças, feito em Python com PyGame, que ensina a separar o lixo reciclável.

## Integrantes do grupo

- Eduardo Marques
- Igor Matheus
- Mateus Galatro

## Vídeo do jogo funcionando

---

## Descrição

Estamos dentro de uma **Central de Triagem**. Uma esteira traz vários lixos e a criança precisa
**arrastar cada um até a lixeira certa**:

| Lixeira   | Cor      |
| --------- | -------- |
| Plástico | Vermelha |
| Papel     | Azul     |
| Vidro     | Verde    |
| Metal     | Amarela  |
| Orgânico | Marrom   |

As cores seguem o padrão brasileiro da coleta seletiva (Resolução CONAMA 275).

### Regras

- O jogo tem **3 fases**. A esteira fica mais rápida a cada fase, e a música também.
- Fases 1 e 2: **10 lixos**. Fase 3: **15 lixos**, todos diferentes e mais difíceis
  (isopor, papel-alumínio, caixa de ovos...).
- **Dificuldade:** antes da fase 1 o jogo pergunta a dificuldade, que vale para as 3 fases:
  | Dificuldade | Ajudas por fase |
  | ----------- | --------------- |
  | Fácil      | Todas (2)       |
  | Médio      | Metade (1)      |
  | Difícil    | Nenhuma         |
- **Ajudas:** em cada fase a criança pode **clicar** em lixos (quantas vezes depende da dificuldade). O jogo **pausa** e mostra
  o que é o objeto, do que ele é feito, em qual lixeira vai e por quê. As lâmpadas no canto
  da tela mostram quantas ajudas ainda restam. Rever a ajuda de um lixo já consultado não gasta outra.
- Soltar na lixeira errada, ou deixar o lixo cair no fim da esteira, conta como erro. O jogo
  mostra qual era a lixeira certa.
- **Estrelas** (fases com 10 lixos): 10 acertos = 3 estrelas, 8 ou 9 = 2, de 4 a 7 = 1, menos de 4 = nenhuma.
  Na fase 3 vale a mesma proporção: 15 = 3, de 12 a 14 = 2, de 6 a 11 = 1.
- É preciso ganhar **2 estrelas** para passar de fase. Se não ganhar, a fase é repetida.
- Ao vencer a fase 3 aparece a animação final: **"Parabéns! Você aprendeu a reciclar um lixo!"**

### Telas

- **Menu** (fachada da central): `PLAY` pergunta a dificuldade e começa a fase 1, `FASES` escolhe uma fase já
  desbloqueada e `SAIR` fecha o jogo.
- **Dificuldade**: fácil, médio ou difícil (aparece antes da fase 1).
- **Partida** (dentro da central): esteira, lixeiras, pontuação, ajudas e progresso da rodada.
- **Resultado** da fase com estrelas animadas.
- **Parabéns** com confete, lixeiras dançando e chuva de lixinhos.

### Controles

| Ação                 | Como                                      |
| ---------------------- | ----------------------------------------- |
| Separar o lixo         | Clicar, segurar e arrastar até a lixeira |
| Ver ajuda              | Clicar (sem arrastar) no lixo             |
| Pausar / Continuar     | `ESC`                                   |
| Ligar / Desligar o som | `M`                                     |

## Como rodar

1. Instale o Python 3 (3.10 ou mais novo).
2. Instale a dependência:

   ```bash
   pip install -r requirements.txt
   ```

   (Usamos o `pygame-ce`, que é compatível com o `pygame` e já tem versão para o Python 3.14.
   Se preferir, `pip install pygame` também funciona em versões do Python que ele suporta.)
3. Na pasta do projeto, rode:

   ```bash
   python jogo.py
   ```

O progresso (fases desbloqueadas e estrelas) é salvo no arquivo `progresso.json`.
Para recomeçar do zero, basta apagar esse arquivo.

## Organização do código

A organização segue o modelo do handout de PyGame da disciplina: cada tela é uma função com o seu
próprio loop, que devolve o estado da próxima tela (`INIT`, `ESCOLHA`, `DIFICULDADE`, `GAME`, `RESULTADO`, `PARABENS`, `QUIT`).

```
jogo.py                 ponto de entrada: abre a janela e troca de tela conforme o estado
config.py               constantes (tela, cores, lixeiras, fases e estados)
assets.py               load_assets(): imagens dos lixos, cenários e sons num dicionário
sprites.py              classes Botao, Lixo, Lixeira, Particula, TextoFlutuante, LixoCaindo
cenarios.py             fundos animados (central por fora e por dentro) e a esteira
desenho.py              funções de desenho: textos, painéis, estrelas, lâmpadas, lixeiras
desenho_itens.py        desenho de cada lixo, feito com formas geométricas
dados.py                catálogo de lixos com as explicações educativas
progresso.py            salvar/carregar progresso e cálculo de estrelas
init_screen.py          tela do menu principal
fases_screen.py         tela de escolha de fases
dificuldade_screen.py   tela de escolha da dificuldade e cálculo das ajudas
game_screen.py          a partida (esteira, lixeiras, ajudas e pausa)
resultado_screen.py     tela de estrelas no fim da fase
parabens_screen.py      animação de vitória
ferramentas/
  gerar_sons.py         sintetiza todas as músicas e efeitos (.wav)
assets/sons/            sons gerados pelo script acima
```

Todos os desenhos e sons foram criados pelo próprio código, sem imagens ou músicas de terceiros.
Para regerar os sons: `python ferramentas/gerar_sons.py`.

## Uso de Inteligência Artificial

_Preencher conforme as regras da disciplina: indicar quais partes do código foram geradas
com IA, qual ferramenta foi usada, e anexar a interação._
