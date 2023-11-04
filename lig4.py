import pygame, sys
import constantes as cte


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

def main():
    jogador_atual = 1  # Começa com o jogador 1
    tabuleiro = [[0] * cte.COLUNAS for _ in range(cte.LINHAS)]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, _ = pygame.mouse.get_pos()
                coluna_selecionada = x // cte.TAMANHO_CASA
                for linha in range(cte.LINHAS - 1, -1, -1):
                    if tabuleiro[linha][coluna_selecionada] == 0:
                        tabuleiro[linha][coluna_selecionada] = jogador_atual
                        jogador_atual = 3 - jogador_atual  # Alternar entre jogador 1 e 2
                    
                  
        janela.fill(cte.VERDE_AGUA)
        desenhar_tabuleiro()
        pygame.display.update()

if __name__ == "__main__":
    main()
