#!/bin/bash

# Fix tree rights.

USER=ctb
GROUP=ctb

if [ ! -x /bin/realpath ]
	then
		exit 1
fi

if [ ! -x /bin/dirname ]
	then
		exit 1
fi

SCRIPT_FULL_PATH=$(/bin/realpath "$0")
DIRNAME=$(/bin/dirname "$SCRIPT_FULL_PATH")

cd $DIRNAME

find $DIRNAME -exec chown $USER:$GROUP {} \;
find $DIRNAME -type d -exec chmod 755 {} \;
find $DIRNAME -type f -exec chmod 644 {} \;

chmod 777 $DIRNAME/tools/cache
chmod 666 $DIRNAME/tools/cache/*

chmod u+x *.sh
chmod u+x manage.py
chmod u+x $DIRNAME/tools/*.py 
