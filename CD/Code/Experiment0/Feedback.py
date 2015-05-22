#!/usr/bin/python3
import ENUMS

class FeedbackList(list):
    def __init__(self):
        super(FeedbackList,self).__init__(self)

    def get_score(self):
        score = (0,0)
        for t in self:
            if t.source == ENUMS.FeedbackSource.transaction:
                score = t.get_score(score=score)
        return score

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