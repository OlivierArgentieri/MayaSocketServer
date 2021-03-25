import sys, os        
dir_path = os.path.dirname(os.path.realpath(__file__))

if dir_path != "":
    path_to_append = dir_path.split("src")[0]
    sys.path.append(path_to_append) #todo

tmp_modules = sys.modules.copy()
for key, value in tmp_modules.iteritems():
    if key.startswith('src.'):
        sys.modules.pop(key, None)


from src.servers.maya import MayaSocketServer
server = MayaSocketServer()