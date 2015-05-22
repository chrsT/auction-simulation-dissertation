import ENUMS
# SIMULATION parameters
VERSION = "E00"
GENOME_STRING = "E00-{strategy}"
GENES = ["strategy"]
DEBUG = True

N_GENERATIONS = 10
N_AGENTS = 250
TRANSACTIONS_PER_AGENT = 250

# PAYOFF parameters
PAYOFF_COOP = 2 #Both Coop
PAYOFF_DAGA = -2 #Defected Against
PAYOFF_DDON = 4 #Defected success
PAYOFF_DBOT = -1 #Both defected
PAYOFF_DECL = 0 #Declined to participate

# GENETICS parameters
INITIAL_HAWK = 150
GENETICS_STRATEGY_HAWK_DOM = 100
GENETICS_STRATEGY_MUTATE = 75

#Breeding
BREEDING_METHOD = ENUMS.BreedingMethod.top_x
TOP_X = 30
Sliding = 0.02

#MANAGER parameters


