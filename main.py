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
from optparse import OptionParser
from utils import SQLiteUtils

VALID_METHODS = ('Local')
def parseOptions():
    """Adds different commandline options for mDataRecovery. 
    """
    parser = OptionParser()
    parser.add_option('-a',
                      '--action',
                      dest="action",
                      help="User action ('backup' or 'restore').No default.\n")
    
    parser.add_option('-s',
                      '--source_location',
                      dest='source_location',
                      help="Location of source directory for backup.No default.\n\n")

    parser.add_option('-m',
                      '--method',
                      dest='method',
                      help="Method of backup ('Local' or 'Rsync' or 'AWS' or "\
                          "'Rackspace' etc). Only 'Local' is supported as of now.\n\n",
                      default='Local')

    parser.add_option('-b',
                      '--base_location',
                      dest="base_location",
                      help="Location of the mDataRecovery backup directory"\
                          " to be create.Defaults to '.mdatarecovery' "\
                          "in current directory.\n\n",
                      default='.mdatarecovery')    

    parser.add_option('-r',
                      '--revision_number',
                      dest='revision_number',
                      help='Revision number which is needs to be restored.'\
                          ' Defaults to most recent version.\n\n',
                      default=None)

    parser.add_option('-t',
                      '--target_location',
                      dest='target_location',
                      help='Location where the restoration should happen.'\
                          'Defaults to current directory.\n\n',
                      default='.')

    (params, args) = parser.parse_args()

    if params.action not in ('backup', 'restore'):
        print "--action should be either 'backup' or 'restore'."
        sys.exit(0)

    if params.action == 'backup':
        if not params.method in VALID_METHODS:
            print "--method must be in %s." %(",".join(VALID_METHODS))
            sys.exit(0)

        if not params.source_location:
            print "--source_location must be secified."
            sys.exit(0)
    return params

if __name__ == '__main__':
    parser = parseOptions()

    if parser.action == 'backup':
        # Create a backup method object, based on parser.method,
        # and call the .backup() function 
        backupObj = __import__('backup.' + parser.method.lower(),\
                                   globals(),
                               locals(), [parser.method],-1)\
                               .__dict__[parser.method]\
                               (parser.base_location,parser.source_location)
        backupObj.backup()

    elif parser.action == 'restore':
        # Create the restore method object, based on the method specified
        # in the database, and call .restore() function.
        sObj = SQLiteUtils()
        method = sObj.getMethod(parser.base_location + os.sep + \
                                    '.mdb',parser.revision_number)
        restoreObj = __import__('restore.' + method.lower(),\
                                    globals(),
                                locals(), [method],-1)\
                                .__dict__[method](parser.base_location,
                                                      parser.target_location,
                                                      parser.revision_number)
        restoreObj.restore()
