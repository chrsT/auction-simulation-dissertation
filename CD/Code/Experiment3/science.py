#!/usr/bin/python3
import Simulation
import PARAMETERS, RANDOMS
from Genetics import StrategyGene
from Agents import AgentList, Agent
import Manager
import time

def log(text):
    print("[{}] {}".format(time.ctime(time.time()),text))

def hypothesis_3_1():
    PARAMETERS.N_AGENTS = 1000
    PARAMETERS.TRANSACTIONS_PER_AGENT = 2500
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = True

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,50)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,50)
    personal_experience = lambda: 0
    false_feedback = lambda: 0

    A = {"c" : lambda: RANDOMS.random_int(1,1023),
         }

    n_repeats = 10

    stats = {}

    for k in A.keys():
        log("Beginning test for k = {}\n-----------\n\n".format(k))
        stats[k] = []
        for n in range(0,n_repeats):
            log("Beginning test {} out of {} for k = {}".format(n+1,n_repeats,k))
            agent_list = AgentList([None] * PARAMETERS.N_AGENTS)
            for n in range(0,PARAMETERS.N_AGENTS):
                agent_list[n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{
                    "strategy" : strategy(),
                    "prob_defect" : prob_defect(),
                    "rep_weighting" : rep_weighting(),
                    "personal_experience" : personal_experience(),
                    "false_feedback" : false_feedback(),
                    "alturistic_punishment" : A[k]()
                }))
            sim = Simulation.Simulation(agents=agent_list)
            sim.run_simulation()
            stats[k].append(sim.agent_list.gene_score("alturistic_punishment"))

    return stats

import matplotlib.pyplot as plt
import scipy.stats
def hypothesis_3_1_plot(stats):
    x = []
    y = []
    for k, v in stats.items():
        for stat in v:
            for s in stat:
                x.append(int(s[1]))
                y.append(s[0])

    m1, c1, r1, p1, stderr1 = scipy.stats.linregress(x,y)
    plt.scatter(x,y)
    plt.plot([0, 1024], [c1, c1 + m1 * 1023],color="r")
    plt.title("Experiment 3.1")
    plt.ylabel("Average Dove Score Per Transaction (D)")
    plt.xlabel("Altruistic Punishment value (A)")
    plt.xlim([0,1024])
    plt.ylim([0,2])
    plt.show()

    print("m = {}, c = {}, r = {}, p = {}, stderr = {}".format(m1,c1,r1,p1,stderr1))

def hypothesis_3_2(KEY_TO_DO=None):
    PARAMETERS.N_AGENTS = 250
    PARAMETERS.TRANSACTIONS_PER_AGENT = 1000
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = True

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    personal_experience = lambda: 0
    false_feedback = lambda: 0 #RANDOMS.normal_random_int(500,150)

    I = {}
    I["c"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["1"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["2"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["3"] = AgentList([None] * PARAMETERS.N_AGENTS)
    #I["zero"] = AgentList([None] * PARAMETERS.N_AGENTS)
    #I["1023"] = AgentList([None] * PARAMETERS.N_AGENTS)

    A = {"c" : lambda: RANDOMS.random_int(1,1023),
         "1" : lambda: RANDOMS.normal_random_int(300,150),
         "2" : lambda: RANDOMS.normal_random_int(500,150),
         "3" : lambda: RANDOMS.normal_random_int(700,150)}


    stats = {}

    sims = {}

    n_times = 10

    for k, v in I.items():
        if KEY_TO_DO is not None and KEY_TO_DO != k:
            continue
        log("\n---\nBeginning test for k = {}\n".format(k))
        stats[k] = {}
        for which_time in range(0,n_times):
            log("Running k = {} ---  for time {} out of {}.".format(k,which_time+1,n_times))
            agent_list = AgentList([None] * PARAMETERS.N_AGENTS)
            for n in range(0,PARAMETERS.N_AGENTS):
                agent_list[n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{
                    "strategy" : strategy(),
                    "prob_defect" : prob_defect(),
                    "rep_weighting" : rep_weighting(),
                    "personal_experience" : personal_experience(),
                    "false_feedback" : false_feedback(),
                    "alturistic_punishment" : A[k]()
                }))
            sim = Simulation.Simulation(agents=agent_list)
            sim.run_simulation()
            #print("FOR KEY = {}".format(k))
            #sim.agent_list.breakdown()
            #print("-----\n\n")

            stats[k][which_time] = sim.agent_list.score_breakdown()

            #sims[k] = sim
    return stats

import numpy as np
def hypothesis_3_2_analysis(stats):
    stat_arrays = [
            "avg_dove_score",
            "avg_hawk_score",
            "avg_score" ,
            "avg_dove_sd",
            "avg_hawk_sd",
            "avg_score_sd",
    ]
    new_stats = {}
    stat_compilation = {}
    for k, v in stats.items():
        new_stats[k] = {}
        for stat in stat_arrays:
            new_stats[k][stat] = []
        for k_n, v_n in stats[k].items():
            for stat in stat_arrays:
                new_stats[k][stat].append(stats[k][k_n][stat])

    for k, v in new_stats.items():
        stat_compilation[k] = {}
        for stat in stat_arrays:
            stat_compilation[k][stat] = np.mean(new_stats[k][stat])

    print("k = c, mean = {}, sd = {}".format(np.mean(new_stats["c"]["avg_dove_score"]),np.std(new_stats["c"]["avg_dove_score"])))
    print("k = 1, mean = {}, sd = {}".format(np.mean(new_stats["1"]["avg_dove_score"]),np.std(new_stats["1"]["avg_dove_score"])))
    print("k = 2, mean = {}, sd = {}".format(np.mean(new_stats["2"]["avg_dove_score"]),np.std(new_stats["2"]["avg_dove_score"])))
    print("k = 3, mean = {}, sd = {}".format(np.mean(new_stats["3"]["avg_dove_score"]),np.std(new_stats["3"]["avg_dove_score"])))

    print("ANOVA: p = {}".format(scipy.stats.f_oneway(new_stats["3"]["avg_dove_score"],new_stats["2"]["avg_dove_score"],new_stats["1"]["avg_dove_score"],new_stats["c"]["avg_dove_score"])[1]))

    print("T-test: D(I_3) > D(I_c) - p = {}".format(scipy.stats.ttest_ind(new_stats["c"]["avg_dove_score"],new_stats["3"]["avg_dove_score"],equal_var=False)[1]))
    print("T-test: D(I_3) > D(I_1) - p = {}".format(scipy.stats.ttest_ind(new_stats["1"]["avg_dove_score"],new_stats["3"]["avg_dove_score"],equal_var=False)[1]))
    print("T-test: D(I_3) > D(I_2) - p = {}".format(scipy.stats.ttest_ind(new_stats["2"]["avg_dove_score"],new_stats["3"]["avg_dove_score"],equal_var=False)[1]))
    print("T-test: D(I_2) > D(I_1) - p = {}".format(scipy.stats.ttest_ind(new_stats["1"]["avg_dove_score"],new_stats["2"]["avg_dove_score"],equal_var=False)[1]))

    return new_stats, stat_compilation

def hypothesis_3_3(KEY_TO_DO=None):
    PARAMETERS.N_AGENTS = 250
    PARAMETERS.TRANSACTIONS_PER_AGENT = 1000
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = False
    PARAMETERS.N_GENERATIONS = 25
    PARAMETERS.TOP_X = int(PARAMETERS.N_AGENTS * 0.3)


    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    personal_experience = lambda: 0
    false_feedback = lambda: 0 #RANDOMS.normal_random_int(500,150)

    A = {"c" : lambda: RANDOMS.random_int(1,1023),
         "1" : lambda: RANDOMS.normal_random_int(300,150),
         "2" : lambda: RANDOMS.normal_random_int(500,150),
         "3" : lambda: RANDOMS.normal_random_int(700,150),
         #"zero" : lambda: 0,
         #"1023" : lambda: 1023,
         }

    I = {}
    I["c"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["1"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["2"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["3"] = AgentList([None] * PARAMETERS.N_AGENTS)

    stats = {}

    n_times = 3

    for k, v in I.items():
        if KEY_TO_DO is not None and KEY_TO_DO != k:
            continue
        log("\n---\nBeginning test for k = {}\n".format(k))
        stats[k] = {}
        for which_time in range(0,n_times):
            log("Running k = {} ---  for time {} out of {}.".format(k,which_time+1,n_times))
            agent_list = AgentList([None] * PARAMETERS.N_AGENTS)
            for n in range(0,PARAMETERS.N_AGENTS):
                agent_list[n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{
                    "strategy" : strategy(),
                    "prob_defect" : prob_defect(),
                    "rep_weighting" : rep_weighting(),
                    "personal_experience" : personal_experience(),
                    "false_feedback" : false_feedback(),
                    "alturistic_punishment" : A[k]()
                }))
            man = Manager.Manager()
            stats[k][which_time] = man.run_lean(agent_list=agent_list)
            #print("FOR KEY = {}".format(k))
            #sim.agent_list.breakdown()
            #print("-----\n\n")
    return stats

def hypothesis_3_3_analysis(stats):
    new_stats = {}
    for k, v in stats.items():
        new_stats[k] = {}
        new_stats[k]["strategy_breakdown"] = []
        for k_n, v_n in stats[k].items():
           new_stats[k]["strategy_breakdown"].append([])
           for n in range(0,len(stats[k][k_n]["strategy_breakdown"]),5):
               new_stats[k]["strategy_breakdown"][k_n].append(stats[k][k_n]["strategy_breakdown"][n])

        new_stats[k]["H"] = []
        new_stats[k]["Hawks"] = []
        for k_n, v_n in stats[k].items():
            new_stats[k]["Hawks"].append([])
            h_stat = 0
            for breakdown in new_stats[k]["strategy_breakdown"][k_n]:
                new_stats[k]["Hawks"][k_n].append(breakdown[1])
                if breakdown[1] > 20:
                    h_stat += 1
            new_stats[k]["H"].append(h_stat)



    return new_stats

def hypothesis_3_3_ttests(new_stats):
    for k, v in new_stats.items():
        print("k = {}, mean = {}, sd = {}".format(k,np.mean(new_stats[k]["H"]),np.std(new_stats[k]["H"])))

    print("ANOVA: p = {}".format(scipy.stats.f_oneway(new_stats["c"]["H"],new_stats["1"]["H"],new_stats["2"]["H"],new_stats["3"]["H"])))
    print("t-test H(I_3) < H(I_C): p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["H"],new_stats["c"]["H"],equal_var=False)))
    print("t-test H(I_3) < H(I_1): p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["H"],new_stats["1"]["H"],equal_var=False)))
    print("t-test H(I_3) < H(I_2): p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["H"],new_stats["2"]["H"],equal_var=False)))
    print("t-test H(I_2) < H(I_1): p = {}".format(scipy.stats.ttest_ind(new_stats["2"]["H"],new_stats["1"]["H"],equal_var=False)))
