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

0.10 2009-05-29 Initial version.

    This code is part of Pypso.
    Require matplotlib v.0.98.5.0+
    Used to create the graph analysis.
    
TODO:
    
    
'''

from optparse import OptionParser
from optparse import OptionGroup

TOP = {
   "identify"   : 0, "iteration"  : 1, "bestFitness" : 2,
   "bestPosDim"    : 3
}


#Parse the data from row at the database
#@param line_record: The row
#@param field: The desired field
def parse(line_record, field):
   return line_record[TOP[field]]



def graph_compare_bestFitness(all, id_list, filesave=None):
    data = []
    k = 0
    if type(all[0]) == list:    
        try:
            print "Loading module numpy for some calculation...",
            import numpy
            print " done!\n"
        except:
            print "\ERROR: cannot import Numpy ! Group Report is not available !"
            exit()
            
        for db in all:
            data.append([])
            for i in xrange(len(db[0])):
                bestFitList = []
                for it_out in db:
                    bestFitList.append(parse(it_out[i],"bestFitness"))
                avgFit = numpy.mean(bestFitList)
                data[k].append([i+1,avgFit])
            k+=1

    else:
        for it_out in all:
            data.append([])
            for it in it_out:
                data[k].append([parse(it,"iteration"),parse(it,"bestFitness")])
            k+=1
    
    print "Loading data..." 
    
    colors_list = ["g","b","r","k","m","y"]
    index = 0
    
    pylab.figure()
    
    for it_out in data:
        x = []
        y = []
        for it in it_out:
            x.append(it[0])
            y.append(it[1])
            
        pylab.plot(x, y, colors_list[index], label = "%s" %(id_list[index][:-3],), linewidth=3.0)
        
        index += 1
     
    pylab.xlabel("Number of time steps(iterations)")
    pylab.ylabel("Fitness")
    pylab.legend(prop=FontProperties(size="smaller"))
    
    if filesave:
        pylab.savefig(filesave)
        print "Graph saved to %s file !" % (filesave,)
    else:
        pylab.show()
        print "Graph created!"




if __name__ == "__main__":
    from pypso import __version__ as pypso_version
    from pypso import __author__ as pypso_author

    popGraph = False

    print "PyPso %s - Graph Plot Tool" % (pypso_version,)
    print "By %s\n" % (pypso_author,)
   
    parser = OptionParser()
   
    parser.add_option("-f", "--file", dest="dbfile",
                     help="Database file to read (default is 'pypso.db'.",
                     metavar="FILENAME", default="pypso.db")
   
   
    parser.add_option("-i", "--identify", dest="identify",
                     help="The identify of simulation.", metavar="IDENTIFY")
   
    parser.add_option("-o","--outfile",dest="outfile",
                     help="""Write the report to a pdf file (use just the filename)""",
                     metavar="OUTFILE")
   
    parser.add_option("-e", "--extension", dest="extension",
                  help="""Graph image file format. Supported options (formats) are: emf, eps, pdf, png, ps, raw, rgba, svg, svgz. Default is 'png'.""",
                  metavar="EXTENSION", default="png")
   
    parser.add_option("-t", "--tsrange", dest="tsrange",
                  help="""This is the time steps range of the graph, ex: 1:30 (interval between 1 and 30).""",
                  metavar="TSRANGE")
   
    group = OptionGroup(parser, "Graph types", "These are the supported graph types")
   
    group.add_option("-1", action="store_true", help="""Compare best fitness of two or more evolutions/simulations (For evolution: you must specify the identify comma-separed list with --identify (-i) parameter, like 'one, two, three'), the maximum is 6 items. 
                                                       (For simulation: you must specify the file (dbfile) comma-separed with --file (-f) parameter, like 'one, two , three'), the maximum is 6 items.""" , dest="compare_bestFitness")
 
    parser.add_option_group(group)
   
    (options,args) = parser.parse_args()
   
    if (not options.dbfile):
        parser.print_help()
        exit()
   
    db_list = options.dbfile.split(",")
    db_list = map(str.strip, db_list)
    print db_list
   
    if (options.identify and len(db_list) > 1):
        parser.error("You must choose simulation or evolution graphs!")
    
    if (not options.identify and len(db_list)==1):
        parser.print_help()
        exit()
    
    if not options.compare_bestFitness:
        parser.error("You must choose one graph type !")
    
    print "Loading modules...."
    
    import os.path
    for dbfile in db_list:
        if not os.path.exists(dbfile):
            print "Database file '%s' not found !" % (dbfile, )
            exit()
    
    import pylab
    from matplotlib.font_manager import FontProperties
    import matplotlib.cm
    import sqlite3
    import math
    import os
    
    print "Loading database and creating graph..."

    identify_list = None
    
    if options.identify:
        identify_list = options.identify.split()
        identify_list = map(str.strip,identify_list)
        
    all = None
    
    #Case One: Simulation Graphs
    if len(db_list) > 1:
        all = []
        i = 0
        if (not options.compare_bestFitness):
            parser.error("You can only use the compare bestFitness graph type for simulations analysis!")
        
        for db_file in db_list:
            all.append([])
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            temp = c.execute("select distinct identify from topology")
            fetchtemp = temp.fetchall()
            if len(fetchtemp) > 0:
                for item in fetchtemp:
                    if options.tsrange:
                        tsrange = options.tsrange.split(":")
                        ret = c.execute("select * from topology where identify = ? and iteration between ? and ?", (item[0],tsrange[0],tsrange[1]))
                    else:
                        ret = c.execute("select * from topology where identify = ?", (item[0],))  
                    fetchall = ret.fetchall()   
                    if len(fetchall) > 0:
                        all[i].append(fetchall)   
            i+=1
            
        temp.close()
        conn.close()
        
        if len(all)< len(db_list):
            print "No statistic data found for the database list '%s' !" % (options.dbfile,)
            exit()
        
        total = []
        for all_out in all:
            total.append(len(all_out))
            if len(all_out) <= 0:
                print "No statistic data found for the database list '%s' !" % (options.dbfile,)
                exit()
        
        j = 0
        for sum in total:
            print "%d identify found for %s database." % (sum,db_list[j])
            j+=1
        
        
    if not identify_list:
        identify_list = db_list
    
    
    if options.compare_bestFitness:
        if options.outfile: graph_compare_bestFitness(all, identify_list, options.outfile + "." + options.extension)
        else: graph_compare_bestFitness(all, identify_list)