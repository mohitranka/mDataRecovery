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
from base import Base

class Local(Base):
    """Backup class for 'Local' Method. 
    """
    def backup(self,**kw):
        """Backup data on the local file system.
        """
        target_location = self.base_location+os.sep+str(self.next_revision_number)+'.zip'
        self._writeToZip(target_location)
        self._writeToDB('Local',target_location)
