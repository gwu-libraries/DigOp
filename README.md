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

        sudo apt-get install apache2 python-dev mysql-server mysql-client python-setuptools libapache2-mod-wsgi python-mysqldb libmysqlclient15-dev 

2. Install git

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

1. Login to mysql

        mysql -u root -p

2. Create the Database
        
        create Database Production;

3. Create Database user while changing user with a different username and pass with a different password
        
        CREATE USER 'user'@'localhost' IDENTIFIED BY 'pass';

4. Assign the privileges to user

        GRANT ALTER,CREATE,SELECT,INSERT,UPDATE,DELETE,INDEX ON Production.* TO 'user1'@'localhost';

5. Commit the changes

        FLUSH PRIVILEGES;

6. Configure database and other settings in a local_settings file

        cd DigOp
        cp local_settings.py.template local_settings.py
        vim local_settings.py

7. Fill in the values for Database in local_settings.py as follows:

        DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'Production',
                    'HOST': 'localhost',
                    'USER': '',
                    'PASSWORD': '',
                    'PORT': 3306,
                    }
                }

8. Fill in the values for the following fields required for making API calls to Inventory service in local_settings.py:

        INV_API_KEY = ""
        INV_USER = ""
        INV_URL = ""

9. Fill in the values for the test user required for running tests:

        TEST_USER = ""
        TEST_USER_PWD = ""

10. Edit wsgi file

        cp DigOp/wsgi.py.template DigOp/wsgi.py
        vim DigOp/wsgi.py

11. Use the following command in shell to set the loacale

        sudo dpkg-reconfigure locales
        export LC_ALL=en_GB.UTF-8
        export LANG=en_GB.UTF-8

12. Go into the DIGOPS-HOME directory where manage.py is stored and type in the following command

        python manage.py syncdb

13. At this point, you should be able to run the app and view it working, even without apache configured. This might be sufficient for dev/test.

        python manage.py runserver 0.0.0.0:8080
        (visit http://your-server:8080 to test)


14. If you want to use apache, add apache config file to sites-enabled and edit it

        sudo cp ../apache/DigOp /etc/apache2/sites-available/DigOp
        vim /etc/apache2/sites-available/DigOp

15. Enable the app in apache and bounce apache2 to start it up

        sudo a2ensite DigOp
        sudo /etc/init.d/apache2 restart

16. open a web browser and type in the url of the server running DigOps app. Type in the admin user and password created in step 13 to login.

17. If you get the Access Forbidden error, Make sure that the folder containing DIGOPS-HOME allows read and execute permissions to everyone. Typically, this might require giving 755 with chmod to your home directory if DIGOPS-HOME resides in your home directory.

