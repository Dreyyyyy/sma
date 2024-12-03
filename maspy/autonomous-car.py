from maspy import *

import random

class Car(Agent):
  def __init__(self, agt_name):
    super().__init__(agt_name)
    self.add(Belief("obstacle"))

    @pl(gain, Goal("maneuver"), Belief("obstacle"))
    def exec_maneuver(self, src):
      self.print("Executing maneuver")
      maneuver = random.choice([True, False])

      if maneuver == True:
        self.print("Maneuver executed sucessfully")
      else: self.add(Goal("critical_maneuver"))

    @pl(gain, Goal("critical_maneuver"), Belief("obstacle"))
    def inform_stakeholder(self, src):
      self.print("Informing stakeholder")
      self.stop_cycle()

car1 = Car("Waymo")
car1.add(Goal("maneuver"))

Admin().start_system()