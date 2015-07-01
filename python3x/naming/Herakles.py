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
RootDrive/
    Project/
        FILM/
            SEQ/
                SHOT/
                    Dept/
                        FILM_SEQ_Shot-Dept/
                            FILM_SEQ_Shot-Dept-SubTypes-Version.ext
        LIB/
            FAMILY/
                ASSET/
                    Dept/
                        LIB_FAMILY_Asset-Dept/
                            LIB_FAMILY_Asset-Dept-SubTypes-Version.ext

                



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
    fields = (ShotTaskFull, Extension)
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


class ShotTaskFolder(PathItem):
    NAME = ShotTask
    CHILD_CLASSES = (ShotRefFile,)

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

class AssetTaskFolder(PathItem):
    NAME = AssetTask 
    CHILD_CLASSES = (AssetRefFile,)

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


#
# TESTS
#

if __name__ == "__main__":
    import log as logger

    log = logger.getLogger("naming")
    log.info("Naming test of %s" % __file__)
    log.info("Sarting tests")

    store = StoreFolder.from_name('Projets')
    project = store / 'herakles/LIB/Chars/Flavio/Mod_OK/LIB_Chars_Flavio-Mod_OK/LIB_Chars_Flavio-Mod_OK-TypeA_TypeB-v01.blend'

    print(project.path())
    print(project.config())
    
    if project.is_wild():
        print(project.why())

    store = StoreFolder.from_name('Projets')
    project = store / 'herakles/HERAKLES/S01/P02/Anim/HERAKLES_S01_P02-Anim/HERAKLES_S01_P02-Anim-TypeA_TypeB-v01.blend'

    print(project.path())
    print(project.config())
    
    if project.is_wild():
        print(project.why())

    log.info(logger.getDeltaToStart(log))
    