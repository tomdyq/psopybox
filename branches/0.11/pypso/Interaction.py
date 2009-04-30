'''
Particle Swarm Optimization - PyPSO 

Copyright (c) 2009 Marcel Pinheiro Caraciolo
caraciol@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

0.10 2009-04-29 Initial version.
'''

"""
In this module, you will find the funcionality for the term `Interactive mode`.
When you enter in the Interactive Mode, PyPso will automatic import this module
and exposes to you in the name space called "it".
"""

from pypso import Util

try:
   print "Loading module pylab (matplotlib)...",
   import pylab
   print " done!\n"
except:
   print "\nWarning: cannot import Matplotlib ! Plots will not be available !"

try:
   print "Loading module numpy...",
   import numpy
   print " done!\n"
except:
   print "\nWarning: cannot import Numpy ! Some functions will not be available !"

#Returns a list of swarm fitness scores
#@param topology: The swarm object
#@param bestFitness: If it's True, the best fitness will be used, otherwise, the current one.
#@return the list of the swarm fitness
def getSwarmFitness(topology, bestFitness=False):
    fitness_list = []
    for particle in topology.getSwarm():
        if bestFitness:
            x = particle.ownBestFitness
        else:
            x = particle.fitness
        fitness_list.append(x)
    return fitness_list

#Returns a list of swarm particles positions (2 dimmensions)
#@param topology: The swarm object
#@param bestPosition: If it's True, the best position will be used, otherwise, the current one.
#@return the list of the swarm particles positions
def getSwarmPosition(topology, bestPosition=False):
    position_list = []
    for particle in topology.getSwarm():
        if bestPosition:
            x = particle.ownBestPosition[:2]
        else:
            x = particle.position[:2]
        position_list.append(x)
    return position_list

#Plot the swarm fitness distribution
#@param topology: The topology object
#@param bestFitness: If it's True, the bestFitness score will be used, otherwise, the current one.
def plotSwarmFitness(topology, bestFitness=False):
    fitness_list = getSwarmFitness(topology,bestFitness)
    pylab.plot(fitness_list,'o')
    pylab.title("Plot of the swarm fitness distribution")
    pylab.xlabel('Particle')
    pylab.ylabel('Fitness')
    pylab.grid(True)
    pylab.show()

#Swarm fitness distribution histogram
#@param topology: The topology object
#@param bestFitness: if it's True, the bestFitness will be used, otherwise, the current one.
def plotHistSwarmFitness(topology, bestFitness=False):
    fitness_list = getSwarmFitness(topology,bestFitness)
    n,bins,patches = pylab.hist(fitness_list,50,facecolor='green',alpha=0.75,normed=1)
    pylab.plot(bins,pylab.normpdf(bins,numpy.mean(fitness_list),numpy.std(fitness_list)),'r--')
    pylab.xlabel('Fitness')
    pylab.ylabel('Frequency')
    pylab.grid(True)
    pylab.title("Plot of the swarm fitness distribution")
    pylab.show()

#Plot the swarm position (2D Dimension)
#@param topology: The  topology object
#@param bestPosition: if it's True, the bestPosition will be used, otherwise, the current one.
def plotSwarmPosition(topology,bestPosition=False):
    position_list = getSwarmPosition(topology,bestPosition)
    pylab.plot(position_list,'o')
    pylab.title("Plot of the swarm position distribution")
    pylab.xlabel('Particle')
    pylab.ylabel('Position')
    pylab.grid(True)
    pylab.show()
