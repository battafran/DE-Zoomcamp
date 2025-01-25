services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: ny_taxi
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    restart: always




#Iniciar contenedor de Docker para postgre:
    
docker run -it ^
  -e POSTGRES_USER="root" ^
  -e POSTGRES_PASSWORD="root" ^
  -e POSTGRES_DB="ny_taxi" ^
  -v "C:/Users/Fran/Desktop/Zoomcamp/Week_1/02-docker-SQL/vol-pgdatabase:/var/lib/postgresql/data:rw" ^
  -p 5432:5432 ^
  --network pg-network ^
  --name pgdatabase ^
  postgres:postgres:13

#Para trabajar con postgre usamos PGCLI
#pip install pgcli

#Conectar a la base de datos:
#pgcli -h localhost -p 5432 -u root -d ny_taxi

#Correr Jupyter notebook para cargar y manejar el dataset con python
#jupyter notebook

#Librería de pandas para usar SQL
#pip install sqlalchemy

#Para obtener imagen del contenedor de pgadmin (toolkit para el manejo de base de datos)
#docker pull dpage/pgadmin4

#Para correr el contenedor:
#docker run -it ^
#  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" ^
#  -e PGADMIN_DEFAULT_PASSWORD="root" ^
#  -p 8080:80 ^
#   --network pg-network ^
#   --name pgadmin ^
#  dpage/pgadmin4

#Una vez que corre se puede entrar a localhost:8080

#Para poder linkear ambos contenedores (postgre y pgadmin)
#Necesito meterlos en una red (--network pg-network)

#Ejecuto el ingest_data.py para testearlo

#python ingest_data.py ^
#  --user=root ^
#  --password=root ^
#  --host=localhost ^
#  --port=5432 ^
#  --db=ny_taxi ^
#  --table_name=yellow_taxi_trips ^
#  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

#Crea una imagen Docker a partir del Dockerfile
docker build -t taxi_ingest:v001 .

#Inicio el contenedor a partir de esta imagen

docker run -it ^
  --network pg-network ^
  taxi_ingest:v001 ^
    --user=root ^
    --password=root ^
    --host=pgdatabase ^
    --port=5432 ^
    --db=ny_taxi ^
    --table_name=yellow_taxi_trips ^
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"


git rm --cached yellow_tripdata_2021-01.csv
git rm --cached yellow_tripdata_2021-01.csv.gz