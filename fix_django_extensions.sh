#!/bin/bash

# Fix django_extensions

if [ -z $VIRTUAL_ENV ]
	then
		echo "Please switch to opentracks virtual environment"
		exit 1
fi

cd $VIRTUAL_ENV/lib/python2.7/site-packages

if [ -d django_extensions/tests ]
	then
		mv django_extensions/tests/test_print_settings.py django_extensions/tests/test_print_settings.py.bak
		perl -i.bak -pe 's/from django_extensions.tests.test_print_settings import PrintSettingsTests/#from django_extensions.tests.test_print_settings import PrintSettingsTests/g' django_extensions/tests/__init__.py
		perl -i.bak -pe 's/def testUUIDField_pkAgregateCreate/#def testUUIDField_pkAgregateCreate/g' django_extensions/tests/uuid_field.py 
		perl -i.bak -pe 's/j = TestAgregateModel.objects.create/#j = TestAgregateModel.objects.create/g' django_extensions/tests/uuid_field.py
	else
		echo "django_extensions module not found"
		exit 1
fi
