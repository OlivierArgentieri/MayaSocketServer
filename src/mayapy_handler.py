import sys
by_path = sys.argv[0]
if(by_path != "" ):
    path_to_append = sys.argv[0].split("src")[0]
    sys.path.append(path_to_append) #todo

tmp_modules = sys.modules.copy()
for key, value in tmp_modules.iteritems():
    if key.startswith('src.'):
        sys.modules.pop(key, None)


# import maya.standalone
# maya.standalone.initialize()


from src.servers.mayapy import MayapySocketServer
server = MayapySocketServer()
    
