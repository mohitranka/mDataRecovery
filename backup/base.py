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
import sys
from utils import ZipUtils,SQLiteUtils

zObj = ZipUtils()
sObj = SQLiteUtils()

class Base(object):
    """Base class for Backup.
    """
    def __init__(self, base_location, source_location):
        """Initializes the 'backup' object. Also creates the mDataRecovery base directory
        and Sqlite database, if absent.

        base_location - File system location of base_directory for mDataRecovery.
        source_location - File system location where files needs to be read for making a backup.
        """
        self.base_location = os.path.abspath(base_location)
        self.source_location = os.path.abspath(source_location)
        self.db_location = self.base_location+os.sep+'.mdb'
        self.__initializeDirectory()
        sObj.initializeDatabase(self.db_location)
        self.next_revision_number = sObj.getLastRevisionNumber(self.db_location)+1

    def __initializeDirectory(self):
        if not os.path.isdir(self.base_location):
            try:
                print "Creating the backup directory at %s"%(self.base_location)
                os.mkdir(self.base_location)
            except OSError:
                print("Cannot create backup directory %s"%(self.base_location))
                sys.exit(1)

    
    def backup(self,**kw):
        """backup function which needs to be overridden for all method implementations.
        """
        raise Exception ("backup function is not overriden in %s"%self.__module__)

    def _writeToZip(self,target_location):
        """Write the backup in one zip file
        """
        zObj.toZip(self.source_location,target_location)

    def _writeToDB(self,method,target_location):
        """Write the backup information in the sqlite3 database.
        """
        sObj.writeToDB(self.db_location, self.next_revision_number, method, target_location)
