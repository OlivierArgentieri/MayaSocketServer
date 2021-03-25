import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

if('mayapy' in sys.executable):
    import mayapy_handler
else:
    import maya_handler
