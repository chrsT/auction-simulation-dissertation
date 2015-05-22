from enum import Enum

class TransactionDecision(Enum):
	cooperate = 1
	defect = 2
	decline = 3

class StrategyEnum(Enum):
	dove = 1
	hawk = 2

class GeneTypeEnum(Enum):
    distinct = 1
    int = 2

class TransactionState(Enum):
	initialised = 1
	executed = 2
	feedback = 3
	completed = 4

class FeedbackSource(Enum):
    transaction = 1

class FeedbackValue(Enum):
	positive = 1
	negative = 2

class SimulationState(Enum):
    initialised = 1
    executed = 2
    bred = 3

class BreedingMethod(Enum):
    top_x = 1
    sliding = 2