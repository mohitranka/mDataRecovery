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

from base import Base
from utils import ZipUtils,SQLiteUtils

zObj = ZipUtils()
sObj = SQLiteUtils()

class Local(Base):
    """Restore class for 'Local' Method. 
    """
    def restore(self, **kw):
        """Restores a locally saved backup.
        """
        print "Restoring revision_number %d" %(int(self.revision_number))
        zip_location = sObj.getLocation(self.db_location, int(self.revision_number))
        zObj.fromZip(zip_location, self.target_location)
