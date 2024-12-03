from maspy import *
import random

class Bedroom(Environment):
    def __init__(self, env_name):
        super().__init__(env_name)
        self.create(Percept("bedHasDirty"))

    def bed_clean_dirty(self, src):
        dirtyBedroom = random.choice([True, False])

        print(f"Bedroom: {dirtyBedroom}")    
    def bed_mop_floor(self, src):
        self.print("Bedroom Floor mopped.")

class VacuumCleanerBed(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("bedNeedVacuum"))

    @pl (gain, Belief("bedNeedVacuum"))

    def verify_dirty_bed(self, src):
        self.print("Bedroom Dirty's been verified...")
        perception = self.get(Belief("bedHasDirty", source="Bedroom"))
        
        if perception:
            self.bed_clean_dirty()
            self.add(Belief("bedNeedMop"))
            self.print("Dirty from bedroom cleaned, now can mop!\n")  

        self.perceive("Bedroom")

    @pl (gain, Belief("bedNeedMop"))
    def need_mop_bed_floor(self, src):
        perception = self.get(Belief("bedNeedMop"))
        
        if perception:
            self.print("Bedroom's floor needs to be moped, sending it to Mopper...")
            self.send("Mopper", tell, Belief("bedCanMop"), "channel")
            self.stop_cycle()

class MopperBed(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("bedCannotMop"))

    @pl (gain, Belief("bedCanMop"))
    def mopping(self, src):
        perception = self.get(Belief("bedCanMop"))
        
        if perception:
            self.print("Mopping bedroom's floor...")
            self.bed_mop_floor()
            self.add(Belief("bedHasMoped"))
            self.stop_cycle()

if __name__ == "__main__":
    vacuum2 = VacuumCleanerBed("Vacuum")
    mopper2 = MopperBed("Mopper")
    bed = Bedroom("Bedroom")

    ch = Channel("channel")

    Admin().connect_to([vacuum2, mopper2], [ch, bed])

    Admin().start_system()