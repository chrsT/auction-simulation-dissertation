import PARAMETERS, RANDOMS, ENUMS
import Agents, Transactions
import time

class Simulation(object):
    def __init__(self,agents=None):
        self.simulation_state = ENUMS.SimulationState.initialised
        self.agent_list = Agents.AgentList()
        self.transaction_list = Transactions.TransactionList()
        if agents is None:
            self.agent_list = self.generate_random_agents(PARAMETERS.N_AGENTS)
        else:
            self.agent_list = agents
        #self.agent_list.breakdown()

    def run_simulation(self):
        if not self.simulation_state == ENUMS.SimulationState.initialised:
            raise ValueError
        n_transactions = PARAMETERS.N_AGENTS * PARAMETERS.TRANSACTIONS_PER_AGENT
        for roun in range(0,n_transactions):
            if (roun % (n_transactions/10) == 0 and PARAMETERS.VERBOSE_SIMULATIONS):
                print("[{}] - ROUND {} of {}".format(time.ctime(time.time()),roun,n_transactions))
            a1, a2 = self.agent_list.get_two_random()
            transaction = Transactions.Transaction(a1,a2)
            transaction.execute_transaction()
            self.transaction_list.append(transaction)
        self.simulation_state = ENUMS.SimulationState.executed

    def order_by_score(self):
        if self.simulation_state == ENUMS.SimulationState.initialised:
            raise ValueError
        l =  Agents.AgentList(list=sorted(self.agent_list,key=lambda agent: agent.score,reverse=True))
        return l

    def print_leaderboard(self):
        if self.simulation_state == ENUMS.SimulationState.initialised:
            raise ValueError
        ordered = self.order_by_score()
        for o in ordered:
            print("ID: {}. Genome: {}. Score {}. Feedback: {}.".format(o.ID,o.genome,o.score,o.get_feedback()))

    def breed(self):
        if not self.simulation_state == ENUMS.SimulationState.executed:
            raise ValueError
        new_agents = Agents.AgentList()
        breeding_pool = self.get_breeding_pool()
        if PARAMETERS.VERBOSE_SIMULATIONS:
            print("Breeding pool")
            breeding_pool.breakdown()
        for n in range(0,PARAMETERS.N_AGENTS):
            if PARAMETERS.BREEDING_METHOD == ENUMS.BreedingMethod.top_x:
                a1, a2 = breeding_pool.get_two_random()
                new_agents.append(a1.CLASS_breed(a1,a2))
        return new_agents

    def get_breeding_pool(self):
        if PARAMETERS.BREEDING_METHOD == ENUMS.BreedingMethod.top_x:
            return Agents.AgentList(self.order_by_score()[:PARAMETERS.TOP_X])


    def generate_random_agents(self,n_agents):
        a = Agents.AgentList()
        for n in range(0,n_agents):
            a.append(Agents.Agent.CLASS_generate_random_agent())
        return a