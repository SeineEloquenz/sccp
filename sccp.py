# SEUS Conquest Compatibility Patcher - Patches the SEUS Renewed Shaderpack to be compatible with Conquest
# Copyright (C) 2020-present Alexander Linder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Home: https://github.com/SeineEloquenz/sccp

import zipfile as zip
import sys

search_string = b'vec4 tex = texture2D(texture, texcoord.st);'
replace_string = b'vec4 tex = texture2D(texture, texcoord.st) * vec4(color.rgb, 1.0);'

if len(sys.argv) != 2:
    print('You need to supply the file name of the SEUS zip')
    exit(1)
path = sys.argv[1]
try:
    with zip.ZipFile(path) as zin, zip.ZipFile(path.replace('.zip', '_patched.zip'), 'w', zip.ZIP_DEFLATED) as zout:
        item: zip.ZipInfo
        for item in zin.infolist():
            buf = zin.read(item.filename)
            if item.filename == 'shaders/gbuffers_water.fsh':
                buf = buf.replace(search_string, replace_string)
            zout.writestr(item.filename, buf)
    print('Successfully patched conquest!')
    exit(0)
except FileNotFoundError:
    print('Zipfile \'' + path + '\' not found.')
except PermissionError:
    print('No permission to open the file \'' + path + '\'.')
except zip.BadZipFile:
    print('ZipFile \'' + path + '\' seems to be corrupt.')
exit(1)
