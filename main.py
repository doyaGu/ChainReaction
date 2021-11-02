# Chain Reaction

import json
import pygame
from pygame.locals import *
from time import sleep
from os import path
from sys import exit
from itertools import cycle
from random import choice
from algorithms import *

pygame.init()
mainClock = pygame.time.Clock()
FPS = 30

COLOR = {'RED': (255, 0, 0),
         'GREEN': (0, 255, 0),
         'BLUE': (0, 0, 255),
         'ORANGE': (243, 160, 35),
         'YELLOW': (240, 255, 97),
         'PINK': (255, 0, 127),
         'VIOLET': (151, 22, 191),
         'BROWN': (127, 89, 0),
         'BLACK': (0, 0, 0),
         'WHITE': (255, 255, 255),
         'GRAY': (128, 128, 128)
         }

player_color = [COLOR[k] for i, k in enumerate(COLOR) if i < 8]

font1 = pygame.font.SysFont(None, 48)
font2 = pygame.font.SysFont(None, 72)
font1_height = font1.get_linesize()


def click(button, pos):
    """
    test if the point to click for a particular button is inside a button
    :param button: the surface of the button
    :param pos: (left, top) or (x, y)
    :return: True if the button is clicked, else it returns False.
    """
    rect = button.get_rect(left=pos[0], top=pos[1])
    return rect.collidepoint(pygame.mouse.get_pos())


def initGame(mySurface):
    """
    :return: (players, rows, columns)
    """
    texts = ['Select number of players',
             'Select number of rows   ',
             'Select number of columns']
    spacing = 60  # The width of the spacing between the '<' and '>'.
    text_surfaces = []
    rel_height = 0
    rel_posx = mySurface.get_width() // 12 * 10  # for buttons
    rel_posy = []  # for buttons
    for text in texts:
        text_surface = font1.render(text, True, COLOR['WHITE'], COLOR['BLACK'])
        text_pos = text_surface.get_rect(left=mySurface.get_width() // 18,
                                         centery=mySurface.get_height() // 5 + rel_height)
        rel_posy.append(text_pos.top)
        rel_height += font1_height * 2
        text_surfaces.append((text_surface, text_pos))

    buttons = []
    for content in ['<', '>', '<', '>', '<', '>']:
        buttons.append(font1.render(content, True, COLOR['WHITE'], COLOR['BLACK']))
    for content in ['START', 'LOAD']:
        buttons.append(font2.render(content, True, COLOR['WHITE'], COLOR['BLACK']))
    buttons_pos = []
    for y in rel_posy:
        for _ in range(0, spacing + 1, spacing):
            buttons_pos.append((rel_posx + _, y))
    for i, t in zip(range(2, 0, -1), range(4, 1, -2)):
        buttons_pos.append(((mySurface.get_width() - buttons[-i].get_width()) // 2,
                            mySurface.get_height() - buttons[-i].get_height() * t))

    values = [2, 8, 5]  # [players, rows, columns]
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if click(buttons[0], buttons_pos[0]):
                    if 1 < values[0] < 8:
                        values[0] -= 1
                    elif values[0] == 8:
                        values[0] = 7
                elif click(buttons[1], buttons_pos[1]):
                    if 1 < values[0] < 8:
                        values[0] += 1
                    elif values[0] == 1:
                        values[0] = 2
                elif click(buttons[2], buttons_pos[2]):
                    if 2 < values[1] < 8:
                        values[1] -= 1
                    elif values[1] == 8:
                        values[1] = 7
                elif click(buttons[3], buttons_pos[3]):
                    if 2 < values[1] < 8:
                        values[1] += 1
                    elif values[1] == 2:
                        values[1] = 3
                elif click(buttons[4], buttons_pos[4]):
                    if 2 < values[2] < 8:
                        values[2] -= 1
                    elif values[2] == 8:
                        values[2] = 7
                elif click(buttons[5], buttons_pos[5]):
                    if 2 < values[2] < 8:
                        values[2] += 1
                    elif values[2] == 2:
                        values[2] = 3
                elif click(buttons[6], buttons_pos[6]):
                    return tuple(values)
                elif click(buttons[7], buttons_pos[7]):
                    return loadGame()

        mySurface.fill(COLOR['BLACK'])
        for i, pos in enumerate(buttons_pos):
            mySurface.blit(buttons[i], pos)
        for i, y in zip(values, rel_posy):
            mySurface.blit(font1.render(str(i), True, COLOR['WHITE'], COLOR['BLACK']), (rel_posx + spacing // 2, y))
        for sur in text_surfaces:
            mySurface.blit(*sur)

        pygame.display.update()
        mainClock.tick(FPS)


def saveGame(gameBoard, n, m, nb, player):
    data = {'gameBoard': gameBoard,
            'n': n,
            'm': m,
            'nb': nb,
            'player': player
            }
    with open('save_data.json', 'w') as file:
        json.dump(data, file)


def loadGame():
    if path.exists('save_data.json'):
        with open('save_data.json', 'r') as file:
            data = json.load(file)
        return data
    else:
        return False


def drawCell(cell_surface, cell):
    """
    :param cell_surface: the surface of the cell
    :param cell: the item in the gameBoard. (such as [0, 0])
    """
    if cell[1] == 1:
        pawn_pos = (cell_surface.get_width() // 2, cell_surface.get_height() // 2)
        radius = cell_surface.get_width() // 7
        pygame.draw.circle(cell_surface, player_color[cell[0] - 1], pawn_pos, radius)
    if cell[1] == 2:
        pawn_pos = [(cell_surface.get_width() // 4, cell_surface.get_height() // 4),
                    (cell_surface.get_width() // 4 * 3, cell_surface.get_height() // 4 * 3)]
        radius = cell_surface.get_width() // 8
        for pos in pawn_pos:
            pygame.draw.circle(cell_surface, player_color[cell[0] - 1], pos, radius)
    if cell[1] == 3:
        pawn_pos = [(cell_surface.get_width() // 4, cell_surface.get_height() // 4),
                    (cell_surface.get_width() // 2, cell_surface.get_height() // 2),
                    (cell_surface.get_width() // 5 * 4, cell_surface.get_height() // 5 * 4)]
        radius = cell_surface.get_width() // 8
        for pos in pawn_pos:
            pygame.draw.circle(cell_surface, player_color[cell[0] - 1], pos, radius)


def adjustBoard(mySurface, margin, border, n, m):
    """
    :param mySurface: the surface where we draw
    :param margin: the same as the margin of the Box Model in CSS
    :param border: the same as the border of the Box Model in CSS
    :param n: the number of rows
    :param m: the number of columns
    :return: board_pos, board_size, cells_pos, cell_size
    """
    board_pos = (margin, margin)
    board_size = (mySurface.get_width() - margin * 2 - border,
                  mySurface.get_height() - margin * 2 - border)

    cell_size = (board_size[0] // m - border, board_size[1] // n - border)
    cells_pos = []
    for y in range(board_pos[0] + border, board_size[1] + margin + border, cell_size[1] + border):
        temp = []
        for x in range(board_pos[1] + border, board_size[0] + margin + border, cell_size[0] + border):
            temp.append((x, y))
        cells_pos.append(temp)
    return board_pos, board_size, cells_pos, cell_size


def drawBoard(mySurface, gameBoard, n, m, player):
    """
    :param mySurface: the surface where we draw
    :param gameBoard: The two dimensional list of the board
    :param n: the number of rows
    :param m: the number of columns
    :param player: the number of the current player
    :return: the list of Rect of the cell
    """
    board_pos, board_size, cells_pos, cell_size = adjustBoard(mySurface, 50, 3, n, m)
    board = pygame.Surface(board_size)
    board.fill(player_color[player - 1])
    cells = []
    mySurface.blit(board, board_pos)
    for temp, row in zip(cells_pos, gameBoard):
        for cell_pos, cell in zip(temp, row):
            cell_rect = pygame.Rect(cell_pos, cell_size)
            cells.append(cell_rect)
            cell_surface = mySurface.subsurface(cell_rect)
            cell_surface.fill(COLOR['BLACK'])
            drawCell(cell_surface, cell)
    return cells


def select(cells, gameBoard, n, m, player):
    """
    :param cells: the list of the Rect of the cell
    :param gameBoard: The two dimensional list of the board
    :param n: the number of rows
    :param m: the number of columns
    :param player: the number of the current player
    :return: the coordinates of the chosen cell
    """
    clicked_pos = pygame.mouse.get_pos()
    for index, cell in enumerate(cells):
        if cell.collidepoint(clicked_pos):
            j, i = divmod(index, m)
            if possible(gameBoard, n, m, i, j, player):
                return i, j
            else:
                return None, None
    return None, None


def computer_select(gameBoard, n, m):
    empty_index = [(x, y) for y in range(n) for x in range(m) if gameBoard[y][x][0] != 1]
    return choice(empty_index)


def gamePlay(mySurface, gameBoard, n, m, nb, player=1):
    """
    :param mySurface: the surface where we draw
    :param gameBoard: The two dimensional list of the board
    :param n: the number of rows
    :param m: the number of columns
    :param nb: the number of the players
    :param player: the current player
    :return: the text which will be used in the gameOver function
    """
    button = font1.render('Save', True, COLOR['WHITE'], COLOR['BLACK'])
    button_pos = (20, mySurface.get_height() - font1_height)
    if nb == 1:
        multiplayer = False
        player_turns = cycle([1, 2])
    else:
        multiplayer = True
        players = [player for player in range(1, nb + 1)]
        player_turns = cycle(players)
    temp = 0
    while temp != player:
        temp = next(player_turns)
    first_turn = True
    check_someone = False
    saved = False
    time = 0
    while True:
        if player == 2 and not multiplayer:
            i, j = computer_select(gameBoard, n, m)
        else:
            i, j = None, None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if not saved and click(button, button_pos):
                        saveGame(gameBoard, n, m, nb, player)
                        saved = True

                cells = drawBoard(mySurface, gameBoard, n, m, player)
                i, j = select(cells, gameBoard, n, m, player)

        mySurface.fill(COLOR['BLACK'])
        if i is None and j is None:
            drawBoard(mySurface, gameBoard, n, m, player)
        else:
            put(gameBoard, n, m, i, j, player)
            if player == 2 and not multiplayer:
                sleep(0.3)
            drawBoard(mySurface, gameBoard, n, m, player)
            if first_turn:
                player = next(player_turns)
                first_turn = False
                continue
            if multiplayer and player == players[-1]:
                check_someone = True
            if check_someone:
                someone = someone_loose(gameBoard, n, m, players)
                if someone:
                    players.remove(someone)
                    player_turns = cycle(players)
                    player = next(player_turns)
            if win(gameBoard, n, m, player):
                return 'Player {} wins !'.format(player)
            if loose(gameBoard, n, m, 1):
                return 'Player 1 lost !'
            player = next(player_turns)

        if saved:
            button = font1.render('Save', True, COLOR['GRAY'], COLOR['BLACK'])
            time += 1
            if time == 5:
                button = font1.render('Save', True, COLOR['WHITE'], COLOR['BLACK'])
                saved = False
                time = 0
        mySurface.blit(button, button_pos)

        pygame.display.update()
        mainClock.tick(FPS)


def gameOver(mySurface, text):
    """
    :param mySurface: the surface where we draw
    :param text: the text which we will print
    :return: True if the player clicks the "Play again", else it returns False.
    """
    text_surface = font2.render(text, True, COLOR['WHITE'])
    text_pos = text_surface.get_rect(centerx=mySurface.get_width() // 2,
                                     centery=mySurface.get_height() // 3)
    buttons = []
    for content in ['Play again', 'Load', 'Quit']:
        buttons.append(font1.render(content, True, COLOR['WHITE']))
    buttons_pos = []
    for i, t in zip(range(3), range(8, 3, -2)):
        buttons_pos.append(((mySurface.get_width() - buttons[i].get_width()) // 2,
                            mySurface.get_height() - buttons[i].get_height() * t))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if click(buttons[0], buttons_pos[0]):
                    return True
                elif click(buttons[1], buttons_pos[1]):
                    return loadGame()
                elif click(buttons[2], buttons_pos[2]):
                    return False
        sleep(0.2)
        for i, pos in enumerate(buttons_pos):
            mySurface.blit(buttons[i], pos)
        mySurface.blit(text_surface, text_pos)

        pygame.display.update()
        mainClock.tick(FPS)


def chainReaction():
    size = width, height = 620, 600
    mySurface = pygame.display.set_mode(size, 0, 32)
    pygame.display.set_caption("Chain Reaction")
    # disable the keyboard
    pygame.event.set_blocked([KEYDOWN, KEYUP])

    data = False
    while True:
        if data and isinstance(data, dict):
            end_text = gamePlay(mySurface, **data)
        else:
            data = initGame(mySurface)
            if isinstance(data, tuple):
                nb, n, m = data
                gameBoard = newBorad(n, m)
                end_text = gamePlay(mySurface, gameBoard, n, m, nb)
            else:
                continue
        if end_text:
            again = gameOver(mySurface, end_text)
            if again:
                data = again
                continue
            else:
                return


if __name__ == '__main__':
    chainReaction()
