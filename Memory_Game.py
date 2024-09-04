import random


def init_game(rows: int = 2, columns: int = 4) -> dict:
    game_data = {
        'rows': rows,
        'columns': columns,
        'score': {'Player1': 0, 'Player2': 0},
        'turn': 'Player1',
        'game_over': False,
        'board': [['*' for _ in range(columns)] for _ in range(rows)],
        'cards': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G']
    }
    random.shuffle(game_data['cards'])
    return game_data


def play(game_data: dict) -> None:
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
        print("Player 1 wins!")
    elif game_data['score']['Player2'] > game_data['score']['Player1']:
        print("Player 2 wins!")
    else:
        print("It's a tie!")


def display_board(game_data: dict) -> None:
    for row in game_data['board']:
        print(' '.join(row))
    print()


def get_player_choice(player: str, rows: int, columns: int) -> tuple:
    while True:
        try:
            row = int(input(f"{player}, choose a row (0-{rows - 1}): "))
            col = int(input(f"{player}, choose a column (0-{columns - 1}): "))
            if 0 <= row < rows and 0 <= col < columns:
                return row, col
            else:
                print(
                    f"Invalid choice. Please choose a row between 0 and {rows - 1}, and a column between 0 and {columns - 1}.")
        except ValueError:
            print("Invalid input. Please enter valid integers.")


def reveal_card(game_data: dict, choice: tuple) -> None:
    row, col = choice
    index = row * game_data['columns'] + col
    card = game_data['cards'][index]
    game_data['board'][row][col] = card


def check_match(game_data: dict, first_choice: tuple, second_choice: tuple) -> bool:
    row1, col1 = first_choice
    row2, col2 = second_choice
    return game_data['board'][row1][col1] == game_data['board'][row2][col2]


def hide_card(game_data: dict, first_choice: tuple, second_choice: tuple) -> None:
    row1, col1 = first_choice
    row2, col2 = second_choice
    game_data['board'][row1][col1] = '*'
    game_data['board'][row2][col2] = '*'


def switch_turn(game_data: dict) -> None:
    game_data['turn'] = 'Player2' if game_data['turn'] == 'Player1' else 'Player1'


def check_game_over(game_data: dict) -> None:
    total_pairs = (game_data['rows'] * game_data['columns']) // 2
    if sum(game_data['score'].values()) == total_pairs:
        game_data['game_over'] = True

