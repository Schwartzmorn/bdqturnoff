#!/bin/bash

dirName=`pwd`
# Gets the name of the folder we're in
curFolder="${dirName%"${dirName##*[!/]}"}"
targetFolder="$HOME/.kodi/addons/${curFolder##*/}"

rsync -a --exclude='.git' --include='*.py' --include='*.xml' --include='LICENSE' --include='*/' --exclude='*' . ${targetFolder} --delete
