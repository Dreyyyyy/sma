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
            self.print("Dirty from bedroom cleaned, now can mop!")  

        self.perceive("Bedroom")

    @pl (gain, Belief("bedNeedMop"))
    def need_mop_bed_floor(self, src):
        perception = self.get(Belief("bedNeedMop"))
        
        if perception:
            self.print("Bedroom's floor needs to be moped, sending it to Mopper_1...")
            self.send("Mopper_1", tell, Belief("bedCanMop"), "channel")

    @pl (gain, Goal("bedCleaned"))
    def stop_clean_bed(self, src):
        self.print("Bedroom's been cleaned, we're done.")
        self.stop_cycle()

class MopperBed(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("bedCannotMop"))

    @pl (gain, Belief("bedCanMop"))
    def mopping_bed(self, src):
        perception = self.get(Belief("bedCanMop"))
        
        if perception:
            self.print("Mopping bedroom's floor...")
            self.bed_mop_floor()
            self.add(Belief("bedHasMoped"))
            self.send("Vacuum_1", achieve, Goal("bedCleaned"), "channel")
            self.stop_cycle()

class Kitchen(Environment):
    def __init__(self, env_name):
        super().__init__(env_name)
        self.create(Percept("kitHasDirty"))

    def kit_clean_dirty(self, src):
        dirtyKitchen = random.choice([True, False])

        print(f"Kitchen: {dirtyKitchen}")    
    def kit_mop_floor(self, src):
        self.print("Kitchen Floor mopped.")

class VacuumCleanerKit(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("kitNeedVacuum"))

    @pl (gain, Belief("kitNeedVacuum"))

    def verify_dirty_kit(self, src):
        # self.wait(3)
        self.print("Kitchen Dirty's been verified...")
        perception = self.get(Belief("kitHasDirty", source="Kitchen"))
        
        if perception:
            self.kit_clean_dirty()
            self.add(Belief("kitNeedMop"))
            self.print("Dirty from kitchen cleaned, now can mop!")  

        self.perceive("Kitchen")

    @pl (gain, Belief("kitNeedMop"))
    def need_mop_kit_floor(self, src):
        perception = self.get(Belief("kitNeedMop"))
        
        if perception:
            self.print("Kitchen's floor needs to be moped, sending it to Mopper_2...")
            self.send("Mopper_2", tell, Belief("kitCanMop"), "channel")

    @pl (gain, Goal("kitCleaned"))
    def stop_clean_kit(self, src):
        self.print("Kitchen's been cleaned, we're done.")
        self.stop_cycle()


class MopperKit(Agent):
    def __init__(self, agent_name):
        super().__init__(agent_name)
        self.add(Belief("kitCannotMop"))

    @pl (gain, Belief("kitCanMop"))
    def mopping_kit(self, src):
        perception = self.get(Belief("kitCanMop"))
        
        if perception:
            self.print("Mopping kitchen's floor...")
            self.kit_mop_floor()
            self.add(Belief("kitHasMoped"))
            self.send("Vacuum_2", achieve, Goal("kitCleaned"), "channel")
            self.stop_cycle()

if __name__ == "__main__":
    vacuum1 = VacuumCleanerBed("Vacuum")
    mopper1 = MopperBed("Mopper")
    bed = Bedroom("Bedroom")

    ch = Channel("channel")

    Admin().connect_to([vacuum1, mopper1], [ch, bed])

    vacuum2 = VacuumCleanerKit("Vacuum")
    mopper2 = MopperKit("Mopper")
    kit = Kitchen("Kitchen")

    Admin().connect_to([vacuum2, mopper2], [ch, kit])

    Admin().start_system()