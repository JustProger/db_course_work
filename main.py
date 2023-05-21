import psycopg2
from psycopg2 import Error
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from faker import Faker
from faker.providers import DynamicProvider

import time
import os.path
from config import user, password, host, port, database
from db_cw_create import db_cw_create

start_time = time.time()


def create_provider_and_upload_data(provider_name: str, path: str, cursor):
    '''
        provider_name - название нового провайдера faker
        path - путь до файла .txt с данными для добавления в таблицу (название файла - название соответствующей таблицы)
        cur - объект типа psycopg2.cursor (для выполнения SQL команд на бд)
    '''

    # массив для хранения строк файла
    # path - путь до файла .txt
    table_name = os.path.basename(os.path.splitext(path)[0])
    temp = []

    if (table_name == 'ensembles'):
        with open(path, 'r') as f:
            while (tstr := f.readline()):
                processed_tstr = '. '.join((tstr.split('\n')[0].split('. '))[1:])
                cursor.execute('''SELECT type_of_ensemble_id FROM types_of_ensemble WHERE name = %s LIMIT 1;''', (fake.type_of_ensemble(),))
                random_type_of_ensemble_id = int(cursor.fetchone()[0])
                cursor.execute('''INSERT INTO ensembles (name, type_of_ensemble) VALUES (%s, %s);
                            ''', (processed_tstr, random_type_of_ensemble_id))
                temp.append(processed_tstr)

    elif (table_name == 'musical_works'):
        with open(path, 'r') as f:
            while (tstr := f.readline()):
                processed_tstr = '. '.join((tstr.split('\n')[0].split('. '))[1:])
                cursor.execute('''SELECT musician_id FROM musicians WHERE name = %s LIMIT 1;''', (fake.musician(),))
                random_musician_id = int(cursor.fetchone()[0])
                cursor.execute('''INSERT INTO musical_works (name, author) VALUES (%s, %s);
                            ''', (processed_tstr, random_musician_id))
                temp.append(processed_tstr)

    else:
        with open(path, 'r') as f:
            while (tstr := f.readline()):
                processed_tstr = '. '.join((tstr.split('\n')[0].split('. '))[1:])
                cursor.execute(sql.SQL('''INSERT INTO {table} (name) VALUES (%s);
                            ''').format(table=sql.Identifier(table_name)), (processed_tstr,))
                temp.append(processed_tstr)

    return DynamicProvider(provider_name=provider_name, elements=temp)


if (__name__ == '__main__'):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            user=user,
            # пароль, который указали при установке PostgreSQL
            password=password,
            host=host,
            port=port,
            database=database)

        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Курсор для выполнения операций с базой данных
        with connection.cursor() as cursor:

            # Создаём таблицы БД по заранее составленному SQL скрипту
            db_cw_create(cursor)

            # Загрузка данных в некоторые таблицы бд и создание провайдеров для работы модуля faker
            fake = Faker()
            fake.add_provider(create_provider_and_upload_data('album', 'data/albums.txt', cursor))
            fake.add_provider(create_provider_and_upload_data('type_of_ensemble', 'data/types_of_ensemble.txt', cursor))
            fake.add_provider(create_provider_and_upload_data('musical_instrument', 'data/musical_instruments.txt', cursor))
            fake.add_provider(create_provider_and_upload_data('musician', 'data/musicians.txt', cursor))
            fake.add_provider(create_provider_and_upload_data('role', 'data/roles.txt', cursor))
            # Эти провайдерам при создании используют некоторые провайдеры выше (нужно , чтобы он уже были созданы, поэтому провайдеры musical_work и ensemble создаём в последнюю очередь)
            fake.add_provider(create_provider_and_upload_data('musical_work', 'data/musical_works.txt', cursor))
            fake.add_provider(create_provider_and_upload_data('ensemble', 'data/ensembles.txt', cursor))

            # Заполнение оставшихся 3х таблиц: musicians_and_ensembles, Recordings, Instruments_of_the_performer_of_a_musical_work

            # Добавляем 15 рандомно сгенерированных записей в таблицу musicians_and_ensembles
            for i in range(15):
                cursor.execute('''
                    SELECT musician_id FROM musicians WHERE name = %s;
                ''', (fake.musician(),))
                # id случайной записи из таблицы musicians
                random_musician_id = int(cursor.fetchone()[0])

                cursor.execute('''
                    SELECT ensemble_id FROM ensembles WHERE name = %s;
                ''', (fake.ensemble(),))
                # id случайной записи из таблицы ensembles
                random_ensemble_id = int(cursor.fetchone()[0])

                cursor.execute('''
                    SELECT role_id FROM roles WHERE name = %s;
                ''', (fake.role(),))
                # id случайной записи из таблицы roles
                random_role_id = int(cursor.fetchone()[0])

                # добавляем запись в таблицу musicians_and_ensembles
                cursor.execute('''
                    INSERT INTO musicians_and_ensembles (musician, ensemble, role) VALUES (%s, %s, %s);
                ''', (random_musician_id, random_ensemble_id, random_role_id))

            # Добавляем 15 рандомно сгенерированных записей в таблицу instruments_of_the_performer_of_a_musical_work
            for i in range(15):
                cursor.execute('''
                    SELECT musician_id FROM musicians WHERE name = %s;
                ''', (fake.musician(),))
                # id случайной записи из таблицы musicians
                random_musician_id = int(cursor.fetchone()[0])

                cursor.execute('''
                    SELECT musical_work_id FROM musical_works WHERE name = %s;
                ''', (fake.musical_work(),))
                # id случайной записи из таблицы musical_works
                random_musical_work_id = int(cursor.fetchone()[0])

                cursor.execute('''
                    SELECT musical_instrument_id FROM musical_instruments WHERE name = %s;
                ''', (fake.musical_instrument(),))
                # id случайной записи из таблицы musical_instruments
                random_musical_instrument_id = int(cursor.fetchone()[0])

                # добавляем запись в таблицу instruments_of_the_performer_of_a_musical_work
                cursor.execute('''
                    INSERT INTO instruments_of_the_performer_of_a_musical_work (musician, musical_work, musical_instrument) VALUES (%s, %s, %s);
                ''', (random_musician_id, random_musical_work_id, random_musical_instrument_id))

            # Добавляем 100000 рандомно сгенерированных записей в таблицу recordings
            for i in range(100000):
                cursor.execute('''
                    SELECT musical_work_id FROM musical_works WHERE name = %s;
                ''', (fake.musical_work(),))
                # id случайной записи из таблицы musical_works
                random_musical_work_id = int(cursor.fetchone()[0])

                cursor.execute('''
                    SELECT ensemble_id FROM ensembles WHERE name = %s;
                ''', (fake.ensemble(),))
                # id случайной записи из таблицы ensembles
                random_ensemble_id = int(cursor.fetchone()[0])

                cursor.execute('''
                    SELECT album_id FROM albums WHERE name = %s;
                ''', (fake.album(),))
                # id случайной записи из таблицы albums
                random_album_id = int(cursor.fetchone()[0])

                # добавляем запись в таблицу recordings
                cursor.execute('''
                    INSERT INTO recordings (musical_work, ensemble, album) VALUES (%s, %s, %s);
                ''', (random_musical_work_id, random_ensemble_id, random_album_id))

            # querySelect_musicians_and_ensembles = '''SELECT * FROM recordings, musical_works, ensembles, albums WHERE
            #                                         recordings.musical_work = musical_works.musical_work_id
            #                                         AND recordings.ensemble = ensembles.ensemble_id
            #                                         AND recordings.album = albums.album_id;'''
            # cursor.execute(querySelect_musicians_and_ensembles)
            # output_data = cursor.fetchall()
            # print('SQL command:', querySelect_musicians_and_ensembles)
            # for tstr in output_data:
            #     print(*tstr)
            # print('End of output.')

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.close()
            print("-------------------------------")
            print("Соединение с PostgreSQL закрыто")

    print("--- %s seconds ---" % (time.time() - start_time))
