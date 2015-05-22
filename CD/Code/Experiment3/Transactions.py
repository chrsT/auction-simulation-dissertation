import ENUMS, RANDOMS, PARAMETERS
import Feedback, Agents, Genetics
import collections

class Transaction(object):
    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.decision_1 = None
        self.decision_2 = None
        self.transaction_state = ENUMS.TransactionState.initialised

        self.feedback_for_agent_1 = []
        self.feedback_for_agent_2 = []

        self.chose_to_punish_1 = False
        self.chose_to_punish_2 = False


    def other_agent(self,agent):
        if self.agent_1 == agent:
            return self.agent_2
        elif self.agent_2 == agent:
            return self.agent_1
        else:
            raise ValueError

    def other_agent_feedback(self,agent):
        #Returns the feedback they GAVE to other agent.
        if self.agent_1 == agent:
            return self.feedback_for_agent_2
        elif self.agent_2 == agent:
            return self.feedback_for_agent_1
        else:
            raise ValueError

    def execute_transaction(self):
        if self.transaction_state != ENUMS.TransactionState.initialised:
            raise ValueError
        self.decision_1 = self.agent_1.AUT_transaction_decision(self.agent_2)
        self.decision_2 = self.agent_2.AUT_transaction_decision(self.agent_1)
        self.transaction_state = ENUMS.TransactionState.executed

        if self.decision_1 == ENUMS.TransactionDecision.decline or self.decision_2 == ENUMS.TransactionDecision.decline:
            self.agent_1.new_transaction(self)
            self.agent_2.new_transaction(self)
            self.transaction_state = ENUMS.TransactionState.completed
        else:
            self.transaction_state = ENUMS.TransactionState.feedback
            self.execute_feedback()

    def execute_feedback(self):
        if self.transaction_state != ENUMS.TransactionState.feedback:
            raise ValueError
        self.feedback_for_agent_2 = [Feedback.Feedback(ENUMS.FeedbackSource.transaction,self.agent_1.AUT_leave_feedback(self), source_transaction=self)]
        self.feedback_for_agent_1 = [Feedback.Feedback(ENUMS.FeedbackSource.transaction,self.agent_2.AUT_leave_feedback(self), source_transaction=self)]

        if self.decision_2 == ENUMS.TransactionDecision.defect and self.agent_1.AUT_alturistic_punishment():
            self.feedback_for_agent_2.append(Feedback.Feedback(ENUMS.FeedbackSource.punishment,ENUMS.FeedbackValue.punishment, source_transaction=self))
            self.chose_to_punish_1 = True

        if self.decision_1 == ENUMS.TransactionDecision.defect and self.agent_2.AUT_alturistic_punishment():
            self.feedback_for_agent_1.append(Feedback.Feedback(ENUMS.FeedbackSource.punishment,ENUMS.FeedbackValue.punishment, source_transaction=self))
            self.chose_to_punish_2 = True



        self.agent_2.new_transaction(self,feedback_value=self.feedback_for_agent_2)
        self.agent_1.new_transaction(self,feedback_value=self.feedback_for_agent_1)

        self.transaction_state = ENUMS.TransactionState.completed

    def get_decision(self, agent):
        if (agent == self.agent_1):
            return self.decision_1
        elif (agent == self.agent_2):
            return self.decision_2
        raise ValueError

    def get_punishment(self,agent):
        if self.agent_1 == agent:
            return self.chose_to_punish_1
        elif self.agent_2 == agent:
            return self.chose_to_punish_2
        else:
            raise ValueError

    def get_score(self, agent):
        a1 = agent
        a2 = self.other_agent(agent)

        a1d = self.get_decision(a1)
        a2d = self.get_decision(a2)

        value = 0
        if (a1d == ENUMS.TransactionDecision.decline or a2d == ENUMS.TransactionDecision.decline):
            value = PARAMETERS.PAYOFF_DECL
        if (a1d == ENUMS.TransactionDecision.cooperate and a2d == ENUMS.TransactionDecision.cooperate):
            value = PARAMETERS.PAYOFF_COOP
        elif (a1d == ENUMS.TransactionDecision.cooperate and a2d == ENUMS.TransactionDecision.defect):
            value = PARAMETERS.PAYOFF_DAGA
        elif (a1d == ENUMS.TransactionDecision.defect and a2d == ENUMS.TransactionDecision.cooperate):
            value = PARAMETERS.PAYOFF_DDON
        elif (a1d == ENUMS.TransactionDecision.defect and a2d == ENUMS.TransactionDecision.defect):
            value =  PARAMETERS.PAYOFF_DBOT

        if self.get_punishment(a1):
            value += PARAMETERS.FEEDBACK_PUNISHMENT_COST
        return value

class TransactionList(collections.UserList):
    def __init__(self, list=[]):
        super(TransactionList,self).__init__(list)
        self.score = 0
        self.evaluated = 0

    def get_score(self,agent):
        if len(self) == self.evaluated:
            return self.score
        to_check = len(self) - self.evaluated
        for t in self[self.evaluated:]:
            self.score += t.get_score(agent)
        self.evaluated = len(self)
        return self.score

    def get_score_breakdown(self,agent):
        ret = {"total" : self.get_score(agent)}

        for t in self:
            ret[t.get_score(agent)] = ret.get(t.get_score(agent),0) + 1

        return ret