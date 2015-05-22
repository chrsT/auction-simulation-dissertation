import ENUMS, RANDOMS, PARAMETERS
import Genetics, Transactions, Feedback
import collections
import numpy as np
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

    def gene_score(self, key):
        stats = []
        dove = True if key in ["rep_weighting","personal_experience"] else False
        for a in self:
            if a.get_gene("strategy") == ENUMS.StrategyEnum.dove and dove:
                stats.append((a.score/len(a.transaction_list),a.get_gene(key)))
            elif a.get_gene("strategy") == ENUMS.StrategyEnum.hawk and not dove:
                stats.append((a.score/len(a.transaction_list),a.get_gene(key)))
        return stats


    def breakdown(self):
        n_doves, n_hawks = self.strategy_breakdown()
        int_genes = self.gene_breakdown()
        scores = self.score_breakdown()
        print("---\nAgentList breakdown:")
        print("N_Agents: {}".format(len(self)))
        print("N_Doves: {}. N_Hawks: {}".format(n_doves,n_hawks))
        print("Average score (SD): {} ({}). For doves: {} ({}). For hawks: {} ({})".format(scores["avg_score"],scores["avg_score_sd"],scores["avg_dove_score"],scores["avg_dove_sd"],scores["avg_hawk_score"],scores["avg_hawk_sd"]))
        print("Int genes - [Gene Name]: [Average Relevant Value] ([Average All Value])")
        print("prob_defect: {} ({})".format(int_genes["prob_defect_hawk"],int_genes["prob_defect_all"]))
        print("rep_weighting: {} ({})".format(int_genes["rep_weighting_dove"],int_genes["rep_weighting_all"]))
        print("false_feedback: {} ({})".format(int_genes["false_feedback_hawk"],int_genes["false_feedback_all"]))
        print("personal_experience: {} ({})".format(int_genes["personal_experience_dove"],int_genes["personal_experience_all"]))
        print("---")

    def strategy_breakdown(self):
        n_doves = 0; n_hawks = 0
        for a in self:
            if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
                n_doves += 1
            elif a.get_gene("strategy") == ENUMS.StrategyEnum.hawk:
                n_hawks += 1
        return n_doves, n_hawks

    def score_breakdown(self):
        dove_scores = []; hawk_scores = []
        for a in self:
            if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
                dove_scores.append(a.score/len(a.transaction_list))
            elif a.get_gene("strategy") == ENUMS.StrategyEnum.hawk:
                hawk_scores.append(a.score/len(a.transaction_list))
        stats = {
            "avg_dove_score" : np.mean(dove_scores) if len(dove_scores) > 0 else 0,
            "avg_hawk_score" : np.mean(hawk_scores) if len(hawk_scores) > 0 else 0,
            "avg_score" : np.mean(dove_scores + hawk_scores),
            "avg_dove_sd" : np.std(dove_scores) if len(dove_scores) > 0 else 0,
            "avg_hawk_sd" : np.std(hawk_scores) if len(hawk_scores) > 0 else 0,
            "avg_score_sd" : np.std(dove_scores + hawk_scores)
        }
        return stats

    def gene_breakdown(self):
        n_doves = 0; n_hawks = 0
        stats = {
            "prob_defect_all" : 0,
            "prob_defect_hawk" : 0,
            "rep_weighting_all" : 0,
            "rep_weighting_dove" : 0,
            "false_feedback_all" : 0,
            "false_feedback_hawk" : 0,
            "personal_experience_all" : 0,
            "personal_experience_dove" : 0
        }
        for a in self:
            if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
                n_doves += 1
                stats["rep_weighting_dove"] += int(a.get_gene("rep_weighting"))
                stats["personal_experience_dove"] += int(a.get_gene("personal_experience"))
            elif a.get_gene("strategy") == ENUMS.StrategyEnum.hawk:
                n_hawks += 1
                stats["prob_defect_hawk"] += int(a.get_gene("prob_defect"))
                stats["false_feedback_hawk"] += int(a.get_gene("false_feedback"))
            stats["prob_defect_all"] += int(a.get_gene("prob_defect"))
            stats["rep_weighting_all"] += int(a.get_gene("rep_weighting"))
            stats["false_feedback_all"] += int(a.get_gene("false_feedback"))
            stats["personal_experience_all"] += int(a.get_gene("personal_experience"))

        stats["prob_defect_all"] /= (n_doves + n_hawks)
        stats["rep_weighting_all"] /= (n_doves + n_hawks)
        stats["false_feedback_all"] /= (n_doves + n_hawks)
        stats["personal_experience_all"] /= (n_doves + n_hawks)

        if n_doves > 0:
            stats["rep_weighting_dove"] /= n_doves
            stats["personal_experience_dove"] /= n_doves

        if n_hawks > 0:
            stats["prob_defect_hawk"] /= n_hawks
            stats["false_feedback_hawk"] /= n_hawks

        return stats



class Agent(object):
    CLASS_N_ID = 0

    @classmethod
    def CLASS_generate_random_agent(self):
        genome_dict = { "strategy" : RANDOMS.binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D"),
                        "prob_defect" : RANDOMS.random_int(1,1023),
                        "rep_weighting" : RANDOMS.random_int(1,1023),
                        "false_feedback" : RANDOMS.random_int(1,1023),
                        "personal_experience" : RANDOMS.random_int(1,1023)}
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
        self.transaction_table = {}
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

        other_id = transaction.other_agent(self).ID
        if self.transaction_table.get(other_id,None) is None:
            self.transaction_table[other_id] = [transaction]
        else:
            self.transaction_table[other_id].append(transaction)

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
        other_feedback = other_agent.feedback_list

        rep_weighting = int(self.get_gene("rep_weighting"))

        personal_experience = int(self.get_gene("personal_experience"))

        other_score = other_feedback.get_score()

        personal_score = self.get_personal_feedback(other_agent)

        if other_score[0] + other_score[1] == 0:
            return ENUMS.TransactionDecision.cooperate
        else:
            percent_reputation = (other_score[0] / (other_score[0] + other_score[1]))
            if (personal_score[0] + personal_score[1] == 0):
                percent = percent_reputation
            else:
                percent_personal = (personal_score[0] / (personal_score[0] + personal_score[1]))
                percent = (personal_experience/1024) * percent_personal + ((1024-personal_experience)/1024) * percent_reputation

            if (percent >= (rep_weighting/1024)):
                return ENUMS.TransactionDecision.cooperate
            else:
                return ENUMS.TransactionDecision.decline

    def get_personal_feedback(self,other_agent):
        score = (0, 0)
        for t in self.transaction_table.get(other_agent.ID,[]):
            f = t.other_agent_feedback(self)
            if f is None:
                continue
            if f.value == ENUMS.FeedbackValue.positive:
                score = (score[0]+1,score[1])
            elif f.value == ENUMS.FeedbackValue.negative:
                score = (score[0],score[1]+1)
        return score




    def AUT_leave_feedback(self,transaction):
        """
        :param transaction:
        :return: ENUMS.FeedbackValue
        """
        other_agent = transaction.other_agent(self)
        decision = transaction.get_decision(other_agent)
        my_decision = transaction.get_decision(self)


        #Doves are always honest
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
        score = self.feedback_list.get_score()
        prob_defect = int(self.get_gene("prob_defect"))

        if (score[0] + score[1]) < (10 - prob_defect/100) or (score[0] + score[1] == 0):
            return ENUMS.TransactionDecision.cooperate
        else:
            if (score[1] / (score[1] + score[0])) > (prob_defect/1024):
                return ENUMS.TransactionDecision.cooperate
            else:
                return ENUMS.TransactionDecision.defect

    def AUT_leave_feedback(self,transaction):
        """
        :param transaction:
        :return: ENUMS.FeedbackValue
        """
        other_agent = transaction.other_agent(self)
        decision = transaction.get_decision(other_agent)
        my_decision = transaction.get_decision(self)

        decieve = RANDOMS.binary_random_decision(int(self.get_gene("false_feedback")), True, False)
        #Hawks are not
        if decision == ENUMS.TransactionDecision.decline or my_decision == ENUMS.TransactionDecision.decline:
            feedback_val = 0
        elif decision == ENUMS.TransactionDecision.cooperate:
            feedback_val = ENUMS.FeedbackValue.positive
        elif decision == ENUMS.TransactionDecision.defect:
            feedback_val = ENUMS.FeedbackValue.negative
        else:
            raise ValueError

        if decieve:
            if feedback_val == ENUMS.FeedbackValue.positive:
                feedback_val = ENUMS.FeedbackValue.negative
            elif feedback_val == ENUMS.FeedbackValue.negative:
                feedback_val = ENUMS.FeedbackValue.positive

        return feedback_val
