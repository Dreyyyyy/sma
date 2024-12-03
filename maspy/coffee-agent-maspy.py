# Creating a simple agent using the Python library MASPY

from maspy import *

class CoffeAgent(Agent):
  @pl(gain, Belief("make_coffee")) # Define the agent's plan
  
  def make_coffee(self, src):
    self.print("Making coffee")
    self.stop_cycle()

coffee = CoffeAgent() # instance of the agent class
coffee.add(Belief("make_coffee")) # add the belief to the agent

Admin().start_system()