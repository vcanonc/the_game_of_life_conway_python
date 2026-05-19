import os
from random import randrange

ROWS = 30
COLS = 30

LIVE = 1
DEAD = 0


def get_symbols():
    if os.name == "nt":
        return "■ ", "□ "
    return "🟨", "⬛"


LIVE_CELL, DEAD_CELL = get_symbols()


def count_living_neighbors(world, row, col):
    """
    Cuenta las células vivas vecinas alrededor de una posición dada.

    La función revisa las ocho posiciones adyacentes a la célula
    especificada y devuelve cuántas están vivas. Las posiciones
    fuera de los límites del tablero se consideran muertas.

    Args:
        world: Matriz bidimensional que representa el mundo del juego.
        row: Índice de la fila de la célula.
        col: Índice de la columna de la célula.

    Returns:
        El número de vecinos vivos alrededor de la célula.
    """
    count = 0

    for i in range(-1, 2):
        nr = row + i  # Posición de fila del vecino
        for j in range(-1, 2):
            if i == 0 and j == 0:  # Ignorar la propia celda
                continue

            nc = col + j  # Posición de columna del vecino
            if is_alive(world, nr, nc):
                count += 1

    return count


def toroidal_count_living_neighbors(world, row, col):
    """
    Cuenta los vecinos vivos usando un tablero toroidal.

    En un mundo toroidal, los bordes del tablero están conectados:
    salir por un lado hace que se reaparezca por el lado opuesto.

    Args:
        world: Matriz bidimensional que representa el mundo del juego.
        row: Índice de la fila de la célula.
        col: Índice de la columna de la célula.

    Returns:
        El número de vecinos vivos alrededor de la célula.
    """
    count = 0

    for i in range(-1, 2):
        nr = (row + i + ROWS) % ROWS  # Posición de fila del vecino
        for j in range(-1, 2):
            if i == 0 and j == 0:  # Ignorar la propia celda
                continue

            nc = (col + j + COLS) % COLS  # Posición de columna del vecino
            if is_alive(world, nr, nc):
                count += 1

    return count


def is_alive(world, row, col):
    """
    Determina si una célula está viva.

    Si la posición está fuera de los límites del tablero,
    la función devuelve False.

    Args:
        world: Matriz bidimensional que representa el mundo del juego.
        row: Índice de la fila de la célula.
        col: Índice de la columna de la célula.

    Returns:
        True si la célula está viva, False en caso contrario.
    """
    if row < 0 or row >= ROWS:
        return False

    if col < 0 or col >= COLS:
        return False

    return world[row][col] == LIVE


def initialize():
    """
    Inicializa el tablero del juego con células aleatorias.

    Se crea una matriz de tamaño ROWS x COLS con todas las
    células inicialmente muertas. Luego se activan posiciones
    aleatorias del tablero.

    Returns:
        Una matriz bidimensional representando el estado inicial
        del mundo.
    """
    world = [[DEAD for _ in range(COLS)] for _ in range(ROWS)]

    for _ in range(ROWS * COLS // 4):
        r = randrange(ROWS)
        c = randrange(COLS)
        world[r][c] = LIVE

    return world


def update(world):
    """
    Calcula la siguiente generación del juego.

    La actualización sigue las reglas clásicas del
    Juego de la Vida de Conway:

    - Una célula viva muere si tiene menos de 2 vecinos vivos.
    - Una célula viva muere si tiene más de 3 vecinos vivos.
    - Una célula muerta revive si tiene exactamente 3 vecinos vivos.

    Args:
        world: Matriz bidimensional con el estado actual del juego.

    Returns:
        Una nueva matriz con el estado actualizado del mundo.
    """
    new_world = [row.copy() for row in world]
    for r in range(ROWS):
        for c in range(COLS):
            count = count_living_neighbors(world, r, c)
            # count = toroidal_count_living_neighbors(world, r, c)
            if is_alive(world, r, c):
                if count < 2 or count > 3:
                    new_world[r][c] = DEAD
            else:
                if count == 3:
                    new_world[r][c] = LIVE

    return new_world


def print_world(world):
    """
    Imprime el tablero del juego en consola.

    Las células vivas se representan con el simbolo asignado
    para cada caso.

    Args:
        world: Matriz bidimensional que representa el mundo del juego.
    """

    for r in range(ROWS):
        for c in range(COLS):
            if is_alive(world, r, c):
                print(LIVE_CELL, end="")
            else:
                print(DEAD_CELL, end="")
        print()


def main():
    gen = 0
    world = initialize()

    flag = True
    while flag:
        os.system("cls" if os.name == "nt" else "clear")

        print(" ****** EL JUEGO DE LA VIDA DE CONWAY ******")

        print(f"\nGeneración {gen}")
        print_world(world)

        gen += 1

        while True:
            option = input("¿Avanzar a la siguiente generación? (s/n): ")

            if option.lower() == "s" or option == "":
                world = update(world)
                break

            elif option.lower() == "n":
                flag = False
                break

            else:
                print("ERROR: Inserte una opción valida.")


if __name__ == "__main__":
    main()
