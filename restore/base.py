# mDataRecovery, CommandLine backup utility for unix.
# Copyright (C) 2010  Mohit Ranka
    
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see http://www.gnu.org/licenses/agpl.txt.

import os
from utils import SQLiteUtils

sObj = SQLiteUtils() 

class Base(object):
    """Base class for Restore.
    """
    def __init__(self, base_location, target_location, revision_number):
        """Initializes the 'restore' object.

        base_location - File system location of base_directory for mDataRecovery.
        target_location - File system location where files needs to be restored.
        revision_number - revision_number to be restored, if None is supplied, most
                          recent revision is restored.
        """
        self.base_location = os.path.abspath(base_location)
        self.target_location = os.path.abspath(target_location)
        self.db_location = self.base_location+os.sep+'.mdb'
        self.revision_number = self.__getRevisionNumber(revision_number)
        
    def __getRevisionNumber(self,revision_number):
        if not revision_number:
            return sObj.getLastRevisionNumber(self.db_location)
        return revision_number

    def restore(self,**kw):
        """restore function which needs to be overridden for all method implementations.
        """
        raise Exception ("restore function is not overriden in %s"%self.__module__)
