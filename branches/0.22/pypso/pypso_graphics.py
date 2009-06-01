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


if __name__ == "__main__":
   from pypso import __version__ as pypso_version
   from pypso import __author__ as pypso_author

   popGraph = False

   print "PyPso %s - Graph Plot Tool" % (pypso_version,)
   print "By %s\n" % (pypso_author,)
   
   parser = OptionParser()
   