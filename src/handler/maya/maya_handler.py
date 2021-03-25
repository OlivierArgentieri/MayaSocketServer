import sys, os        
dir_path = os.path.dirname(os.path.realpath(__file__))

if(dir_path != "" ):
    path_to_append = dir_path.split("pipeline2")[0]
    sys.path.append(path_to_append) #todo

tmp_modules = sys.modules.copy()
for key, value in tmp_modules.iteritems():
    if key.startswith('pipeline2.'):
        sys.modules.pop(key, None)


from pipeline2.engines.servers.maya import MayaSocketServer
server = MayaSocketServer()