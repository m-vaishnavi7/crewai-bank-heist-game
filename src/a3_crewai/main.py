import sys
import yaml
from a3_crewai.crew import GameBuilderCrew

def run():
    print("## Welcome to the Game Crew")
    print('-------------------------------')

    # Load game design instructions from gamedesign.yaml
    with open('src/a3_crewai/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        gamedesign = yaml.safe_load(file)

    # Load the game template from the templates folder
    with open('src/a3_crewai/config/gametemplate.html', 'r', encoding='utf-8') as template_file:
        template = template_file.read()

    # Prepare inputs using {game} and {template}
    inputs = {
        'game': gamedesign['bank_heist'],  # Generic instructions for a stealth and card-based game
        'template': template
    }

    # Kick off the Crew pipeline, chaining outputs from each task
    final_game_code = GameBuilderCrew().crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("Final HTML code for the game:")
    print(final_game_code)

if __name__ == "__main__":
    run()
