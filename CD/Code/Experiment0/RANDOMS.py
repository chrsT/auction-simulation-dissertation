''' Auction Simulation Version V10 '''
import random

def binary_random_decision(threshold,below,above):
    # below, above inclusive
	random.seed()
	n = random.randint(0,1023)
	if n <= threshold:
		return below
	else:
		return above

def random_int(lower,upper): #inclusive
	random.seed()
	return random.randint(lower,upper)

def two_random_items(l):
	length = len(l)
	if length < 2:
		raise
	first = random_int(0,length-1)
	second = random_int(0,length-1)
	while first == second:
		second = random_int(0,length-1)
	return l[first],l[second]