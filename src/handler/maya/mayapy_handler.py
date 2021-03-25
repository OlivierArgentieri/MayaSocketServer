import sys
by_path = sys.argv[0]
if(by_path != "" ):
    path_to_append = sys.argv[0].split("pipeline2")[0]
    sys.path.append(path_to_append) #todo

tmp_modules = sys.modules.copy()
for key, value in tmp_modules.iteritems():
    if key.startswith('pipeline2.'):
        sys.modules.pop(key, None)


import maya.standalone
maya.standalone.initialize()


from pipeline2.engines.servers.mayapy import MayapySocketServer
server = MayapySocketServer()
    
