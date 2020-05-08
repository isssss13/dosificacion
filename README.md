Requerimientos de software
python 3.5
Django 2.2

Instalar dependencias

Instalar mysqlclient

sudo apt-get install python3-dev
sudo apt-get install python-dev default-libmysqlclient-dev
pip install mysqlclient

**Instalar django
python3 -m pip install django

Instalar wsgi

pip install mod-wsgi
sudo apt-get install libapache2-mod-wsgi-py3

**Poner en produccion con Apache y wsgi**
** instalar apache 
sudo apt-get install apache2

** Instalar wsgi
sudo apt-get install libapache2-mod-wsgi-py3

** Instalar virtualenv
python3 -m pip install virtualenv

**crear entorno virtual
virtualenv nombredelentorno --python=python3

**clonar repositorio dentro de carpeta creada de env
git clone https://github.com/isssss13/dosificacion.git

configurar /etc/apache2/sites-available
si se va a utilizar para el servidor se configura de la siguiente manera en el archivo 000-config
*****************************************************************************************************
<VirtualHost *:80>
    Alias /static /home/server/env/dosificacion/dosificacion/static
    <Directory /home/server/env/dosificacion/dosificacion/static>
        Require all granted
    </Directory>

    <Directory /home/server/env/dosificacion/dosMetro>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess dosmetro python-path=/home/server/env:/home/server/env/lib/python3.6/site-packages
    WSGIProcessGroup dosmetro
    WSGIScriptAlias / /home/server/env/dosificacion/dosMetro/wsgi.py

    ServerAdmin webmaster@localhost
        
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>

****************************************************************************************************

**Configurar en wsgi la linea sys.path.append ingresar la direccion de la carpeta donde se aloga el sistema

**configurar settings.py la linea ALLOWED_HOSTS ingresando la direccion ip del servidor

**Reinicia apache
sudo systemctl restart apache2

**Crear migraciones**
python3 manage.py makemigrations dosificacion
python3 manage.py migrate

**Crear superusuario**
python3 manage.py createsuperuser
