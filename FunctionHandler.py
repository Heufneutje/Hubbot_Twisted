import os, sys
from glob import glob
import GlobalVars

def LoadFunction(path, loadAs=''):
    loadType = 'l'
    name = path
    src = __import__('Functions.' + name, globals(), locals(), [])
    if loadAs != '':
        name = loadAs
    if name in GlobalVars.functions:
        loadType = 'rel'
        del sys.modules['Functions.'+name]
        for f in glob ('Functions/%s.pyc' % name):
            os.remove(f)
        
    reload(src)

    components = name.split('.')
    for comp in components[:1]:
        src = getattr(src, comp)
    
    ModuleName = str(src).split("from")[0].lstrip("<").rstrip(" ")
    ModuleName = ModuleName[0:1].upper() + ModuleName[1:]
    if loadType != 'rel':
        print "--- {} loaded.".format(ModuleName)
    else:
        print "--- {} reloaded.".format(ModuleName)
        
    func = src.Instantiate()
    
    GlobalVars.functions.update({name:func})

    return loadType

def UnloadFunction(name):
    success = True
    if name in GlobalVars.functions.keys():
        del GlobalVars.functions[name]
    else:
        success = False

    return success

def AutoLoadFunctions():
    root = os.path.join('.', 'Functions')
    for item in os.listdir(root):
        if not os.path.isfile(os.path.join(root, item)):
            continue
        if not item.endswith('.py'):
            continue
        
        try:
            if item[:-3] not in GlobalVars.nonDefaultModules:
                LoadFunction(item[:-3])
        except Exception, x:
            print x.args
