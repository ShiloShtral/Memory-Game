from Memory_Game import init_game, play

def main():
    """
    Initializes the game and starts playing.
    """
    game_data = init_game()  # Initialize the game data
    play(game_data)  # Start the game

if __name__ == "__main__":
    main()  # Run the main function if this file is executed
