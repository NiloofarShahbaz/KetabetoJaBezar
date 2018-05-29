how to run project:
--->install python3.5 pip3.5

--->install virtualenv with pip
on linux: sudo pip3.5 install virtualenv

--->create a virtual enviroment
on linux: virtualenv .test


--->activate virtualenv and go to project directory
on linux: source .test/bin/activate
	  cd ketabetojabezar
	  
--->install the requirments
on linux: pip3.5 install -r requirements/local.txt

--->finally you can run the project :))
on linux: python3.5 manage.py runserver --settings=config.settings.local 8000 
	
