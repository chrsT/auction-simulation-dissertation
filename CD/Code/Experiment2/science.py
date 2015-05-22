#!/usr/bin/python3
import Simulation
import PARAMETERS, RANDOMS
from Genetics import StrategyGene
from Agents import AgentList, Agent
import Manager
import time

def log(text):
    print("[{}] {}".format(time.ctime(time.time()),text))

def hypothesis_2_1_informal_reexperiment():
    PARAMETERS.N_AGENTS = 250
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = False
    PARAMETERS.TOP_X = int(PARAMETERS.N_AGENTS * 0.3)

    t = 2500

    E = [lambda: 0, lambda: RANDOMS.random_int(1,1023)]

    n_repeats = 10

    stats = {}

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    false_feedback = lambda: RANDOMS.normal_random_int(700,150)

    e_n = 0
    for e in E:
        log("Beginning test for e = {}\n-----------\n\n".format(e_n))
        PARAMETERS.TRANSACTIONS_PER_AGENT = t
        stats[e_n] = []
        for n in range(0,n_repeats):
            log("Beginning test {} out of {} for e = {}".format(n+1,n_repeats,e_n))
            agent_list = AgentList([None] * PARAMETERS.N_AGENTS)
            for n in range(0,PARAMETERS.N_AGENTS):
                agent_list[n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{
                    "strategy" : strategy(),
                    "prob_defect" : prob_defect(),
                    "rep_weighting" : rep_weighting(),
                    "personal_experience" : e(),
                    "false_feedback" : false_feedback()
                }))
            sim = Simulation.Simulation(agents=agent_list)
            sim.run_simulation()
            stats[e_n].append(sim.agent_list.gene_score("personal_experience"))
        e_n += 1

    return stats

def hypothesis_2_1(KEYS_TO_DO=None):
    PARAMETERS.N_AGENTS = 250
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = False
    PARAMETERS.TOP_X = int(PARAMETERS.N_AGENTS * 0.3)


    T = [250, 625, 1250, 1875, 2500, 3750, 5000]

    n_repeats = 10

    stats = {}

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    personal_experience = lambda: RANDOMS.random_int(1,1023)
    false_feedback = lambda: RANDOMS.normal_random_int(700,150)

    for t in T:
        if KEYS_TO_DO is not None and t not in KEYS_TO_DO:
            continue
        log("Beginning test for t = {}\n-----------\n\n".format(t))
        PARAMETERS.TRANSACTIONS_PER_AGENT = t
        stats[t] = []
        for n in range(0,n_repeats):
            log("Beginning test {} out of {} for t = {}".format(n+1,n_repeats,t))
            agent_list = AgentList([None] * PARAMETERS.N_AGENTS)
            for n in range(0,PARAMETERS.N_AGENTS):
                agent_list[n] = Agent.CLASS_create_agent(genome_string=PARAMETERS.GENOME_STRING.format(**{
                    "strategy" : strategy(),
                    "prob_defect" : prob_defect(),
                    "rep_weighting" : rep_weighting(),
                    "personal_experience" : personal_experience(),
                    "false_feedback" : false_feedback()
                }))
            sim = Simulation.Simulation(agents=agent_list)
            sim.run_simulation()
            stats[t].append(sim.agent_list.gene_score("personal_experience"))

    return stats

def hypothesis_2_1_analysis(stats):
    new_stats = {}
    for k, v in stats.items():
        new_stats[k] = {}
        for n in range(0,len(stats[k])):
            new_stats[k][n] = {}
            new_stats[k][n]["x"] = [int(a[1]) for a in stats[k][n]]
            new_stats[k][n]["y"] = [a[0] for a in stats[k][n]]

    return new_stats

import matplotlib.pyplot as plt
import scipy.stats
def hypothesis_2_1_plot(new_stats_k, k=0,SHOW_GRAPH=True):
    x = []
    y = []
    for l,lst in new_stats_k.items():
        x.append([])
        y.append([])
        x[l] += lst["x"]
        y[l] += lst["y"]


    if SHOW_GRAPH:
        plt.title("Experiment 2.1, T:N = {}".format(k/250.0))
        plt.ylabel("Score per transaction (S)")
        plt.xlabel("E")
        for n in range(0,len(x)):
            plt.scatter(x[n],y[n])
        plt.show()
        plt.ylim([0,2])
        plt.xlim([0,1024])

    means = []
    sds = []
    outliers = []

    for n in range(0,len(x)):
        mean = np.mean(y[n])
        means.append(mean)
        sd = np.std(y[n])
        sds.append(sd)
        outlier = 0
        for score in y[n]:
            if score < 1:
                outlier += 1
        outliers.append(outlier)
    #m, c, r, p, stderr = scipy.stats.linregress(x[n],y[n])
    print("----------------")
    print("k = {}".format(k))
    #print("m = {}, c = {}, r = {}, p = {}, stderr = {}".format(m,c,r,p,stderr))
    print("mean = {} (SD: {}), mean sd = {}, outliers = {} (SD: {})".format(np.mean(means),np.std(means),np.mean(sds),np.mean(outliers),np.std(outliers)))
    print("----------------\n")




def hypothesis_2_2(KEY_TO_DO=None):
    PARAMETERS.N_AGENTS = 250
    PARAMETERS.TRANSACTIONS_PER_AGENT = 2500
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = False

    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    personal_experience = lambda: RANDOMS.normal_random_int(500,150)

    F = {"c" : lambda: RANDOMS.random_int(1,1023),
         "1" : lambda: RANDOMS.normal_random_int(300,150),
         "2" : lambda: RANDOMS.normal_random_int(500,150),
         "3" : lambda: RANDOMS.normal_random_int(700,150),
         "zero" : lambda: 0,
         "1023" : lambda: 1023,
         }

    I = {}
    I["c"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["1"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["2"] = AgentList([None] * PARAMETERS.N_AGENTS)
    I["3"] = AgentList([None] * PARAMETERS.N_AGENTS)
    #I["zero"] = AgentList([None] * PARAMETERS.N_AGENTS)
    #I["1023"] = AgentList([None] * PARAMETERS.N_AGENTS)


    stats = {}

    sims = {}

    n_times = 50

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
                    "false_feedback" : F[k]()
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
import scipy.stats
def hypothesis_2_2_analysis(stats):
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

    print("T-test: D(I_3) < D(I_c) - p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["avg_dove_score"],new_stats["c"]["avg_dove_score"],equal_var=False)[1]))
    print("T-test: D(I_3) < D(I_1) - p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["avg_dove_score"],new_stats["1"]["avg_dove_score"],equal_var=False)[1]))
    print("T-test: D(I_3) < D(I_2) - p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["avg_dove_score"],new_stats["2"]["avg_dove_score"],equal_var=False)[1]))
    print("T-test: D(I_2) < D(I_1) - p = {}".format(scipy.stats.ttest_ind(new_stats["2"]["avg_dove_score"],new_stats["1"]["avg_dove_score"],equal_var=False)[1]))

    return new_stats, stat_compilation

def hypothesis_2_3(KEY_TO_DO=None):
    PARAMETERS.N_AGENTS = 100
    PARAMETERS.TRANSACTIONS_PER_AGENT = 1000
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = False
    PARAMETERS.N_GENERATIONS = 25
    PARAMETERS.TOP_X = int(PARAMETERS.N_AGENTS * 0.3)


    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    personal_experience = lambda: RANDOMS.normal_random_int(500,150)

    F = {"c" : lambda: RANDOMS.random_int(1,1023),
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

    n_times = 25

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
                    "false_feedback" : F[k]()
                }))
            man = Manager.Manager()
            stats[k][which_time] = man.run_lean(agent_list=agent_list)
            #print("FOR KEY = {}".format(k))
            #sim.agent_list.breakdown()
            #print("-----\n\n")

    return stats

def hypothesis_2_3_informal(KEY_TO_DO=None):
    PARAMETERS.N_AGENTS = 100
    PARAMETERS.TRANSACTIONS_PER_AGENT = 1000
    PARAMETERS.INITIAL_HAWK = 400
    PARAMETERS.VERBOSE_SIMULATIONS = False
    PARAMETERS.N_GENERATIONS = 100
    PARAMETERS.TOP_X = int(PARAMETERS.N_AGENTS * 0.3)


    strategy = lambda: RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")
    prob_defect = lambda: RANDOMS.normal_random_int(300,150)
    rep_weighting = lambda: RANDOMS.normal_random_int(500,150)
    personal_experience = lambda: RANDOMS.normal_random_int(500,150)

    F = {"c" : lambda: RANDOMS.random_int(1,1023),
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
                    "false_feedback" : F[k]()
                }))
            man = Manager.Manager()
            stats[k][which_time] = man.run_lean(agent_list=agent_list)
            #print("FOR KEY = {}".format(k))
            #sim.agent_list.breakdown()
            #print("-----\n\n")

    return stats

def hypothesis_2_3_analysis(stats):
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

def hypothesis_2_3_ttests(new_stats):
    for k, v in new_stats.items():
        print("k = {}, mean = {}, sd = {}".format(k,np.mean(new_stats[k]["H"]),np.std(new_stats[k]["H"])))

    print("ANOVA: p = {}".format(scipy.stats.f_oneway(new_stats["c"]["H"],new_stats["1"]["H"],new_stats["2"]["H"],new_stats["3"]["H"])))
    print("t-test H(I_3) < H(I_C): p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["H"],new_stats["c"]["H"],equal_var=False)))
    print("t-test H(I_3) < H(I_1): p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["H"],new_stats["1"]["H"],equal_var=False)))
    print("t-test H(I_3) < H(I_2): p = {}".format(scipy.stats.ttest_ind(new_stats["3"]["H"],new_stats["2"]["H"],equal_var=False)))
    print("t-test H(I_2) < H(I_1): p = {}".format(scipy.stats.ttest_ind(new_stats["2"]["H"],new_stats["1"]["H"],equal_var=False)))

def hypothesis_2_3_plot(new_stats,title="",x_axis="",y_axis=""):
    colours = ["b","g","r","c","m","y","k"]
    for stat in new_stats:
        x = []
        y = []
        for n in range(0,len(stat)):
            x.append(n)
            y.append(stat[n])
        colour = colours[0]
        colours = colours[1:]
        plt.scatter(x,y,c=colour)
    plt.title = title
    plt.xlabel = x_axis
    plt.ylabel = y_axis

    plt.show()


