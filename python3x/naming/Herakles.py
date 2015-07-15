"""
File discribing our naming conventions
"""

import os
import re



from kabaret.naming import (
    Field, ChoiceField, MultipleFields, CompoundField, IndexingField, FixedField,
    FieldValueError,
    PathItem
)

"""
TODO
####
Fonction de detection du store ?

"""


"""
Store/
    Project/
        FILM/
            SEQ/
                SHOT/
                    Dept/
                        FILM_SEQ_Shot-Dept/
                            FILM_SEQ_Shot-Dept-SubTypes-Version.frame.ext
                                                  |       |       |> optional
                                                  |       |> optional
                                                  |> optional
        LIB/
            FAMILY/
                ASSET/
                    Dept/
                        LIB_FAMILY_Asset-Dept/
                            LIB_FAMILY_Asset-Dept-SubTypes-Version.frame.ext
                                                     |       |       |> optional
                                                     |       |> optional
                                                     |> optional

                



"""

#
# Fields
#

class Dept(ChoiceField):
    choices = ['Mod', 'Actor', 'Shad', 'Anim','Layout','Lighting', 'Compo', 'Matte',  'Cam', 'Vfx'] 
    # A decliner 
    # Mod, Mod_Ok, Actor, Actor_OK, ...

class Family(ChoiceField):
    choices = ['Chars', 'Props', 'Sets','Lookdev']

class Extension(ChoiceField):
    choices = ["blend", "psd"]

class Version(IndexingField):
    prefix = "v"
    padding = "@@"
    optional = True
    def increment(self):
        if not re.match("v([\d]+)", self._value):
            raise FieldValueError("Value %s is not a v@@' % self._value")
        self._value = "v%02i" % ( int(re.match("v([\d]+)", self._value).group(0)) + 1)

class Type(Field):
    def validate(self):
        super(Type, self).validate()
        if re.match("v([\d]+)", self._value): 
            raise FieldValueError("Value %s Looks to be a version and not a TAG" % self._value)
        elif not re.match("[A-Za-z0-9]+$", self._value): 
            raise FieldValueError("Value %s uses a non authorized character (only a->Z and 0->9)" % self._value)

class SubTypes(MultipleFields):
    field_type = Type
    separator = '_'
    optional = True

class Edit(FixedField):
    fixed_value = "EDIT"

class Frame(Field):
    def validate(self):
        super(Frame, self).validate()
        if not self._value.isdigit(): raise FieldValueError("Value %s uses a non authorized character (only 0->9)" % self._value)


# Film fields

class Film(Field):
    def validate(self):
        super(Film, self).validate()
        if not re.match("[A-Za-z0-9]+$", self._value): raise FieldValueError("Value %s uses a non authorized character (only a->Z and 0->9)" % self._value)

class Sequence(Field):
    def validate(self): # a LIB folder should start by LIB
        super(Sequence, self).validate()
        if not self._value.startswith('S'): raise FieldValueError("Value %s is not a Sequence" % self._value)

class Shot(Field):
    def validate(self): # a LIB folder should start by LIB
        super(Shot, self).validate()
        if not self._value.startswith('P'): raise FieldValueError("Value %s is not a Shot" % self._value)

class ShotId(CompoundField):
    fields = (Film, Sequence, Shot)
    separator = "_" 

class ShotTask(CompoundField):
    fields = (ShotId, Dept)
    separator = "-"

class ShotTaskFull(CompoundField):
    fields = (ShotId, Dept, SubTypes, Version)
    separator = '-'    

class ShotTaskFile(CompoundField):
    fields = (ShotTaskFull,  Extension)
    separator = '.'

class ShotTaskFileWithFrameNumber(CompoundField):
    fields = (ShotTaskFull, Frame, Extension)
    separator = '.'

# LIb Fields

class Lib(Field):
    def validate(self): # a LIB folder should start by LIB
        super(Lib, self).validate()
        if not self._value.startswith('LIB'): raise FieldValueError("Value %s is not a LIB" % self._value)

class Asset(Field):
    def validate(self):
        super(Asset, self).validate()
        if not re.match("[A-Za-z0-9]+$", self._value): raise FieldValueError("Value %s uses a non authorized character (only a->Z and 0->9)" % self._value)


class AssetId(CompoundField):
    fields = (Lib, Family, Asset)
    separator = "_" 

class AssetTask(CompoundField):
    fields = (AssetId, Dept)
    separator = "-"

class AssetTaskFull(CompoundField):
    fields = (AssetId, Dept, SubTypes, Version)
    separator = '-'    

class AssetTaskFile(CompoundField):
    fields = (AssetTaskFull, Extension)
    separator = '.'

class AssetTaskFileWithFrameNumber(CompoundField):
    fields = (AssetTaskFull, Frame, Extension)
    separator = '.'




# Root fields

class Project(Field):
    pass

class Store(Field):
    pass

#
# Project and Store
#

# FILM Folders

class ShotRefFile(PathItem):
    NAME = ShotTaskFile
    CHILD_CLASSES = ()

class ShotRefFileWithFrameNumber(PathItem):
    NAME = ShotTaskFileWithFrameNumber
    CHILD_CLASSES = ()

class ShotTaskFolder(PathItem):
    NAME = ShotTask
    CHILD_CLASSES = (ShotRefFileWithFrameNumber,ShotRefFile,)

class ShotDeptFolder(PathItem):
    NAME = Dept
    CHILD_CLASSES = (ShotTaskFolder,)

class ShotFolder(PathItem):
    NAME = Shot
    CHILD_CLASSES = (ShotDeptFolder,)

class SequenceFolder(PathItem):
    NAME = Sequence
    CHILD_CLASSES = (ShotFolder,)

class FilmFolder(PathItem):
    NAME = Film
    CHILD_CLASSES = (SequenceFolder,)

# LIB Folders



class AssetRefFile(PathItem):
    NAME = AssetTaskFile
    CHILD_CLASSES = ()

class AssetRefFileWithFrameNumber(PathItem):
    NAME = AssetTaskFileWithFrameNumber
    CHILD_CLASSES = ()

class AssetTaskFolder(PathItem):
    NAME = AssetTask 
    CHILD_CLASSES = (AssetRefFileWithFrameNumber,AssetRefFile,)

class AssetDeptFolder(PathItem):
    NAME = Dept
    CHILD_CLASSES = (AssetTaskFolder,)

class AssetFolder(PathItem):
    NAME = Asset
    CHILD_CLASSES = (AssetDeptFolder,)

class FamilyFolder(PathItem):
    NAME = Family
    CHILD_CLASSES = (AssetFolder,)

class LibFolder(PathItem):
    NAME = Lib
    CHILD_CLASSES = (FamilyFolder,)

# Root folders

class ProjectFolder(PathItem):
    NAME = Project
    CHILD_CLASSES = (LibFolder, FilmFolder)


class StoreFolder(PathItem):
    NAME = Store
    CHILD_CLASSES = (ProjectFolder,)

    
    @classmethod
    def from_path(cls, path, root=None):
        if root:
            remaining_path = path.replace(root, '')
            print(remaining_path)
            item = cls.from_name(root)
            return item / remaining_path
        else:
            store, remaining_path = path.split("/", 1)
            item = cls.from_name(store)
            return item/remaining_path


def guessStore(path, splitLevel = 0):
    """
    This function tries to guees the Store path : it's an experiment
    IF the rest of the path match the needed keys for the config of the remaining path
    In this example, the rest of the path should be pretty complete as we ask for 
    a lot of keys

    Return a string if a store is found with a valid config
    Return None otherwise... (might be a bad path also, not checked)

    Usage :
    store = guessStore("Path/To/Check")
    if not store : print("Impossible to guess the root path")
    """
    if splitLevel > path.count("/"): return None
    neededKeys = [
            ["Project", "Film", "Sequence", "Shot", "Dept"], # OR :
            ["Project", "Lib", "Asset", "Family", "Dept"]
        ]
    
    try:
        remainingPath = path.split("/", splitLevel)[-1]
        store = "/".join(path.split("/", splitLevel)[:-1])
        if not store: store = "/"
    except: # End of the line ?
        return None
    n =  StoreFolder.from_path(remainingPath, store)
    if n.is_wild():
        return guessStore(path, splitLevel +1)
    else:
        c = n.config()
        print(c)
        for keys in neededKeys:
            allKeys = True
            for k in keys:
                if not k in c : allKeys = None
            if allKeys :
                print(n.path())
                return store
        return guessStore(path, splitLevel +1)
#
# TESTS
#

if __name__ == "__main__":
    
   
    n = StoreFolder.from_path("C:/titi/toto/projet/FILM/Seq01/Plan02/Anim", "C:/titi/toto/")
    #print(n.config())

    
    store = StoreFolder.from_name('Projets')
    project = store / 'herakles/LIB/Chars/Flavio/Mod/LIB_Chars_Flavio-Mod/LIB_Chars_Flavio-Mod-TypeA_TypeB-v01.blend'

    #print(project.path())
    #print(project.config())
    
    if project.is_wild():
        print(project.why())

    store = StoreFolder.from_name('Projets')
    project = store / 'herakles/HERAKLES/S01/P02/Anim/HERAKLES_S01_P02-Anim/HERAKLES_S01_P02-Anim-TypeA_TypeB-v01.blend'

    print(project.path())
    print(project.config())
    
    if project.is_wild():
        print(project.why())

    project = store / 'herakles/HERAKLES/S01/P02/Anim/HERAKLES_S01_P02-Anim/HERAKLES_S01_P02-Anim-TypeA_TypeB.5123.blend'

    print(project.path())
    print(project.config())
    
    if project.is_wild():
        print(project.why())


    