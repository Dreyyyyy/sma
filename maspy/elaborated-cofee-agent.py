# A coffee maker agent with distinct isntances using MASPY

from maspy import *

class CoffeeMaker(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("have_water")) # Initial belief

    @pl(gain, Belief("have_water"), Belief("have_coffee")) # Define the agent's plan
    def espresso_machine_ready(self, src):
        self.print("Espresso machine's ready!")
        self.add(Goal("make_coffee"))

    @pl(gain, Goal("make_coffee")) # Define the agent's plan
    def make_coffee(self, src):
        self.print("Make coffee!")
        self.stop_cycle()

    @pl(gain, Belief("have_water"), Belief("filter")) # Define the agent's plan
    def coffee_machine_ready(self, src):
        self.print("Coffee machine's ready!")
        self.add(Goal("make_coffee"))

machine1 = CoffeeMaker("Espresso")
machine2 = CoffeeMaker("CoffeMaker")

machine1.add(Belief("have_coffee")) # Add belief
machine2.add(Belief("filter")) # Add belief

Admin().start_system() # Start system