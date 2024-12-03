from maspy import *

class VA(Agent):
  def __init__(self, agt_name):
    super().__init__(agt_name)
    self.add(Belief("obstacle"))
    self.add(Goal("criticalManeuver"))

  @pl(gain, Goal("criticalManeuver"), Belief("obstacle"))
  def inform_stakeholder(self, src):
    self.print("Critical Maneuver: Informing stakeholder")
    self.send("RemoteControl", tell, Belief("VAneedHelp"), "V2C")

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
  veichle = VA("Waymo")
  controller = Stakeholder("RemoteControl")
  communication_ch = Channel("V2C")

  Admin().connect_to([veichle, controller], communication_ch)
  Admin().report = True
  Admin().start_system()