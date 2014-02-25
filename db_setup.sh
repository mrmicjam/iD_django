sudo su - postgres -c "createdb id_django"
sudo su - postgres -c "createlang -d id_django plpgsql"
sudo su - postgres -c "psql -d id_django -f /usr/share/postgresql/*/contrib/*/postgis.sql"
sudo su - postgres -c "psql -d id_django -f /usr/share/postgresql/*/contrib/*/spatial_ref_sys.sql"
sudo su - postgres -c "createuser -s id_django"
sudo su - postgres -c "psql -d id_django -c \"ALTER ROLE id_django WITH PASSWORD 'id_django'\""

#sqlite
#https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/#create-spatialite-db
#need to compile and install pysqlite2 manually per instructions