#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
   Usage :

   import persistence

   # Set a persistence
   foo = {'bar':1}
   persistence.set_persistence("FOO", foo)
   # Save it as json instead of pickle
   persistence.set_persistence("FOO", foo, saveAsJson=True)

   # Get that persistent data back :
   foo = persistence.get_persistence("FOO")
   # or for json version : 
   foo = persistence.get_persistence("FOO", loadAsJson=True)
   # Delete it
   persistence.clear_persistence("FOO")



"""
 
import os
import glob
import json
try:
   import cPickle as pickle
except:
   import pickle


__all__ = ['persistences', 'get_persistence', 'set_persistence', 'clear_persistence', 'clear_all_persistences']

# If not in the root user folder, you can specify here a subfolder to use :
SUBFOLDER = "LFS"

def getPersistenceFolder():
    """
    Return the folder where the persistences will be loaded or saved
    """
    rootPath = os.path.expanduser('~')
    return os.path.join(rootPath, SUBFOLDER)
    
def persistences():
    """
    Lists the available persistences
    """
    persistenceFolder = getPersistenceFolder()

    persistencesList = []
    for p in glob.glob(persistenceFolder + "*.pickle"):
        persistencesList.append(os.basename(p).split('.pickle')[0])
    
    return persistencesList

def get_persistence(name, default=None, loadAsJson=False):
    """
    return the value of a specified persistence or the Default value if not found
    """
    path = os.path.join(getPersistenceFolder(),  "%s%s" % (name, ".pickle" if not loadAsJson else ".json"))

    if not os.path.exists(path):
        return default
    if not loadAsJson:
        try:
            f = open(path, "rb")
            value = pickle.load(f)
            f.close()
            return value
        except:
            return default
    else:
        try:
            with open(path,'r+') as file:
                value = json.load(file)
            file.close()
            return value
        except:
            return default
    
def set_persistence(name, value, saveAsJson=False):
    """
    set a persistence (create a new one or override existing one)
    return the value if the file was written well,
    return None if it was not able to save it
    if saveAsJson = True, save the persistence in a json format instead of pickle
    """
    persistenceFolder = getPersistenceFolder()
    path = os.path.join(getPersistenceFolder(), "%s%s" % (name, ".pickle" if not saveAsJson else ".json")) 
    
    if not os.path.exists(persistenceFolder):
        try:     os.makedirs(persistenceFolder)
        except:  raise("Impossible to create the persistent folder")
    
    if not saveAsJson:
        try:
            f = open(path, "wb")
            pickle.dump(value, f)
            f.close()
            return True
        except:
            raise("ERROR : Impossible to create the pickle %s" % path)
    else:
        try:
            f = open(path, "w")
            f.write(json.dumps(value))
            f.close()
            return True
        except:
            raise("ERROR : Impossible to create the json %s" % path)
    
def clear_persistence(name):
    """
    delete the named persistence
    return True if deleted or brownie does not exists already
    """
    persistenceFolder = getPersistenceFolder()
    path = os.path.join(getPersistenceFolder(),  name + ".pickle")
    if not os.path.exists(path): return True
    try:
        os.remove(path)
        return True
    except:
        raise('ERROR : impossible to delete file %s' % path)


def clear_all_persistences():
    """
    delete all the persistences available
    """
    for b in persistences():
        clear_persistence(b)
    return True
    

