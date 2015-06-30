"""
File discribing our naming conventions
"""

import os
import re

if __name__ == "__main__":
    import sys
    sys.path.append("/u/lib/python3x")


from kabaret.naming import (
    Field, ChoiceField, MultipleFields, CompoundField, IndexingField, FixedField,
    FieldValueError,
    PathItem
)

#
# Fields
#

class Project(Field):
    pass

class Store(Field):
    pass

#
# Project and Store
#

class ProjectFolder(PathItem):
    NAME = Project
    CHILD_CLASSES = ()

class StoreFolder(PathItem):
    NAME = Store
    CHILD_CLASSES = (ProjectFolder,)


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
    