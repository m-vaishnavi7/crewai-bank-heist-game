from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class GameBuilderCrew:
    """
    GameBuilderCrew for generating a generic stealth and card-based game using a provided template.
    
    Pipeline:
      1. ui_css_generation: Generate HTML/CSS code for the game interface.
      2. game_logic_generation: Generate core game mechanics (grid layout, entity placement, movement functions).
      3. user_input_generation: Generate code to capture and process user inputs.
      4. template_integration: Integrate the generated code segments into the provided template {template}.
      5. testing_and_debugging: Review and optimize the integrated code.
      6. final_output: Save the final code to outputs/game.html.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def ui_css_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_css_agent'],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def game_logic_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['game_logic_agent'],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def user_input_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['user_input_agent'],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def integrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['integrator_agent'],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def reviewer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer_agent'],
            allow_delegation=True,
            verbose=True
        )

    @task
    def ui_css_generation(self) -> Task:
        return Task(
            config=self.tasks_config['ui_css_generation'],
            agent=self.ui_css_agent()
        )

    @task
    def game_logic_generation(self) -> Task:
        return Task(
            config=self.tasks_config['game_logic_generation'],
            agent=self.game_logic_agent()
        )

    @task
    def user_input_generation(self) -> Task:
        return Task(
            config=self.tasks_config['user_input_generation'],
            agent=self.user_input_agent()
        )

    @task
    def template_integration(self) -> Task:
        return Task(
            config=self.tasks_config['template_integration'],
            agent=self.integrator_agent()
        )

    @task
    def testing_and_debugging(self) -> Task:
        return Task(
            config=self.tasks_config['testing_and_debugging'],
            agent=self.reviewer_agent()
        )

    @task
    def final_output(self) -> Task:
        return Task(
            config=self.tasks_config['final_output'],
            agent=self.reviewer_agent()
        )

    @crew
    def crew(self) -> Crew:
        """
        Orchestrates the pipeline sequentially.
        The outputs flow from:
        ui_css_generation -> game_logic_generation -> user_input_generation ->
        template_integration -> testing_and_debugging -> final_output.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
