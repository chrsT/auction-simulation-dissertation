import ENUMS
# SIMULATION parameters
VERSION = "E02"
GENOME_STRING = "E02-{strategy}-{rep_weighting}-{prob_defect}-{false_feedback}-{personal_experience}"
GENES = ["strategy", "rep_weighting", "prob_defect", "false_feedback","personal_experience"]
DEBUG = True
VERBOSE_SIMULATIONS = False
GARBAGE_COLLECTION = False
MANAGER_FULL_COLLECT = False

N_GENERATIONS = 1
N_AGENTS = 10
TRANSACTIONS_PER_AGENT = 100

# PAYOFF parameters
PAYOFF_COOP = 2 #Both Coop
PAYOFF_DAGA = -2 #Defected Against
PAYOFF_DDON = 4 #Defected success
PAYOFF_DBOT = -1 #Both defected
PAYOFF_DECL = 0 #Declined to participate

# GENETICS parameters
INITIAL_HAWK = 100
GENETICS_STRATEGY_HAWK_DOM = 100
GENETICS_STRATEGY_MUTATE = 75

GENETICS_REP_WEIGHTING_MUTATE_FLIP = [2, 4, 8, 16, 32, 64, 128, 256, 512]
GENETICS_REP_WEIGHTING_MUTATE_ADD = (-64, 64)

GENETICS_PROB_DEFECT_MUTATE_FLIP = [2, 4, 8, 16, 32, 64, 128, 256, 512]
GENETICS_PROB_DEFECT_MUTATE_ADD = (-64, 64)

GENETICS_FALSE_FEEDBACK_MUTATE_FLIP = [2, 4, 8, 16, 32, 64, 128, 256, 512]
GENETICS_FALSE_FEEDBACK_MUTATE_ADD = (-64, 64)

GENETICS_PERSONAL_EXPERIENCE_MUTATE_FLIP = [2, 4, 8, 16, 32, 64, 128, 256, 512]
GENETICS_PERSONAL_EXPERIENCE_MUTATE_ADD = (-64, 64)

#Breeding
BREEDING_METHOD = ENUMS.BreedingMethod.top_x

#MANAGER parameters


