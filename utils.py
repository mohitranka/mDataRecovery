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

import zipfile
import os
import sys
from sqlite3 import *

class ZipUtils:
    """Utility class for all 'zipfile' module related work.

    Part of implementation is from the snippet at
    http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python
    """
    def toZip(self, file, zip_location):
        """Adds a given file (or directory for that matter) to a zip file.
        
        file - File or Directory that to be zipped.
        zip_location - Location where the resultant .zip file would be created.
        """
        zip_file = zipfile.ZipFile(zip_location, 'w')
        if os.path.isfile(file):
            zip_file.write(file)
        else:
            self.__addFolderToZip(zip_file, file)
        print "Wrote %s to %s"%(file,zip_location)
        zip_file.close()

    def fromZip(self, zip_location,extract_location):
        """Extracts the .zip file to a given location

        zip_location - Location of the .zip file which needs to the extracted.
        extract_location - Path on the file system where the .zip file will be extracted. 
        """
        zip_file = zipfile.ZipFile(zip_location,'r')
        zip_file.extractall(extract_location)

    def __addFolderToZip(self, zip_file, folder): 
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                print 'File added: %s'%(full_path)
                zip_file.write(full_path)
            elif os.path.isdir(full_path):
                print 'Entering folder: %s'%(full_path)
                self.__addFolderToZip(zip_file, full_path)

class SQLiteUtils:
    """Utility class for all SQLite interaction.
    """
    def getLastRevisionNumber(self,db_location):
        """Get the most recent backup revision number.

        db_location - Location of sqlite3 database.
        """
        try:
            conn = Connection(db_location)
            curr = conn.cursor()
            val = curr.execute("SELECT max(rev_id) FROM backups").fetchone()[0]
            if val == None:
                val = 0
            curr.close()
            conn.close()
            return val
        except OperationalError:
            print("Could not get last revision number from database %s"%(db_location))
            sys.exit(1)

    def getMethod(self, db_location, revision_number):
        """Get the backup 'method' for a particular backup revision number.

        db_location - Location of sqlite3 database.
        revision_number - Revision number of the backup.
        """
        try:
            conn = Connection(db_location)
            curr = conn.cursor()
            max_rev_number = curr.execute("SELECT max(rev_id) FROM backups").fetchone()[0]
            if revision_number == None: #revision_number can be 0, so using 'not revision_number' is no good.
                revision_number = max_rev_number
            if revision_number > max_rev_number:
                print "%s is invalid revision number, database has only %s "\
                    "revisions"%(str(revision_number),str(max_rev_number))
                sys.exit(0)
            val = curr.execute("SELECT method FROM backups WHERE"\
                                   " rev_id=%d"%(int(revision_number))).fetchone()[0]
            curr.close()
            conn.close()
            return val
        except OperationalError:
            print("Could not get method from database %s"\
                      " for revision_number %d. "\
                      "Make sure the revision number and database location"\
                      " are correct."%(db_location,int(revision_number)))
            sys.exit(1)

    def getLocation(self, db_location, revision_number):
        """Get the location where backup files are stored,
        for a particular backup revision number.

        db_location - Location of sqlite3 database.
        revision_number - Revision number of the backup.
        """
        try:
            conn = Connection(db_location)
            curr = conn.cursor()
            val = curr.execute("SELECT location FROM backups WHERE"\
                                   " rev_id=%d"%(int(revision_number))).fetchone()[0]
            curr.close()
            conn.close()
            return val
        except OperationalError:
            print("Could not get Location from database %s"\
                      " for revision_number %s. "\
                      "Make sure the revision number and database location"\
                      " are correct."%(db_location,str(revision_number)))
            sys.exit(1)

    def initializeDatabase(self, db_location):
        """If the database does not exists at the specified location,
        create the database and 'backups' table.

        db_location - Location of sqlite3 database.
        """
        if not os.path.isfile(db_location):
            try:
                print "Creating the backup database at %s"%(db_location)
                conn = Connection(db_location)
                curr = conn.cursor()
                curr.execute("CREATE TABLE backups (rev_id serial, "\
                                 "method varchar(40), location varchar(255))")
                curr.close()
                conn.close()
            except OperationalError:
                print ("Cannot create the backup database %s"%(db_location))
                sys.exit(1)

    def writeToDB(self, db_location, revision_number, method, target_location):
        """Write the backup to database.

        db_location - Location of sqlite3 database.
        revision_number - Revision number of the backup.
        method - Method used for backing up the files.
        target_location - Location, where backed up files can be found.
        """
        try:
            conn = Connection(db_location)
            curr = conn.cursor()
            curr.execute("INSERT INTO backups VALUES(%d,'%s','%s')"\
                             %(revision_number,method,target_location))
            conn.commit()
            curr.close()
            conn.close()
        except OperationalError:
            print("Cannot connect to database %s"%(db_location))
            sys.exit(1)
