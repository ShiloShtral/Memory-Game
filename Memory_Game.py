import random


def init_game(rows: int = 2, columns: int = 4) -> dict:
    """
    Initialize the game with a given board size and shuffled card pairs.

    :param rows: Number of rows on the board.
    :param columns: Number of columns on the board.
    :return: A dictionary with the initial game setup, including the board and scores.
    """
    cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G']
    random.shuffle(cards)

    board = [cards[i * columns:(i + 1) * columns] for i in range(rows)]

    return {
        'rows': rows,
        'columns': columns,
        'score': {'Player1': 0, 'Player2': 0},
        'turn': 'Player1',
        'game_over': False,
        'board': [['*' for _ in range(columns)] for _ in range(rows)],
        'cards': cards
    }


def play(game_data: dict) -> None:
    """
    Run the game loop, managing player turns and checking for matches.

    :param game_data: Dictionary containing the game state and board information.
    """
    while not game_data['game_over']:
        display_board(game_data)

        first_choice = get_player_choice(game_data['turn'], game_data['rows'], game_data['columns'])
        reveal_card(game_data, first_choice)

        display_board(game_data)

        second_choice = get_player_choice(game_data['turn'], game_data['rows'], game_data['columns'])
        reveal_card(game_data, second_choice)

        if check_match(game_data, first_choice, second_choice):
            print(f"{game_data['turn']} found a match!")
            game_data['score'][game_data['turn']] += 1
        else:
            print(f"{game_data['turn']} did not find a match")
            hide_card(game_data, first_choice, second_choice)

        switch_turn(game_data)
        check_game_over(game_data)

    print("Game over")
    print(f"Final scores: Player 1: {game_data['score']['Player1']} | Player 2: {game_data['score']['Player2']}")

    if game_data['score']['Player1'] > game_data['score']['Player2']:
        print("Player 1 won")
    elif game_data['score']['Player2'] > game_data['score']['Player1']:
        print("Player 2 won")
    else:
        print("It's a tie!")


def display_board(game_data: dict) -> None:
    """
    Print the current game board.

    :param game_data: Dictionary containing the game state and board information.
    """
    for row in game_data['board']:
        print(' '.join(row))
    print()


def get_player_choice(player: str, rows: int, columns: int) -> tuple:
    """
    Get the player's choice for a card position.

    :param player: The name of the current player.
    :param rows: Number of rows on the board.
    :param columns: Number of columns on the board.
    :return: A tuple with the chosen row and column.
    """
    while True:
        try:
            row = int(input(f"{player}, choose a row (0-{rows - 1}): "))
            col = int(input(f"{player}, choose a column (0-{columns - 1}): "))
            if 0 <= row < rows and 0 <= col < columns:
                return row, col
            else:
                print(
                    f"Invalid choice. Row must be between 0 and {rows - 1}, column must be between 0 and {columns - 1}.")
        except ValueError:
            print("Invalid input. Please enter integers only.")


def reveal_card(game_data: dict, choice: tuple) -> None:
    """
    Reveal the card at the specified position.

    :param game_data: Dictionary containing the game state and board information.
    :param choice: Tuple with the row and column of the chosen card.
    """
    row, col = choice
    index = row * game_data['columns'] + col
    card = game_data['cards'][index]
    game_data['board'][row][col] = card


def check_match(game_data: dict, first_choice: tuple, second_choice: tuple) -> bool:
    """
    Check if the two chosen cards match.

    :param game_data: Dictionary containing the game state and board information.
    :param first_choice: Tuple with the row and column of the first chosen card.
    :param second_choice: Tuple with the row and column of the second chosen card.
    :return: True if the cards match, otherwise False.
    """
    row1, col1 = first_choice
    row2, col2 = second_choice
    return game_data['board'][row1][col1] == game_data['board'][row2][col2]


def hide_card(game_data: dict, first_choice: tuple, second_choice: tuple) -> None:
    """
    Hide the cards if they do not match.

    :param game_data: Dictionary containing the game state and board information.
    :param first_choice: Tuple with the row and column of the first card.
    :param second_choice: Tuple with the row and column of the second card.
    """
    row1, col1 = first_choice
    row2, col2 = second_choice
    game_data['board'][row1][col1] = '*'
    game_data['board'][row2][col2] = '*'


def switch_turn(game_data: dict) -> None:
    """
    Switch turns between players.

    :param game_data: Dictionary containing the game state and board information.
    """
    game_data['turn'] = 'Player2' if game_data['turn'] == 'Player1' else 'Player1'


def check_game_over(game_data: dict) -> None:
    """
    Determine if the game is over based on matched pairs.

    :param game_data: Dictionary containing the game state and board information.
    """
    total_pairs = (game_data['rows'] * game_data['columns']) // 2
    if sum(game_data['score'].values()) == total_pairs:
        game_data['game_over'] = True
