import pygame

pygame.init()

tamanho_tela = (1000, 1000)
tela = pygame.display.set_mode(tamanho_tela)

pygame.display.set_caption("Brick Breaker                                                                  " \
"By .'. José Lopes .'.")


# OBJETOS DO JOGO

bola = pygame.Rect(450, 500, 30, 25)
velocidade_bola_x = 8
velocidade_bola_y = -8

jogador = pygame.Rect(400, 850, 150, 25)
velocidade_jogador = 18

cavaleiro_negro = pygame.Rect(350, 650, 140, 25)
velocidade_cavaleiro = 4
direcao_cavaleiro = 1


# TRILHA SONORA

volume_musica = 0.5

pygame.mixer.music.load(r"D:\_01_CURRICULO_PORTFOLIO\06-AULAS_VS\b.mp3")
pygame.mixer.music.set_volume(volume_musica)
pygame.mixer.music.play(-1)


# BLOCOS

qtde_bloco_linha = 10
qtde_linha_bloco = 5


def criar_blocos(qtde_bloco_linha, qtde_linha_bloco):

    distancia_entre_bloco = 7
    largura_bloco = (
        tamanho_tela[0]
        - (qtde_bloco_linha + 1) * distancia_entre_bloco) / qtde_bloco_linha

    altura_bloco = 20
    distancia_entre_linha = 15

    blocos = []

    for j in range(qtde_linha_bloco):
        for i in range(qtde_bloco_linha):

            x = distancia_entre_bloco + i * (
                largura_bloco + distancia_entre_bloco)

            y = distancia_entre_linha + j * (
                altura_bloco + distancia_entre_linha)

            bloco = pygame.Rect(
                x,
                y,
                largura_bloco,
                altura_bloco)

            blocos.append(bloco)

    return blocos

blocos = criar_blocos(
    qtde_bloco_linha,
    qtde_linha_bloco)


# CORES

cores = {
    "preta": (0, 0, 0),
    "azul": (0, 0, 255),
    "branca": (255, 255, 255),
    "verde": (0, 255, 0),
    "cinza": (80, 80, 100),
    "vermelha": (255,0 ,0)}


# VARIÁVEIS

fonte = pygame.font.SysFont(None, 40)
fonte_2 = pygame.font.SysFont(None, 60)

pontos = 0
vidas = 3
fim_jogo = False
pausado = False
vitoria = False
derrota = False
inicio_jogo = True

tempo_inicio = pygame.time.get_ticks()

clock = pygame.time.Clock()


# MOVIMENTO DO CAVALEIRO NEGRO

def movimentar_cavaleiro():

    global direcao_cavaleiro

    cavaleiro_negro.x +=velocidade_cavaleiro * direcao_cavaleiro

    if cavaleiro_negro.left <= 0:
        direcao_cavaleiro = 3

    if cavaleiro_negro.right >= tamanho_tela[0]:
        direcao_cavaleiro = -3


# MOVIMENTO DO JOGADOR

def movimentar_jogador():

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_RIGHT]:
        jogador.x += velocidade_jogador

    if teclas[pygame.K_LEFT]:
        jogador.x -= velocidade_jogador

    if jogador.left < 0:
        jogador.left = 0

    if jogador.right > tamanho_tela[0]:
        jogador.right = tamanho_tela[0]


# MOVIMENTO DA BOLA

def movimentar_bola():

    global velocidade_bola_x
    global velocidade_bola_y
    global pontos
    global vidas
    global fim_jogo
    global derrota
    
    bola.x += velocidade_bola_x
    bola.y += velocidade_bola_y


    if bola.left <= 0 or bola.right >= tamanho_tela[0]:
        velocidade_bola_x *= -1

    if bola.top <= 0:
        velocidade_bola_y *= -1

    if bola.colliderect(jogador):
        velocidade_bola_y *= -1

    if bola.colliderect(cavaleiro_negro):
        velocidade_bola_y *= -1

    for bloco in blocos:
        if bola.colliderect(bloco):
            velocidade_bola_y *= -1
            blocos.remove(bloco)
            pontos += 10
            break

    if bola.bottom >= tamanho_tela[1]:
        vidas -= 1

        if vidas <= 0:
           vidas  = 0
           derrota = True
           fim_jogo = True
        
        else:
            bola.x = 450
            bola.y = 500

            velocidade_bola_y = -5


pontos = 0
vidas = 3
fim_jogo = False


# TELA DE ABERTURA

camada_abertura = pygame.Surface(tamanho_tela,
pygame.SRCALPHA)

camada_abertura.fill((0, 0, 0, 100))


# TELA DA DERROTA

def tela_derrota():

    tempo_inicio = pygame.time.get_ticks()

    esperando = True

    while esperando:
        tela.fill(cores["cinza"])

        mensagem = fonte_2.render(
        "GAME OVER", True,
        cores["vermelha"])

        tela.blit(
        mensagem,
        (325, 350))

        mensagem_2 = fonte.render(
            "Esc _ Sair do Jogo",
            True,
            cores["preta"])

        tela.blit(
            mensagem_2,
            (tamanho_tela[0] // 2 - 180, 110))
        
        mensagem_3 = fonte.render(
            "Enter _ Jogar Novamente",
            True,
            cores["preta"])

        tela.blit(
            mensagem_3,
            (tamanho_tela[0] // 2 - 220, 75))
        
        texto_pontos = fonte.render(
            f"Pontos: {pontos}",
            True,
            cores["branca"])

        tela.blit(
            texto_pontos,
            (tamanho_tela[0] // 2 - 120,
            tamanho_tela[1] // 2))


        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                esperando = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    esperando = False

                if event.key == pygame.K_RETURN:
                    reiniciar_jogo()
                    esperando = False






                   
                   
# REINICIAR JOGO

def reiniciar_jogo():

    global pontos
    global vidas
    global fim_jogo
    global derrota
    global pausado
    global velocidade_bola_x
    global velocidade_bola_y
    global blocos

    pontos = 0
    vidas = 3

    fim_jogo = False
    derrota = False
    pausado = False

    bola.x = 450
    bola.y = 500

    velocidade_bola_x = 7.5
    velocidade_bola_y = -7.5

    jogador.x = 400
    jogador.y = 850

    blocos = criar_blocos(
        qtde_bloco_linha,
        qtde_linha_bloco)


# LOOP PRINCIPAL DO JOGO

while not fim_jogo:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            fim_jogo = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                fim_jogo = True

            if event.key == pygame.K_UP:
                volume_musica += 0.1
                pygame.mixer.music.set_volume(volume_musica)

            if event.key == pygame.K_DOWN:
                volume_musica -= 0.1
                pygame.mixer.music.set_volume(volume_musica)

            if event.key == pygame.K_SPACE:
                pausado = not pausado

    if not pausado:
        movimentar_jogador()
        movimentar_cavaleiro()

    if not pausado and not inicio_jogo:
        movimentar_bola()

    tela.fill(cores["cinza"])

    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores["branca"], bola)
    pygame.draw.rect(tela, cores["preta"], cavaleiro_negro)

    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

    if inicio_jogo:
        tela.blit(camada_abertura, (0, 0))

        tempo_passado = (
            pygame.time.get_ticks() - tempo_inicio) // 1000

        texto_abertura = fonte_2.render(
            "BRICK BREAKER v33",
            True,
            cores["branca"])

        tela.blit(
            texto_abertura,
            (tamanho_tela[0] // 2 - 240, 140))
        
        texto_regra1 = fonte.render(
            "Esq  _  Dir  Jogador",
            True,
            cores["branca"])

        texto_regra2 = fonte.render(
            "Max  _  Min  Música",
            True,
            cores["branca"])

        texto_regra3 = fonte.render(
            "Espaço  _  Pausar",
            True,
            cores["branca"])

        texto_regra4 = fonte.render(
            "Esc  _  Sair",
            True,
            cores["branca"])

        tela.blit(texto_regra1,
                 (tamanho_tela[0] // 2 - 160, 220))

        tela.blit(texto_regra2,
                 (tamanho_tela[0] // 2 - 150, 260))

        tela.blit(texto_regra3,
                 (tamanho_tela[0] // 2 - 140, 300))

        tela.blit(texto_regra4,
                 (tamanho_tela[0] // 2 - 130, 340))

        contagem = 7 - tempo_passado

        if contagem > 0:

            texto_contagem = fonte_2.render(
                str(contagem),
                True,
                cores["branca"])

            tela.blit(texto_contagem,
                     (tamanho_tela[0] // 2 - 20,
                      tamanho_tela[1] // 2 - 40))

        else:

            inicio_jogo = False

    texto_pontos = fonte.render(
        f"Pontos: {pontos}",
        True,
        cores["preta"])

    texto_vidas = fonte.render(
        f"Vidas: {vidas}",
        True,
        cores["preta"])

    tela.blit(texto_pontos, (20, 20))
    tela.blit(texto_vidas, (20, 60))

    pygame.display.flip()

    clock.tick(60)

    if derrota:
      tela_derrota()

pygame.quit()