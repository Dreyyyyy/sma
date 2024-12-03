from maspy import *

class CoffeeMachine(Environment):
    def __init__(self, env_name):
        super().__init__(env_name)
        self.create(Percept("have_water"))

    def make_coffee(self, src):
        self.print(f'Make coffee for the agent: {src}')

class CoffeeAgent(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("want_coffee")) # Initial belief

    @pl(gain, Belief("want_coffee")) # Define the agent's plan
    def machine_ready(self, src):
        self.print("Verify ambient")
        perception1 = self.get(Belief("have_water", source="Espresso"))
        perception2 = self.get(Belief("have_coffee", source="Espresso"))
        self.print(perception1.key) # Print perception's key

        self.print(perception2.key)

        if perception1 and perception2:
            self.make_coffee()
        self.stop_cycle()

if __name__ == "__main__":
    machine = CoffeeMachine("Espresso")
    agent = CoffeeAgent("Coffe35")
    Admin().connect_to([agent], [machine])
    machine.create(Percept("have_coffee"))
    Admin().full_report = True
    Admin().start_system()