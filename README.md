DigOps
======

DigOps is a Django App designed to keep track of time spent in different 
workflow steps involved in digitization of items. DigOps also supports generation
of reports that can be used to track the rate at which items are being digitized.
It also supports plotting of data in graphs using Google chart API.
It uses Django authentication to identify users of the system.It drastically 
reduces tedious labor and endless headaches in keeping track of hours spent 
on a digital operation.

Installation Instructions
-------------------------

This software should be runnable on any kind of operating system. However, 
these installation instructions are tailored to a Linux server, and have
only been tested on ubuntu 10.04 LTS.

**Part I - Basic server requirements**

1. Install the Apache Django and other dependencies using the following command:

        sudo apt-get install apache2 python-dev  python-setuptools libapache2-mod-wsgi

2. Install Postgresql
        
        sudo apt-get install postgresql postgresql-contrib libpq-dev
   
   Install the dependencies you need to compile psycopg2 in virtualenv

        sudo apt-get build-dep python-psycopg2

3. Set up Postgresql

   Create a user for Django

        sudo -u postgres createuser --createdb --no-superuser --no-createrole --pwprompt django

   Create a database for the digops application

        sudo -u postgres createdb -O django digops

4. Install git

        sudo apt-get install git-core


- - -

**Part II - Setting up the project environment**

1. Install virtualenv

        sudo apt-get install python-setuptools
        sudo easy_install virtualenv

2. Create directory for your projects (replace DIGOPS-HOME with your root directory)

        mkdir /DIGOPS-HOME
        cd /DISOPS-HOME

3. Clone the git repository using one of the following commands 

        (GW staff only)
        git clone git@github.com:gwu-libraries/DigOp.git

        (everyone else)
        git clone https://github.com/gwu-libraries/DigOp.git

4. cd into digop directory

        cd /DIGOPS-HOME/DigOp

5. Create virtual python environment using following command 

        virtualenv --no-site-packages ENV
        
6. Activate the virtual environemnt using the following command

        source ENV/bin/activate

7. Install the additional required packages

        pip install -r requirements.txt


- - -

**Part III - Configuring installation**

1. Configure database and other settings in a local_settings file

        cd DigOp
        cp local_settings.py.template local_settings.py
        vim local_settings.py

2. Fill in the values for Database in local_settings.py for the database, NAME, USER, and PASSWORD to the database you created above, and set ENGINE to 'postgresql_psycopg2' 

3. Fill in the values for the following fields required for making API calls to Inventory service in local_settings.py:

        INV_API_KEY = ""
        INV_USER = ""
        INV_URL = ""

4. Fill in the values for the test user required for running tests:

        TEST_USER = ""
        TEST_USER_PWD = ""

5. Fill in the values for Django LDAP Authentication

        AUTH_LDAP_SERVER_URI = ""
        AUTH_LDAP_BIND_DN = ""
        AUTH_LDAP_BIND_PASSWORD = ""
        AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
        LDAPSearch("", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
        )


6. Edit wsgi file

        cp DigOp/wsgi.py.template DigOp/wsgi.py
        vim DigOp/wsgi.py

7. Use the following command in shell to set the loacale

        sudo dpkg-reconfigure locales
        export LC_ALL=en_GB.UTF-8
        export LANG=en_GB.UTF-8

8. Go into the DIGOPS-HOME directory where manage.py is stored and type in the following command. DO NOT create a superuser when prompted!

        python manage.py syncdb

9. Migrate the database to the latest updates

        python manage.py migrate

10. Create the database super user

        python manage.py createsuperuser

11. At this point, you should be able to run the app and view it working, even without apache configured. This might be sufficient for dev/test.

        python manage.py runserver 0.0.0.0:8080
        (visit http://your-server:8080 to test)

12. If you want to use apache, add apache config file to sites-enabled and edit it

        sudo cp ../apache/DigOp /etc/apache2/sites-available/DigOp
        vim /etc/apache2/sites-available/DigOp

13. Enable the app in apache and bounce apache2 to start it up

        sudo a2ensite DigOp
        sudo /etc/init.d/apache2 restart

14. open a web browser and type in the url of the server running DigOps app. Type in the admin user and password created in step 13 to login.

15. If you get the Access Forbidden error, Make sure that the folder containing DIGOPS-HOME allows read and execute permissions to everyone. Typically, this might require giving 755 with chmod to your home directory if DIGOPS-HOME resides in your home directory.

