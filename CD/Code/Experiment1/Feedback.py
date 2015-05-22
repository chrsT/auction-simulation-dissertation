#!/usr/bin/python3
import ENUMS

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
        self.evaluated = len(self)
        return self.score

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