#!/usr/bin/python3

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time
import numpy as np
from TSPClasses import *
import heapq
import itertools


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    ''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        best_solution = None
        start_time = time.time()
        while not foundTour and time.time() - start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            best_solution = TSPSolution(route)
            count += 1
            if best_solution.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = best_solution.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = best_solution
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

    def greedy(self, time_allowance=60.0):
        results = {}
        routeFound = False
        route = []
        listOfPossibleStartCities = self._scenario.getCities().copy()
        cities = self._scenario.getCities()
        startCity = listOfPossibleStartCities.pop()
        city = startCity
        route.append(city)
        start_time = time.time()
        while routeFound is False:
            lowestCost = math.inf
            lowestCity = None
            for neighbor in cities:
                if neighbor is city:
                    continue
                if city.costTo(neighbor) < lowestCost and (neighbor not in route):
                    lowestCost = city.costTo(neighbor)
                    lowestCity = neighbor
            if lowestCity is None:  # check to see if can't continue
                if city.costTo(startCity) < lowestCost:  # check to see if we're done
                    routeFound = True
                    bssf = TSPSolution(route)
                else:
                    route.clear()
                    startCity = listOfPossibleStartCities.pop()
                    city = startCity
            # route.append(city)
            else:  # We did find a lowestCity
                route.append(lowestCity)
                city = lowestCity


        end_time = time.time()
        results['cost'] = bssf.cost if routeFound else math.inf
        results['time'] = end_time - start_time
        results['count'] = len(route)
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''

    def branchAndBound(self, time_allowance=60.0):
        pass

    ''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

    def fancy(self, time_allowance=60.0):
        results = {}

        sol_to_beat = self.greedy()["soln"]

        route_to_beat = sol_to_beat.route.copy()

        # route_to_beat = sol_to_beat.enumerateEdges()
        # bssf

        start_time = time.time()

        improved = True
        iter = 1
        while improved:
            print("Iteration num: %s" % iter)
            iter += 1

            for i in range(1, len(route_to_beat)-2):
                improved = False
                for j in range(i+1, len(route_to_beat)):
                    if j-i == 1:
                        continue
                    new_route = route_to_beat.copy()
                    new_route[i:j] = route_to_beat[j-1:i-1:-1]
                    new_sol = TSPSolution(new_route)

                    if new_sol.cost < sol_to_beat.cost:
                        sol_to_beat = new_sol
                        route_to_beat = new_route
                        improved = True

        end_time = time.time()

        results['cost'] = sol_to_beat.cost #  if routeFound else math.inf
        results['time'] = end_time - start_time
        results['count'] = len(route_to_beat)  # Todo: This probs shouldn't be the len of rout_to_beat
        results['soln'] = sol_to_beat
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results
