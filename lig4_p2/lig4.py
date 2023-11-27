import pygame
import sys
import constantes as cte
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("192.168.31.15", 1883, 10) 
client.subscribe("player1/jogada")
client.subscribe("player1/status")
client.loop_start()

# Matriz do jogo
matriz_tabuleiro = [[' ' for _ in range(cte.COLUNAS)] for _ in range(cte.LINHAS)]

# Inicialização do Pygame
pygame.init()

# Configurações da janela
janela = pygame.display.set_mode((cte.LARGURA, cte.ALTURA))
pygame.display.set_caption("Lig 4")

def desenhar_tabuleiro():
    for coluna in range(cte.COLUNAS):
        for linha in range(cte.LINHAS):
            retangulo = pygame.Rect(coluna * cte.TAMANHO_CASA, linha * cte.TAMANHO_CASA, cte.TAMANHO_CASA, cte.TAMANHO_CASA)
            pygame.draw.rect(janela, cte.VERDE_AGUA, retangulo)
            pygame.draw.circle(janela, cte.BRANCO, (coluna * cte.TAMANHO_CASA + cte.TAMANHO_CASA // 2, linha * cte.TAMANHO_CASA + cte.TAMANHO_CASA // 2), cte.TAMANHO_CASA // 2 - cte.BORDA)

def verificar_vencedor(tabuleiro, jogador, linha, coluna, direcao):
    if direcao == 'vertical':
        count = 0
        for l in range(linha, min(cte.LINHAS, linha + 4)):
            if tabuleiro[l][coluna] == jogador:
                count += 1
            else:
                break
        if count == 4:
            return True
    elif direcao == 'horizontal':
        count = 0
        for c in range(coluna, min(cte.COLUNAS, coluna + 4)):
            if tabuleiro[linha][c] == jogador:
                count += 1
            else:
                break
        if count == 4:
            return True
    elif direcao == 'diagonal_direita':
        count = 0
        for i in range(4):
            l, c = linha + i, coluna + i
            if 0 <= l < cte.LINHAS and 0 <= c < cte.COLUNAS:
                if tabuleiro[l][c] == jogador:
                    count += 1
                else:
                    break
        if count == 4:
            return True
    elif direcao == 'diagonal_esquerda':
        count = 0
        for i in range(4):
            l, c = linha + i, coluna - i
            if 0 <= l < cte.LINHAS and 0 <= c < cte.COLUNAS:
                if tabuleiro[l][c] == jogador:
                    count += 1
                else:
                    break
        if count == 4:
            return True

    return False
def verificar_empate(tabuleiro):
    return all(all(c != ' ' for c in linha) for linha in tabuleiro)
def main():

    jogador_atual = "O"  # Começa com o jogador 1

    def sub_jogada(client, userdata, message):
        cte.COORD = str(message.payload.decode('utf-8'))
    def sub_status(client, userdata, message):
        cte.JOGADA_STATUS = str(message.payload.decode('utf-8'))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            client.message_callback_add("player1/status", sub_status)
            client.message_callback_add("player1/jogada", sub_jogada)

            if(cte.COORD != ''):
                coord = cte.COORD.split()
                linha = int(coord[0])
                coluna = int(coord[1])
                if matriz_tabuleiro[linha][coluna] == " ":
                    jogador = "X"
                    cor = cte.VERMELHO
                    pygame.draw.circle(janela, cor, (coluna * cte.TAMANHO_CASA + cte.TAMANHO_CASA // 2, linha * cte.TAMANHO_CASA + cte.TAMANHO_CASA // 2), cte.TAMANHO_CASA // 2 - cte.BORDA)
                    matriz_tabuleiro[linha][coluna] = jogador

            if(cte.JOGADA_STATUS == "p2"):
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    pos_mouse = pygame.mouse.get_pos()
                    coluna = pos_mouse[0] // cte.TAMANHO_CASA
                    for linha in range(cte.LINHAS - 1, -1, -1):
                        if matriz_tabuleiro[linha][coluna] == " ":
                            jogador = "O"
                            cor = cte.AMARELO
                            pygame.draw.circle(janela, cor, (coluna * cte.TAMANHO_CASA + cte.TAMANHO_CASA // 2, linha * cte.TAMANHO_CASA + cte.TAMANHO_CASA // 2), cte.TAMANHO_CASA // 2 - cte.BORDA)
                            matriz_tabuleiro[linha][coluna] = jogador
                            client.publish("player2/jogada", f"{linha} {coluna}", qos=0)
                            cte.JOGADA_STATUS = "p1"
                            client.publish("player2/status", cte.JOGADA_STATUS, qos=0)
                            
                            for direcao in ['vertical', 'horizontal', 'diagonal_direita', 'diagonal_esquerda']:
                                if verificar_vencedor(matriz_tabuleiro, jogador, linha, coluna, direcao):
                                    print(f"Jogador {jogador} venceu!")
                                    pygame.quit()
                                    sys.exit()

                            if verificar_empate(matriz_tabuleiro):
                                print("Empate!")
                                pygame.quit()
                                sys.exit()
                            break

        pygame.display.update()

if __name__ == "__main__":
    janela.fill(cte.VERDE_AGUA)
    desenhar_tabuleiro()
    main()
