import ENUMS, RANDOMS, PARAMETERS
import Genetics, Transactions, Feedback
import collections
class AgentList(collections.UserList):
    def __init__(self, list=[]):
        super(AgentList,self).__init__(list)

    def get_two_random(self):
        n = len(self)
        if n < 2:
            raise
        n1 = RANDOMS.random_int(0,n-1)
        n2 = RANDOMS.random_int(0,n-1)
        while n1 == n2:
            n2 = RANDOMS.random_int(0,n-1)
        return self[n1],self[n2]

    def breakdown(self):
        n_doves, n_hawks = self.get_n_strategy()
        print("---\nAgentList breakdown:")
        print("N_Agents: {}".format(len(self)))
        print("N_Doves: {}. N_Hawks: {}".format(n_doves,n_hawks))
        print("---")

    def get_n_strategy(self):
        n_doves = 0
        n_hawks = 0
        for a in self:
            if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
                n_doves += 1
            elif a.get_gene("strategy") == ENUMS.StrategyEnum.hawk:
                n_hawks += 1
        return n_doves, n_hawks

    def avg_scores(self):
        n_doves, n_hawks = self.get_n_strategy()
        if n_doves == 0:
            n_doves = 1
        if n_hawks == 0:
            n_hawks = 1
        dove_score = 0
        hawk_score = 0
        for a in self:
            if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
                dove_score += a.score
            elif a.get_gene("strategy") == ENUMS.StrategyEnum.hawk:
                hawk_score += a.score

        return dove_score/n_doves,hawk_score/n_hawks

class Agent(object):
    CLASS_N_ID = 0

    @classmethod
    def CLASS_generate_random_agent(self):
        genome_dict = { "strategy" : RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D")}
        genome_str = PARAMETERS.GENOME_STRING.format(**genome_dict)
        agent = Agent.CLASS_create_agent(genome_str)
        return agent

    @classmethod
    def CLASS_create_agent(self,genome_string):
        genome = Genetics.Genome(genome_string)
        strategy = genome.get("strategy")
        if strategy.value == ENUMS.StrategyEnum.dove:
            agent = DoveAgent(genome)
        elif strategy.value == ENUMS.StrategyEnum.hawk:
            agent = HawkAgent(genome)
        else:
            raise ValueError(strategy)

        return agent

    @classmethod
    def CLASS_breed(self,agent1,agent2):
        return self.CLASS_create_agent(Genetics.Genome.CLASS_breed(agent1.genome,agent2.genome))

    @property
    def score(self):
        return self.get_score()

    @property
    def feedback(self):
        return self.get_feedback()

    def __init__(self, genome):
        self.genome = genome
        self.ID = self.CLASS_N_ID
        Agent.CLASS_N_ID += 1

        self.transaction_list = Transactions.TransactionList()
        self.feedback_list = Feedback.FeedbackList()

    def AUT_transaction_decision(self, other_agent):
        """
        :param other_agent:
        :return: ENUMS.TransactionDecision
        """
        raise NotImplementedError

    def AUT_leave_feedback(self,transaction):
        """
        :param transaction:
        :return: ENUMS.FeedbackValue
        """
        raise NotImplementedError

    def get_feedback(self):
        """
        :return: Tuple (positive,negative) feedback value
        """
        return self.feedback_list.get_score()

    def get_gene(self,key):
        return self.genome.get(key).get_value()

    def new_transaction(self, transaction, feedback_value=None):
        self.transaction_list.append(transaction)
        if feedback_value is not None:
            self.feedback_list.append(feedback_value)

    def get_score(self):
        return self.transaction_list.get_score(self)

class DoveAgent(Agent):
    def __init__(self, genome):
        super(DoveAgent,self).__init__(genome)

    def AUT_transaction_decision(self, other_agent):
        """
        :param other_agent:
        :return: ENUMS.TransactionDecision
        """
        return ENUMS.TransactionDecision.cooperate

    def AUT_leave_feedback(self,transaction):
        """
        :param transaction:
        :return: ENUMS.FeedbackValue
        """
        other_agent = transaction.other_agent(self)
        decision = transaction.get_decision(other_agent)
        my_decision = transaction.get_decision(self)

        if decision == ENUMS.TransactionDecision.decline or my_decision == ENUMS.TransactionDecision.decline:
            return 0
        elif decision == ENUMS.TransactionDecision.cooperate:
            return ENUMS.FeedbackValue.positive
        elif decision == ENUMS.TransactionDecision.defect:
            return ENUMS.FeedbackValue.negative
        else:
            raise ValueError

class HawkAgent(Agent):
    def __init__(self, genome):
        super(HawkAgent,self).__init__(genome)

    def AUT_transaction_decision(self, other_agent):
        """
        :param other_agent:
        :return: ENUMS.TransactionDecision
        """
        return ENUMS.TransactionDecision.defect

    def AUT_leave_feedback(self,transaction):
        """
        :param transaction:
        :return: ENUMS.FeedbackValue
        """
        other_agent = transaction.other_agent(self)
        decision = transaction.get_decision(other_agent)
        my_decision = transaction.get_decision(self)

        if decision == ENUMS.TransactionDecision.decline or my_decision == ENUMS.TransactionDecision.decline:
            return 0
        elif decision == ENUMS.TransactionDecision.cooperate:
            return ENUMS.FeedbackValue.positive
        elif decision == ENUMS.TransactionDecision.defect:
            return ENUMS.FeedbackValue.negative
        else:
            raise ValueError