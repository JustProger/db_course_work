def fill_in_musicians_and_ensembles(num, cursor, fake):
    # Добавляем num рандомно сгенерированных записей в таблицу musicians_and_ensembles
    for i in range(num):
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


def fill_in_recordings(num, cursor, fake):
    # Добавляем num рандомно сгенерированных записей в таблицу recordings
    for i in range(num):
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


def fill_in_instruments_of_the_performer_of_a_musical_work(num, cursor, fake):
    # Добавляем num рандомно сгенерированных записей в таблицу instruments_of_the_performer_of_a_musical_work
    for i in range(num):
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