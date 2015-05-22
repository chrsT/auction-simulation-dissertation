import Simulation
import PARAMETERS, ENUMS

class Manager(object):
    def __init__(self):
        pass

    def run(self):
        agent_list = None
        sim = []
        for n in range(0,PARAMETERS.N_GENERATIONS):
            #print("Running generation {}".format(n))
            sim.append(Simulation.Simulation(agent_list))
            sim[n].run_simulation()
            agent_list = sim[n].breed()
        return sim

    def hypothesis_0_1(self):
        for PARAMETERS.INITIAL_HAWK in range(1,1023,10):
            print("Running simulation for INITIAL_HAWK = {}".format(PARAMETERS.INITIAL_HAWK))
            sim = Simulation.Simulation()
            sim.run_simulation()
            agent_list = sim.order_by_score()
            if self.dove_above_hawk(agent_list):
                print("FAILURE. DOVE ABOVE HAWK.")
                sim.print_leaderboard()
                print("FAILURE. DOVE ABOVE HAWK.")
                return
        print("No dove ever scored higher than a hawk.")

    def dove_above_hawk(self, al):
        dove = False
        for a in al:
            if a.get_gene("strategy") ==  ENUMS.StrategyEnum.dove and dove == False:
                dove = True
            if a.get_gene("strategy") == ENUMS.StrategyEnum.hawk and dove == True:
                return True
        return False