from maspy import *

import random

class UrbanMonitoring(Environment):
  def __init__(self, env_name):
    super().__init__(env_name)
    self.create(Percept("tem_obstaculo"))

  def avoid_obstacle(self, src):
    avoid = random.choice([True, False])
    print(avoid)

    if avoid == True:
      self.print("Obstacle avoided")
      self.create(Percept("obstacle_avoided"))
    else:
      self.print("Obstacle not avoided")
      self.create(Percept("obstacle_not_avoided"))

class VA(Agent):
  def __init__(self, agt_name):
    super().__init__(agt_name)
    self.add(Belief("drivingVA"))

    @pl(gain, Belief("drivingVA"))
    def check_urban_way(self, src):
      self.print("Checking urban way")
      perception1 = self.get(Belief("has_obstacle", source="BR101"))
      self.print(perception1.key)

      if perception1:
        self.avoid_obstacle()

      self.perceive("BR101")

      perception2 = self.get(Belief("obstacle_avoided", source="BR101"))

      if perception2:
        self.print("Obstacle avoided successfully")
        self.stop.cycle()
      else:
        perception3 = self.get(Belief("obstacle_not_avoided", source="BR101"))

        if perception3:
          self.add(Belief("obstacle"))
          self.add(Goal("criticalManeuver"))

    @pl(gain, Goal("emergencyManeuver"))
    def exec_maneuver(self, src):
      self.print(f"Maneuver executed sucessfully as stakeholder: {src}")
      self.stop_cycle()

class Stakeholder(Agent):
  def __init__(self, agt_name):
    super().__init__(agt_name)

  @pl(gain, Belief("VAneedHelp"))
  def send_maneuver(self, src):
    self.send("Waymo", achieve, Goal("emergencyManeuver"), "V2C")
    self.stop_cycle()

if __name__ == "__main__":
  monitor = UrbanMonitoring("BR101")
  veichle = VA("Waymo")
  controller = Stakeholder("RemoteControl")
  communication_ch = Channel("V2C")

  Admin().connect_to([veichle, controller], communication_ch)
  Admin().start_system()

