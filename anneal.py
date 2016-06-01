# simulated annealing
# Wesley Phoa 1/5/00

from copy import *
from operator import *
from math import *
from random import *

# annealing schedule: reduce temp by this factor each try
sched_const = 0.95

# estimate starting temperature by generating some random scenarios

def start_temp(scenario, objective):
	E0 = objective(scenario)
	Es = []
	for i in range(10):
		idx = randint(0, len(scenario) - 1)
		scenario[idx] = 1 - scenario[idx]
		Es.append(objective(scenario))
		scenario[idx] = 1 - scenario[idx]
	return 2. * max(map(lambda E, E0=E0: abs(E - E0), Es))

# generate a new scenario by taking one Metropolis step
# permit certain event switches to be blocked from toggling

def new_scenario(E, scenario, objective, temp, blocked=[]):
	# assumes that E = objective(scenario)
	new_scen = copy(scenario)
	for i in range(10): # try 10 times to generate a scenario
		idx = randint(0, len(scenario) - 1)
		if not idx in blocked:
			new_scen[idx] = 1 - new_scen[idx]
			Enew = objective(new_scen)
			try:
				if uniform(0., 1.) < exp(-(E - Enew) / temp):
					return new_scen, Enew
				else:
					new_scen[idx] = 1 - new_scen[idx]
			except OverflowError:
				new_scen[idx] = 1 - new_scen[idx]
	return scenario, E

# maximize objective function via simulated annealing

def anneal(scenario, objective, temp, blocked=[], iterations=250):
	E = objective(scenario)
	for i in range(iterations):
		scenario, E = \
			new_scenario(E, scenario, objective, temp, blocked)
		temp = sched_const * temp
	return scenario, E

# generate sorted list of worst case scenarios
# for each event, include at least one scenario in which that event occurs
# and at least one scenario in which that event does not occur

def worst_cases(num_events, objective):
	scenarios = []
	nothing = num_events * [0]

	for i in range(num_events):
		start = copy(nothing)
		start[i] = 1
		E = objective(start)
		temp = start_temp(start, objective)
		new = anneal(start, objective, temp, [i])
		if not new in scenarios:
			scenarios.append(new)

	for i in range(num_events):
		start = copy(nothing)
		E = objective(start)
		temp = start_temp(start, objective)
		new = anneal(start, objective, temp, [i])
		if not new in scenarios:
			scenarios.append(new)

	scenarios.sort(lambda x, y: cmp(y[1], x[1]))
	return scenarios

# sample objective function for testing: 10 events
# NB: if risk is concentrated, worst cases consist of 1 or 2 events
#     if diversified, worst cases consist of many events

sensitivities = [1.2, 2.3, 3.4, 4.3, 3.2, 2.3, 3.4, 4.3, 3.2, 2.1]
shifts        = [100, 50, 200, 50, 200, 50, 100, 50, 100, 50]

sensitivities = 3 * sensitivities
shifts = 3 * shifts

# scales[n-1] = individual shift scaling to apply to an n-event scenario
scales = [100, 78, 66, 58, 53, 48, 45, 41, 38, 36, 33] + range(30, 20, -3)
scales = scales + 50 * [20]
scales = map(lambda x: x/100., scales)

# scenario is a vector of 0s and 1s indicating which events occur
def test(scenario):
	n = reduce(add, scenario)
	return reduce(add, map(lambda switch, sensitivity, shift, \
		scale=scales[n - 1]: switch * sensitivity * shift * scale, \
		scenario, sensitivities, shifts))

if __name__=='__main__':

	import time
	t = time.time()
	worst =  worst_cases(30, test)
	print '%0.2f seconds' % (time.time() - t,)