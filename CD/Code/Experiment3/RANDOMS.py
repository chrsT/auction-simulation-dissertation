''' Auction Simulation Version V10 '''
import random
import scipy.stats

def binary_random_decision(threshold,below,above):
    # below, above inclusive
	random.seed()
	n = random.randint(0,1024)
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

import numpy.random
def normal_random_int(mean,sd,min=1,max=1023):
    val = numpy.random.normal(loc=mean,scale=sd)
    if min is not None and val < min:
        return int(min)
    if max is not None and val > max:
        return int(max)
    return int(val)