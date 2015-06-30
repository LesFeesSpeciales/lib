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

#
# Fields
#

# Film fields

# LIb Fields

class Lib(Field):
    pass
    
# Root fields

class Project(Field):
    pass

class Store(Field):
    pass

#
# Project and Store
#

# FILM Folders

# LIB Folders

class LibFolder(PathItem):
    NAME = Lib
    CHILD_CLASSES = ()

# Root folders

class ProjectFolder(PathItem):
    NAME = Project
    CHILD_CLASSES = (LibFolder,)

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
    project = store / 'herakles'

    print(project.path())
    print(project.config())
    
    log.info(logger.getDeltaToStart(log))
    