import random
import time
import turtle
import math

# Configurações iniciais do Canvas e configurações do fundo
turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.title("Crazy turtle: TARTARUGAS MUITO LOUCAS!!!")
turtle.bgpic("mar.gif")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

# definindo as imagens do jogo
imagens_jogador = ["player_0.gif", "player_45.gif", "player_90.gif", "player_135.gif",
                   "player_180.gif", "player_225.gif", "player_270.gif", "player_315.gif"]
imagem_boss = "boss.gif"
imagem_tela_inicial = "startscreen.gif"
imagem_intro_boss = "bossintro.gif"
imagem_vitoria = "vitoria.gif"
imagem_derrota = "derrota.gif"
imagem_obstaculo = "obstacle.gif"

#registrando as imagens do jogo
for imagem in imagens_jogador:
    turtle.register_shape(imagem)
turtle.register_shape(imagem_boss)
turtle.register_shape(imagem_tela_inicial)
turtle.register_shape(imagem_intro_boss)
turtle.register_shape(imagem_vitoria)
turtle.register_shape(imagem_obstaculo)

# Define o sprite, no caso essa é a base para todas as entidades do jogo, define velocidade, onde começa, cor, etc
class Sprite(turtle.Turtle):
    def __init__(self, forma_sprite, cor, startx, starty):
        turtle.Turtle.__init__(self, shape=forma_sprite)
        self.speed(0)
        self.penup()
        self.color(cor)
        self.fd(0)
        self.goto(startx, starty)
        self.velocidade = 1
# define a movimentação de todas as entidades do jogo
    def mover(self):
        self.fd(self.velocidade) #faz o turtle seguir reto na direção atual
#verifica se o sprite atingiu as bordas
        if self.xcor()  > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
#define a colisão das entidades
    def colidir(self, outro, hitbox_size=20):
        if (self.xcor() >= (outro.xcor() - hitbox_size)) and \
                (self.xcor() <= (outro.xcor() + hitbox_size)) and \
                (self.ycor() >= (outro.ycor() - hitbox_size)) and \
                (self.ycor() <= (outro.ycor() + hitbox_size)):
            return True
        else:
            return False

#define a classe do jogador
class Jogador(Sprite):
    def __init__(self, forma_sprite, cor, startx, starty):
        Sprite.__init__(self, forma_sprite, cor, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.velocidade = 4
        self.atualizar_forma()
#hitbox e aparência do turtle
    def atualizar_forma(self):
        angulo = int(self.heading()) % 360
        indice = (angulo // 45) % 8
        self.shape(imagens_jogador[indice])

    def virar_esquerda(self):
        self.lt(45)
        self.atualizar_forma()

    def virar_direita(self):
        self.rt(45)
        self.atualizar_forma()

    def resetar_posicao(self):
        self.goto(0, 0)
        self.setheading(0)
        self.atualizar_forma()

    def mover(self):
        self.fd(self.velocidade)
        if self.xcor() > 290:
            self.setx(290)
            self.rt(135)
            self.atualizar_forma()
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(135)
            self.atualizar_forma()
        if self.ycor() > 290:
            self.sety(290)
            self.rt(135)
            self.atualizar_forma()
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(135)
            self.atualizar_forma()


# Define o inimigo
class Inimigo(Sprite):
    def __init__(self, forma_sprite, cor, startx, starty):
        Sprite.__init__(self, forma_sprite, cor, startx, starty)
        self.velocidade = 6
        self.setheading(random.randint(0, 360))

    def mover(self):
        self.fd(self.velocidade)
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Chefe(Sprite):
    def __init__(self, forma_sprite, cor, startx, starty):
        Sprite.__init__(self, forma_sprite, cor, startx, starty)
        self.shape(imagem_boss)
        self.shapesize(stretch_wid=100, stretch_len=100, outline=None)
        self.velocidade = 2
        self.setheading(90)
        self.saude = 3

    def mover_para_posicao(self, alvo_x, alvo_y):
        if self.distance(alvo_x, alvo_y) > 5:
            angulo = math.atan2(alvo_y - self.ycor(), alvo_x - self.xcor()) #calcula o angulo pro alvo (player)
            angulo = math.degrees(angulo) #converte pra ângulo
            self.setheading(angulo)
            self.fd(self.velocidade)
        else:
            self.goto(alvo_x, alvo_y)  #o boss vai até o ponto
#define a classe do missil do chefe
class MissilChefe(Sprite):
    def __init__(self, forma_sprite, cor, startx, starty):
        Sprite.__init__(self, forma_sprite, cor, startx, starty)
        self.shapesize(stretch_wid=1, stretch_len=2, outline=None)
        self.velocidade = 9
        self.status = "pronto"
        self.goto(-1000, 1000)

    def disparar(self, alvo):
        if self.status == "pronto":
            self.goto(chefe.xcor(), chefe.ycor())
            angulo = math.atan2(alvo.ycor() - self.ycor(), alvo.xcor() - self.xcor())
            angulo = math.degrees(angulo)
            self.setheading(angulo)
            self.status = "disparando"

    def mover(self):
        if self.status == "pronto":
            self.goto(-1000, 1000)
        if self.status == "disparando":
            self.fd(self.velocidade)
        if self.xcor() < -290 or self.xcor() > 290 or \
           self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "pronto"

# Define o míssil do jogador
class Missil(Sprite):
    def __init__(self, forma_sprite, cor, startx, starty):
        Sprite.__init__(self, forma_sprite, cor, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.velocidade = 20
        self.status = "pronto"
        self.goto(-1000, 1000)

    def disparar(self):
        if self.status == "pronto":
            self.goto(jogador.xcor(), jogador.ycor())
            self.setheading(jogador.heading())
            self.status = "disparando"

    def mover(self):
        if self.status == "pronto":
            self.goto(-1000, 1000)
        if self.status == "disparando":
            self.fd(self.velocidade)
        if self.xcor() < -290 or self.xcor() > 290 or \
           self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "pronto"

# Classe para gerenciar o jogo
class Jogo():
    def __init__(self):
        self.nivel = 1
        self.estado = "tela_inicial"
        self.caneta = turtle.Turtle()
        self.vidas = 3
        self.desenhar_borda()

    def desenhar_borda(self):
        self.caneta.speed(0)
        self.caneta.color("white")
        self.caneta.pensize(3)
        self.caneta.penup()
        self.caneta.goto(-300, 300)
        self.caneta.pendown()
        for _ in range(4):
            self.caneta.fd(600)
            self.caneta.rt(90)
        self.caneta.penup()
        self.caneta.ht()
        self.caneta.pendown()

    def mostrar_status(self):
        self.caneta.clear()  # Limpa a caneta para remover o status anterior
        self.caneta.penup()
        self.caneta.goto(-290, 310)
        self.caneta.write(f"Vidas: {self.vidas}", font=("Arial", 16, "normal"))
        self.caneta.hideturtle()
        if self.estado == "tela_inicial":
            self.caneta.clear()

    def mostrar_tela_inicial(self):
        turtle.clear()
        turtle.bgpic(imagem_tela_inicial)
        turtle.update()

    def mostrar_intro_boss(self):
        turtle.bgpic(imagem_intro_boss)
        turtle.update()
        time.sleep(3)
        turtle.bgpic("mar.gif")


# Define o obstáculo
class Obstaculo(Sprite):
    def __init__(self, forma_sprite, cor, startx, starty):
        Sprite.__init__(self, forma_sprite, cor, startx, starty)
        self.shape(imagem_obstaculo)
        self.velocidade = 1

    def mover(self):
        self.setx(self.xcor() + self.velocidade)
        if self.xcor() > 290 or self.xcor() < -290:
            self.velocidade *= -1 # para voltar

# Inicialização das variáveis e sprites
def iniciar_jogo():
    global jogador, missil, missil_chefe, inimigos, chefe, jogo, obstaculos # usa globla pra acessar tudo certinho
    if jogo.estado == "tela_inicial":
        jogo = Jogo()
        turtle.clear()
        turtle.update()
        jogador = Jogador("triangle", "brown", 0, 0)
        missil = Missil("circle", "black", 10, 10)
        missil_chefe = MissilChefe("circle", "red", 10, 10)
        inimigos = [Inimigo("turtle", "green", -100, 0) for _ in range(dificuldade)]
        turtle.bgpic("mar.gif")
        turtle.clear()
        chefe = None
        obstaculos = []
        jogo.estado = "jogando"
#define quando aperta q reinicia o jogo
def terminar_jogo():
    global jogador, missil, missil_chefe, inimigos, chefe, jogo, obstaculos
    turtle.clear()
    turtle.update()
    jogo.estado = "tela_inicial"
    jogador.hideturtle()
    missil.hideturtle()
    missil_chefe.hideturtle()
    if chefe:
        chefe.hideturtle()
    for inimigo in inimigos:
        inimigo.hideturtle()
    for obstaculo in obstaculos:
        obstaculo.hideturtle()
    jogo.caneta.clear()  # Limpa a caneta para remover indicadores de vida sobrepostos
    jogo.mostrar_tela_inicial()


# Inicializa o jogo
jogo = Jogo()

# Variável de dificuldade
dificuldade = 12 # Ajusta a dificuldade conforme necessário

# Bindings de teclado
turtle.onkey(iniciar_jogo, "p")
turtle.onkey(terminar_jogo, "q")
turtle.onkey(lambda: jogador.virar_esquerda(), "Left")
turtle.onkey(lambda: jogador.virar_direita(), "Right")
turtle.onkey(lambda: missil.disparar(), "space")
turtle.listen()

# Mostra a tela inicial
jogo.mostrar_tela_inicial()

# Loop principal do jogo
while True:
    #define as ações iniciais do jogo
    if jogo.estado == "jogando":
        turtle.update()
        time.sleep(0.02)
        jogador.mover()
        missil.mover()
        jogo.mostrar_status()
        #faz com que os inimigos fiquem mais rápidos quando restam apenas 5 inimigos
        if len(inimigos) <= 3:
            for inimigo in inimigos:
                inimigo. pade = 8
        for inimigo in inimigos[:]:
            inimigo.mover()
        #condicional caso o player colida com um inimigo
            if jogador.colidir(inimigo):
                inimigos.remove(inimigo)
                inimigo.hideturtle()
                jogo.vidas -= 1 #caso colida perde uma vida
                jogo.mostrar_status()
                if jogo.vidas == 0: #se a vida for = 0 chama a flag derrota
                    jogo.estado = "derrota"
        #condicional caso o player acerte um projétil no inimigo
            if missil.colidir(inimigo):
                inimigos.remove(inimigo)
                inimigo.hideturtle()
                missil.status = "pronto"
                jogo.mostrar_status()
        if jogo.vidas == 0: #mantém a condicional de derrota
            jogo.estado = "derrota"
        # caso o números de inimigos seja = 0, e o chefe esteja None (como setado no início), começa a fase 2
        if len(inimigos) == 0 and chefe is None:
            jogador.resetar_posicao() #vai pra posição inicial da fase 2
            jogo.mostrar_intro_boss()
            chefe = Chefe(imagem_boss, "red", 0, -400)
            jogo.nivel += 1
            #cria a lista de obstáculos
            obstaculos = [
                Obstaculo("square", "grey", -100, 100),
                Obstaculo("square", "grey", 100, -100),
                Obstaculo("square", "grey", -100, 50),
                Obstaculo("square", "grey", 100, -50)
            ]
        if chefe:
            chefe.mover_para_posicao(0, -50)
            missil_chefe.mover() #move o boss até a posição inicial
            if missil_chefe.status == "pronto":
                missil_chefe.disparar(jogador)
            #caso o míssíl colida com o jogador
            if jogador.colidir(missil_chefe):
                missil_chefe.status = "pronto"
                jogo.vidas -= 1
                jogo.mostrar_status()
                if jogo.vidas == 0:
                    jogo.estado = "derrota"
            #testa a colisão do míssil do player no boss
            if missil.colidir(chefe, hitbox_size=60):
                chefe.saude -= 1
                missil.status = "pronto"
            #caso a vida do boss seja = 0
                if chefe.saude == 0:
                    chefe.hideturtle()
                    for obstaculo in obstaculos:
                        obstaculo.hideturtle()
                    jogo.estado = "vitoria"
            #move os obstáculos
            for obstaculo in obstaculos:
                obstaculo.mover()
            #caso o jogador colida com um obstáculo, perde na hora
                if jogador.colidir(obstaculo):
                    jogo.estado = "derrota"
    #definição do estado do jogo = vitória
    if jogo.estado == "vitoria":
        turtle.clear()
        turtle.resetscreen
        turtle.bgpic(imagem_vitoria)
        turtle.update()
        time.sleep(0.1)
        turtle.clear()
        jogo.estado = "tela_inicial"
    # definição do estado do jogo = derrota
    if jogo.estado == "derrota":
        turtle.clear()
        turtle.resetscreen
        turtle.update()
        turtle.bgpic(imagem_derrota)
        turtle.update()
        time.sleep(0.1)
        jogo.estado = "tela_inicial"
        turtle.update()
    #tela inicial
    elif jogo.estado == "tela_inicial":
        turtle.update()
        time.sleep(0.1)

turtle.done()
