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
0.11 2009-05-28 Added support for database adapter (SQLite3 database)
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
import types
import sqlite3
import SwarmStatistics
import TopologyStatistics
#DBSQLite Class - Adapter to dump data in SQLite3 database format
class ReportDB:
    #The Creator of the ReportDB Class
    #@param dbname: The database filename
    #@param identify: the identify if the run
    #@param resetDB: if True, the database structure will be recreated
    #@param resetIdentify: if True, the identify with the same name will be overwrite with the new data
    #@param frequency: the generational dump frequency
    #@param commit_frequency: the commit frequency
    def __init__(self,dbname=Consts.CDefDBName,identify=None,resetDB=True,
                 resetIdentify=True,frequency=Consts.CDefDBStatsGenFreq, 
                 commit_freq=Consts.CDefDBStatsCommitFreq):
        
        if identify is None:
            self.identify = datetime.datetime.strftime(datetime.datetime.now(),"%d/%m/%y-%H:%M")
        else:
            self.identify = identify
        
        self.connection = None
        self.resetDB = resetDB
        self.resetIdentify = resetIdentify
        self.dbName = dbname
        self.typeDict = {types.FloatType: "real"}
        self.statsGenFreq = frequency
        self.cursorPool = None
        self.commitFreq = commit_freq
    
    #The string representation of adapter
    def __repr__(self):
        ret = "Report DB Adapter [File='%s', identify='%s']" % (self.dbName, self.identify)
        return ret
    
    #Open the database connection
    def open(self):
        print "Opening database, dbname=%s" % self.dbName
        self.connection = sqlite3.connect(self.dbName)
        
        if self.resetDB:
            self.resetStructure((SwarmStatistics.SwarmStatistics(),TopologyStatistics.TopologyStatistics()))
        
        if self.resetIdentify:
            self.resetTableIdentify()
    
    #commit changes on database and closes connection
    def saveAndClose(self):
        self.commit()
        self.close()
    
    #Close the database connection
    def close(self):
        print "Closing the database."
        if self.cursorPool:
            self.cursorPool.close()
            self.cursorPool = None
        self.connection.close()
    
    #Commit changes to database
    def commit(self):
        self.connection.commit()
    
    #Return a cursor from the pool
    def getCursor(self):
        if not self.cursorPool:
            self.cursorPool = self.connection.cursor()
            return self.cursorPool
        else:
            return self.cursorPool
        
    
    #Create table using the Statistics class structure
    def createStructure(self,stats):
        c = self.getCursor()
        
        pstmt = "create table if not exists %s(identify text, iteration integer, " % (Consts.CDefReportDBSwarmTable)
        #Swarm statistics
        for k,v in stats[0].items():
            pstmt += "%s %s, " % (k, self.typeDict[type(v)])
        pstmt = pstmt[:-2] + ")"
        c.execute(pstmt)
        
        pstmt = "create table if not exists %s(identify text, iteration integer, bestFitness real, bestPosDim real)" % (Consts.CDefReportDBTopTable)
        #Topology statistics
        c.execute(pstmt)
        
        #Swarm individuals statistics
        pstmt = """create table if not exists %s(identify text, iteration integer,
                particle integer, fitness real, bestFitness real)""" % (Consts.CDefSQLiteDBPartTable)
        c.execute(pstmt)
        self.commit()
    
    #Delete all records on the table with the same identify
    def resetTableIdentify(self):
        c = self.getCursor()
        stmt = "delete from %s where identify  = ?" % (Consts.CDefReportDBSwarmTable)
        stmt2 = "delete from %s where identify = ?" % (Consts.CDefReportDBTopTable)
        stmt3 = "delete from %s where identify = ?" % (Consts.CDefSQLiteDBPartTable)
        
        try:
            c.execute(stmt, (self.identify,))
            c.execute(stmt2, (self.identify,))
            c.execute(stmt3, (self.identify,))
        except sqlite3.OperationalError, expt:
            if expt.message.find("no such table") >= 0:
                print "\n ## The DB Adapter can't find the tables ! Consider enable the parameter resetDB ! ##\n"
        
        self.commit()

    #Deletes the current structure and creates a new one.
    def resetStructure(self,stats):
        c = self.getCursor()
        c.execute("drop table if exists %s" % (Consts.CDefReportDBSwarmTable,))
        c.execute("drop table if exists %s" % (Consts.CDefReportDBTopTable,))
        c.execute("drop table if exists %s" % (Consts.CDefSQLiteDBPartTable,))
        self.commit()
        self.createStructure(stats)

    #Inserts the statistics into the database
    #@param stats: The statistics objects
    #@param topology: The swarm to insert stats (class: Topology.Topology)
    #@param iteration: The iteration of the insert
    def insert(self,stats,topology,iteration):
        c = self.getCursor()
        #Swarm statistics
        pstmt = "insert into %s values (?, ?, " % (Consts.CDefReportDBSwarmTable)
        for i in xrange(len(stats[1])):
            pstmt += "?, "
        pstmt = pstmt[:-2] + ")"
        c.execute(pstmt, (self.identify,iteration) + stats[1].asTuple())

        #Topology statistics
        pstmt = "insert into %s values(?, ?, ?, ?) " % (Consts.CDefReportDBTopTable)
        c.execute(pstmt, (self.identify,iteration,stats[0]["bestFitness"],stats[0]["bestPosDim"]))
        
        #Particles statistics
        pstmt = "insert into %s values(?, ?, ?, ?, ?)" % (Consts.CDefSQLiteDBPartTable,)
        tups = []
        for i in xrange(len(topology.getSwarm())):
            particle = topology.getSwarm()[i]
            tups.append((self.identify,iteration,i, particle.fitness, particle.ownBestFitness))
        c.executemany(pstmt,tups)
        if (iteration % self.commitFreq == 0):
            self.commit()
            

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
        print "Opening the CSV file to dump statistics [%s]" % self.filename
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

