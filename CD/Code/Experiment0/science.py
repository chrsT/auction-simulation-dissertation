#!/usr/bin/python3
import PARAMETERS, Manager, ENUMS

def hypothesis_0_2():
        PARAMETERS.N_AGENTS = 250
        PARAMETERS.TOP_X = 30
        PARAMETERS.INITIAL_HAWK = 50
        PARAMETERS.N_GENERATIONS = 5
        D_M_TUPLES = [
            (0.1,0.05),
            (0.3,0.05),
            (0.7,0.05),
            (0.1,0.4),
            (0.7,0.4),
        ]
        pair_n = 0
        n_sims = 10
        results = {}
        for pair in D_M_TUPLES:
            results[pair_n] = {}
            PARAMETERS.GENETICS_STRATEGY_HAWK_DOM = pair[0] * 1000
            PARAMETERS.GENETICS_STRATEGY_MUTATE = pair[1] * 1000
            print("##############***************")
            print("Setting D,M parameters to {}".format(pair))
            print("**************###############")
            print()
            for i in range(0,n_sims):
                print("Simulation {} of {}".format(i+1,n_sims))
                man = Manager.Manager()
                sim = man.run()
                n = []
                for s in sim:
                    n_doves,n_hawks = s.agent_list.get_n_strategy()
                    n.append((n_doves,n_hawks))
                results[pair_n][i] = n
            print(results[pair_n])
            pair_n += 1
            print()
            print()
        print()
        print()
        print()
        print("FINAL RESULTS")
        print(results)
        return results

def hypothesis_0_3():
    n_times = 50
    tests = []
    for N in [10,25,50,100,250]:
        for T in [10,25,50,100,250]:
            tests.append((N,T))

    PARAMETERS.BREEDING_METHOD = ENUMS.BreedingMethod.top_x
    PARAMETERS.INITIAL_HAWK = 100
    PARAMETERS.GENETICS_STRATEGY_HAWK_DOM = 300
    GENETICS_STRATEGY_MUTATE = 50
    results = {}
    for t in tests:
        key = "N{}-T{}".format(t[0],t[1])
        results[key] = {"avg_dove" : [], "avg_hawk" : [], "per_hawk" : []}
        print("Test for t = {}".format(t))
        print()
        PARAMETERS.N_AGENTS = t[0]
        PARAMETERS.TRANSACTIONS_PER_AGENT = t[1]
        PARAMETERS.N_GENERATIONS = 2
        PARAMETERS.TOP_X = round(PARAMETERS.N_AGENTS * 0.3)


        for n in range(0,n_times):
            print("Test {} of {}".format(n+1,n_times))
            man = Manager.Manager()
            sim = man.run()
            n_doves,n_hawks = sim[-1].agent_list.get_n_strategy()
            results[key]["per_hawk"].append((n_doves,n_hawks))
            dove_score,hawk_score = sim[-1].agent_list.avg_scores()
            results[key]["avg_dove"].append(dove_score/t[1]/2)
            results[key]["avg_hawk"].append(hawk_score/t[1]/2)
        print(results[key])
    return results

import pickle
import numpy as np
import matplotlib.pyplot as plt

def h_0_3_analysis(data):
    tests = []
    for N in [10,25,50,100,250]:
        for T in [10,25,50,100,250]:
            tests.append((N,T))

    stats = {"avg_dove_iqr" : {},
                 "avg_hawk_iqr" : {},
                 "per_hawk_iqr" : {},
                 "avg_dove_sd" : {},
                 "avg_hawk_sd" : {},
                 "per_hawk_sd" : {},
                 }
    print("TEST\t\tAvg_dove SD\t\tAvg_hawk SD\t\tPer_hawk SD")
    for t in tests:
        key = "N{}-T{}".format(t[0],t[1])
        data[key]["per_hawk_adj"] = []
        for a in data[key]["per_hawk"]:
            d = a[0]
            h = a[1]

            percent = h/(h+d) * 100.0

            data[key]["per_hawk_adj"].append(percent)

        avg_dove_q1, avg_dove_q3 = np.percentile(data[key]["avg_dove"],[75,25])
        avg_dove_iqr = round(avg_dove_q1 - avg_dove_q3,3)
        avg_dove_sd = round(np.std(data[key]["avg_dove"]),3)

        avg_hawk_q1, avg_hawk_q3 = np.percentile(data[key]["avg_hawk"],[75,25])
        avg_hawk_iqr = round(avg_hawk_q1 - avg_hawk_q3,3)
        avg_hawk_sd = round(np.std(data[key]["avg_hawk"]),3)

        per_hawk_q1, per_hawk_q3 = np.percentile(data[key]["per_hawk_adj"],[75,25])
        per_hawk_iqr = round(per_hawk_q1 - per_hawk_q3,3)
        per_hawk_sd = round(np.std(data[key]["per_hawk_adj"]),3)

        print("{}  \t{}\t\t\t{}\t\t\t{}".format(key,avg_dove_sd,avg_hawk_sd,per_hawk_sd))

        stats["avg_dove_iqr"][key] = avg_dove_iqr
        stats["avg_hawk_iqr"][key] = avg_hawk_iqr
        stats["per_hawk_iqr"][key] = per_hawk_iqr

        stats["avg_dove_sd"][key] = avg_dove_sd
        stats["avg_hawk_sd"][key] = avg_hawk_sd
        stats["per_hawk_sd"][key] = per_hawk_sd

    return stats

import math
import scipy.stats
def plot(data,title="thing",y_label="blahhh"):
    x = []
    y = []
    for k, v in data.items():
        print(k)
        print(v)
        strk = k.split("-")
        n = float(strk[0][1:])
        t = float(strk[1][1:])
        x.append(math.log10(n*t))
        y.append(v)

    m, c, r, p, stderr = scipy.stats.linregress(x,y)

    coerr = []
    for a in x:
        coerr.append(a * m + c)
    plt.scatter(x,y)
    print(coerr)
    plt.plot(x, coerr, "r")
    plt.xlabel("log(N * T)")
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def plot_one(data,n=0,t=0,title="thing"):
    new_data = {}
    for k, v in data.items():
        strk = k.split("-")
        nk = float(strk[0][1:])
        tk = float(strk[1][1:])
        if nk == n or tk == t:
            new_data[k] = v

    return plot(new_data,title=title)

