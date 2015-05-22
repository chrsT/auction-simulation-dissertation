#!/usr/bin/python3
import ENUMS, PARAMETERS

class FeedbackList(list):
    def __init__(self):
        super(FeedbackList,self).__init__(self)
        self.score = (0, 0)
        self.evaluated = 0

    def get_score(self):
        if self.evaluated == len(self):
            return self.score
        for t in self[self.evaluated:]:
            if t.source == ENUMS.FeedbackSource.transaction:
                self.score = t.get_score(score=self.score)
            elif t.source == ENUMS.FeedbackSource.punishment:
                self.score = t.get_score(score=self.score)
        self.evaluated = len(self)
        return self.score

    def get_each_class(self):
        p = 0; n = 0; pun = 0;
        for t in self:
            if t.source == ENUMS.FeedbackSource.transaction:
                if t.value == ENUMS.FeedbackValue.positive:
                    p += 1
                elif t.value == ENUMS.FeedbackValue.negative:
                    n += 1
            elif t.source == ENUMS.FeedbackSource.punishment:
                pun += 1
        return p, n, pun

class Feedback(object):
    def __init__(self, source, value, source_transaction=None):
        self.source = source #ENUMS.FeedbackSource
        self.value = value #ENUMS.FeedbackValue
        self.source_transaction = source_transaction #Transaction

    def get_score(self,score=(0,0)):
        if self.source == ENUMS.FeedbackSource.transaction:
            if self.value == ENUMS.FeedbackValue.positive:
                return (score[0]+1,score[1])
            elif self.value == ENUMS.FeedbackValue.negative:
                return (score[0],score[1]+1)
        elif self.source == ENUMS.FeedbackSource.punishment:
            return (score[0], score[1]+PARAMETERS.FEEDBACK_PUNISHMENT)