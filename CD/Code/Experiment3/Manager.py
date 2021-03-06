import Simulation
import PARAMETERS, ENUMS
import gc

class Manager(object):
    def __init__(self):
        self.sims = []

    def run(self,agent_list=None):
        if PARAMETERS.MANAGER_FULL_COLLECT:
            return self.run_greedy(agent_list=agent_list)
        else:
            return self.run_lean(agent_list=agent_list)

    def run_greedy(self,agent_list=None):
        for n in range(0,PARAMETERS.N_GENERATIONS):
            print("Running generation {}".format(n))
            self.sims.append(Simulation.Simulation(agent_list))
            self.sims[n].run_simulation()
            agent_list = self.sims[n].breed()
            #self.sims[n].print_leaderboard()
            if PARAMETERS.GARBAGE_COLLECTION:
                collected = gc.collect()
                if PARAMETERS.DEBUG:
                    print("GC - collect {}".format(gc.collect()))
                    print("\n\n---------------------------\n\n")

        return self.sims

    def run_lean(self,agent_list=None):
        genes = ["personal_experience","rep_weighting","false_feedback","prob_defect"]
        stats = {}
        stats["strategy_breakdown"] = []
        stats["gene_breakdown"] = {}
        for g in genes:
            stats["gene_breakdown"][g] = []
        for n in range(0,PARAMETERS.N_GENERATIONS):
            print("Running generation {}".format(n))
            sim = Simulation.Simulation(agent_list)
            sim.run_simulation()
            agent_list = sim.breed()
            stats["strategy_breakdown"].append(sim.agent_list.strategy_breakdown())#
            for g in genes:
                stats["strategy_breakdown"].append(sim.agent_list.gene_score(g))
            #self.sims[n].print_leaderboard()
            if PARAMETERS.GARBAGE_COLLECTION:
                collected = gc.collect()
                if PARAMETERS.DEBUG:
                    print("GC - collect {}".format(gc.collect()))
                    print("\n\n---------------------------\n\n")

        return stats