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

0.10 2009-05-25 Initial version.
'''

'''
    This module contains the adapters which you can use to save the statistics 
    of every iteration in a file or database with the statistics as parameters.
    You can use the report to plot convergence statistics graphs later.
    
    warning: THE USE OF THE REPORT ADAPTER CAN REDUCE THE PERFORMANCE OF THE
             PSO ALGORITHM.
'''

import csv
import Consts

#ReportFileCSV Class  - Adapter to dump statistics in CSV format
class ReportFileCSV:
    
    #The creator of ReportFileCSV Class
    #@param filename: The CSV filename
    #@param identify: The identify of the run
    #@param frequency: the generational dump frequency
    #@param reset: if is True, the file old data will be overwrite with the new
    def __init__(self, filename=Consts.CDefCSVFileName, identify=None,
                 frequency = Consts.CDefCSVFileStatsGenFreq, reset= True):
        if identify is None:
            self.identify = datetime.datetime.strftime(date.datetime.now(),"%d/%m/%y-%H:%M")
        else:
            self.identify = identify
        
        self.filename = filename
        self.statsGenFreq = frequency
        self.csvWriter = None
        self.fHandler = None
        self.reset = reset
     
    #The String representation of adapter
    #@return the representation
    def __repr__(self):
        ret = "ReportFileCSV Report Aadapter [File='%s', identify='%s']" % (self.filename,self.identify)
        return ret

    #Open the CSV file or creates a new file
    def open(self):
        print "Opening the CSV file to dump statistics [%s]", self.filename
        if self.reset: open_mode = "w"
        else: open_mode = "a"
        self.fHandler = open(self.filename,open_mode)
        self.csvWriter = csv.writer(self.fHandler,delimiter=";")
        
    #Closes the CSV file handler"
    def close(self):
        if self.fHandler:
            self.fHandler.close()
    
    #Commits and close
    def saveAndClose(self):
        self.commit()
        self.close()
    
    #Stub
    def commit(self):
        pass
    
    #Inserts the stats into the CSV file
    #@param stats: The statistics tuple (topology statistics, swarm statistics)
    #@param topology: The swarm to insert stats (class: Topology.Topology)
    #@param iteration: The iteration of the insert
    def insert(self,stats,topology,iteration):
        line = [self.identify,iteration]
        line.extend(stats[0].asTuple())
        line.extend(stats[1].asTuple())
        self.csvWriter.writerow(line)