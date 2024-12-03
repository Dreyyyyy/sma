from maspy import *
import random

class Bed(Environment):
    def __init__(self, env_name):
        super().__init__(env_name)
        self.create(Percept("bedHasDirty"))

    def bed_clean_dirty(self, src):
        dirtyBedroom = random.choice([True, False])

        print(f"Bedroom: {dirtyBedroom}")    

        self.create(Percept("bedNeedMop"))

    def bed_mop_floor(self, src):
        self.print("Bedroom Floor mopped.")
        self.create(Percept("bedHasMoped"))

class VacuumCleanerBed(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)

    @pl (gain, Belief("bedHasDirty"))
    def verify_dirty_bed(self, src):
        perception = self.get(Belief("bedHasDirty"))
        
        if perception:
            self.print("Bedroom Dirty's been verified...")
            self.bed_clean_dirty()
            self.print("Dirty from bedroom cleaned, now can mop!\n")  

    @pl (gain, Belief("bedNeedMop"))
    def need_mop_bed_floor(self, src):
        perception = self.get(Belief("bedNeedMop"))
        
        if perception:
            self.print("Bedroom's floor needs to be moped, sending it to Mopper...")
            self.send("Mopper", tell, Belief("bedCanMop"), "channel1")
            self.stop_cycle()

class MopperBed(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)

    @pl (gain, Belief("bedCanMop"))
    def mopping(self, src):
        perception = self.get(Belief("bedCanMop"))
        
        if perception:
            self.print("Mopping bedroom's floor...")
            self.bed_mop_floor()
            self.stop_cycle()

if __name__ == "__main__":
    vacuum1 = VacuumCleanerBed("Vacuum")
    mopper1 = MopperBed("Mopper")
    bed = Bed("Bedroom")

    ch1 = Channel("channel1")
    
    Admin().connect_to([vacuum1, mopper1], [ch1, bed])

    Admin().start_system()