#!/usr/bin/python3
import Simulation
import matplotlib.pyplot as plt
from Genetics import StrategyGene
import scipy.stats
import PARAMETERS
import RANDOMS

def hypothesis_1_1():
    PARAMETERS.N_AGENTS = 1000
    PARAMETERS.TRANSACTIONS_PER_AGENT = 1000
    PARAMETERS.INITIAL_HAWK = 300
    PARAMETERS.VERBOSE_SIMULATIONS = True
    sim = Simulation.Simulation()
    sim.run_simulation()
    agents = sim.agent_list

    x = []
    y = []
    for a in agents:
        if StrategyGene.enum_to_str(a.get_gene("strategy")) == "D":
            x.append(a.get_gene("rep_weighting"))
            y.append(a.score/len(a.transaction_list))

    x1 = []; x2 = []
    y1 = []; y2 = []
    for n in range(0,len(x)):
        if x[n] <= 512:
            x1.append(x[n])
            y1.append(y[n])
        else:
            x2.append(x[n])
            y2.append(y[n])

    plt.scatter(x1,y1,c="red")
    plt.scatter(x2,y2,c="blue")
    m1, c1, r1, p1, stderr1 = scipy.stats.linregress(x1,y1)
    m2, c2, r2, p2, stderr2 = scipy.stats.linregress(x2,y2)

    coerr1 = []
    for a in x1:
        coerr1.append(a * m1 + c1)

    coerr2 = []
    for a in x2:
        coerr2.append(a * m2 + c2)

    plt.plot(x1,coerr1,c="red")
    plt.plot(x2,coerr2,c="blue")

    print("X1 (R < 512), m = {}, c = {}, r = {}, p = {}".format(m1,c1,r1,p1))
    print("X2 (R > 512), m = {}, c = {}, r = {}, p = {}".format(m2,c2,r2,p2))

    plt.xlabel("R")
    plt.ylabel("Score per Transaction")
    plt.axis([0,1024,1,1.8])
    plt.title("Graph of R against average dove score per transaction")
    plt.show()
    return x, y

from Agents import *
import numpy as np
def hypothesis_1_2():
    PARAMETERS.N_AGENTS = 250
    PARAMETERS.TRANSACTIONS_PER_AGENT = 250
    PARAMETERS.INITIAL_HAWK = 200
    PARAMETERS.N_GENERATIONS = 1

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.random_int(1,1023)
    P = {"c" : lambda: RANDOMS.random_int(1,1023),
         "1" : lambda: RANDOMS.normal_random_int(300,150),
         "2" : lambda: RANDOMS.normal_random_int(500,150),
         "3" : lambda: RANDOMS.normal_random_int(700,150),
         }

    I = {}
    I["c"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["1"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["2"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["3"] = AgentList([None] * PARAMETERS.N_AGENTS)

    sims = {}

    stats = {}

    n_times =  50

    for k, v in I.items():
        stats[k] = {}
        stats[k]["dove_scores"] = {"mean" : [], "sd" : []}
        stats[k]["hawk_scores"] = {"mean" : [], "sd" : []}
        for i in range(0,n_times):
            for n in range(0,PARAMETERS.N_AGENTS):
                I[k][n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{"strategy" : strategy(), "prob_defect" : prob_defect(), "rep_weighting" : P[k](),}))
            sims[k] = Simulation.Simulation(agents=I[k])
            sims[k].run_simulation()

            x_d = []
            y_d = []
            y_h = []
            agents= sims[k].agent_list
            for a in agents:
                if StrategyGene.enum_to_str(a.get_gene("strategy")) == "D":
                    x_d.append(a.get_gene("rep_weighting"))
                    y_d.append(a.score/len(a.transaction_list))
                elif StrategyGene.enum_to_str(a.get_gene("strategy")) == "H":
                    y_h.append(a.score/len(a.transaction_list))


            #plt.scatter(x,y)
            #plt.show()
            stats[k]["dove_scores"]["mean"].append(np.mean(y_d))
            stats[k]["dove_scores"]["sd"].append(np.std(y_d))

            stats[k]["hawk_scores"]["mean"].append(np.mean(y_h))
            stats[k]["hawk_scores"]["sd"].append(np.std(y_h))

        print("---------\n\n")
        print("FOR TEST I_{}".format(k))
        print("MEAN HAWK SCORE = {}".format(np.mean(stats[k]["hawk_scores"]["mean"])))
        print("HAWK SCORE SD = {}".format(np.std(stats[k]["hawk_scores"]["mean"])))
        print("MEAN DOVE SCORE = {}".format(np.mean(stats[k]["dove_scores"]["mean"])))
        print("DOVE SCORE SD = {}".format(np.std(stats[k]["dove_scores"]["mean"])))

        print("---------\n\n")

    return stats

import Manager

def hypothesis_1_3(KEY_TO_DO=None):
    PARAMETERS.N_GENERATIONS = 50
    PARAMETERS.N_AGENTS = 100
    PARAMETERS.TRANSACTIONS_PER_AGENT = 100
    PARAMETERS.TOP_X = int(0.3 * PARAMETERS.N_AGENTS)
    PARAMETERS.VERBOSE_SIMULATIONS = False
    PARAMETERS.GARBAGE_COLLECTION = False

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.random_int(1,1023)
    P = {"c" : lambda: RANDOMS.random_int(1,1023),
         "1" : lambda: RANDOMS.normal_random_int(300,150),
         "2" : lambda: RANDOMS.normal_random_int(500,150),
         "3" : lambda: RANDOMS.normal_random_int(700,150),
         }

    I = {}
    I["c"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["1"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["2"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["3"] = AgentList([None] * PARAMETERS.N_AGENTS)

    stats = {}

    n_times = 50
    import gc
    for k, v in I.items():
        if KEY_TO_DO is not None and KEY_TO_DO != k:
            continue
        stats[k] = {}
        for time in range(0,n_times):
            print("\n\nRunning experiment I_{}, {} out of {} times.".format(k,time+1,n_times))
            print("-------------------------------------")
            mans = {}
            stats[k][time] = {}
            for n in range(0,PARAMETERS.N_AGENTS):
                I[k][n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{"strategy" : strategy(), "prob_defect" : prob_defect(), "rep_weighting" : P[k](),}))
            mans[k] = Manager.Manager()
            man_stats = mans[k].run(agent_list=I[k])

            stats[k][time]["x"] = []
            stats[k][time]["y"] = []

            for n in range(0,PARAMETERS.N_GENERATIONS):
                stats[k][time]["x"].append(n+1)
                stats[k][time]["y"].append(man_stats[n][1]/PARAMETERS.N_AGENTS)

            print(stats[k][time]["y"])

            #plt.scatter(stats[k][time]["x"],stats[k][time]["y"])
            #plt.xlabel("Generation")
            #plt.ylabel("Proportion of hawks")
            #plt.title("Graph of generation vs number of hawks, for I_{}".format(k))
            #plt.axis([0,50,0,1])
            #plt.show()

    return stats

import scipy.stats
def hypothesis_1_3_analysis(stats, boundary=0.2):
    new_stats = {}
    for k_main, v_main in stats.items():
        these_stats = []
        for k, v in v_main.items():
            val = 0
            for H in stats[k_main][k]["y"]:
                print(H)
                if H >= boundary:
                    val += 1
            these_stats.append(val)
            print("------------")
        new_stats[k_main] = these_stats

    print("H(I_3) < H(I_c) - p = {}".format(scipy.stats.ttest_ind(new_stats["c"],new_stats["3"],equal_var=False)))
    print("H(I_3) < H(I_1) - p = {}".format(scipy.stats.ttest_ind(new_stats["1"],new_stats["3"],equal_var=False)))
    print("H(I_3) < H(I_2) - p = {}".format(scipy.stats.ttest_ind(new_stats["2"],new_stats["3"],equal_var=False)))
    print("H(I_2) < H(I_1) - p = {}".format(scipy.stats.ttest_ind(new_stats["2"],new_stats["1"],equal_var=False)))
    return new_stats