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
        self.feedback = []

    def other_agent(self,agent):
        if self.agent_1 == agent:
            return self.agent_2
        elif self.agent_2 == agent:
            return self.agent_1
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
        a1f = Feedback.Feedback(ENUMS.FeedbackSource.transaction,self.agent_1.AUT_leave_feedback(self), source_transaction=self)
        a2f = Feedback.Feedback(ENUMS.FeedbackSource.transaction,self.agent_2.AUT_leave_feedback(self), source_transaction=self)

        self.agent_2.new_transaction(self,feedback_value=a1f)
        self.agent_1.new_transaction(self,feedback_value=a2f)

        self.transaction_state = ENUMS.TransactionState.completed

    def get_decision(self, agent):
        if (agent == self.agent_1):
            return self.decision_1
        elif (agent == self.agent_2):
            return self.decision_2
        raise ValueError


    def get_score(self, agent):
        a1 = agent
        a2 = self.other_agent(agent)

        a1d = self.get_decision(a1)
        a2d = self.get_decision(a2)

        if (a1d == ENUMS.TransactionDecision.decline or a2d == ENUMS.TransactionDecision.decline):
            return PARAMETERS.PAYOFF_DECL
        if (a1d == ENUMS.TransactionDecision.cooperate and a2d == ENUMS.TransactionDecision.cooperate):
            return PARAMETERS.PAYOFF_COOP
        elif (a1d == ENUMS.TransactionDecision.cooperate and a2d == ENUMS.TransactionDecision.defect):
            return PARAMETERS.PAYOFF_DAGA
        elif (a1d == ENUMS.TransactionDecision.defect and a2d == ENUMS.TransactionDecision.cooperate):
            return PARAMETERS.PAYOFF_DDON
        elif (a1d == ENUMS.TransactionDecision.defect and a2d == ENUMS.TransactionDecision.defect):
            return PARAMETERS.PAYOFF_DBOT

class TransactionList(collections.UserList):
    def __init__(self, list=[]):
        super(TransactionList,self).__init__(list)

    def get_score(self,agent):
        score = 0
        for t in self:
            score += t.get_score(agent)
        return score