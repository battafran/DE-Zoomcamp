import argparse
import pandas as pd
import os
from sqlalchemy import create_engine
from time import time
import requests

def download_file(url, output_file):
    """
    Descarga un archivo desde una URL y lo guarda con el nombre especificado.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Archivo descargado exitosamente: {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        exit(1)


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Nombre del archivo CSV a guardar
    csv_name = url.split('/')[-1]

    # Descargar el archivo CSV
    download_file(url, csv_name)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df=next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Insertar los siguientes chunks
    while True:
        try:
            t_start = time()
            df = next(df_iter)

            # Convertir columnas de datetime
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # Insertar datos en la tabla
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            print('Inserted another chunk..., took %.3f second' % (t_end - t_start))
        except StopIteration:
            print("All data inserted.")
            break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        description='Ingest CSV data to postgres',
                        )
   
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='pass for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table where we will write the results')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)