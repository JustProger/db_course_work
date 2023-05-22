def print_sql_query_result(query, cursor):
    cursor.execute(query)
    output_data = cursor.fetchall()
    print('SQL command:', query)
    for tstr in output_data:
        print(*tstr)
    print('End of output.')


def main(cursor):
    querySelect_musicians_and_ensembles = '''SELECT * FROM recordings, musical_works, ensembles, albums WHERE
                                                        recordings.musical_work = musical_works.musical_work_id
                                                        AND recordings.ensemble = ensembles.ensemble_id
                                                        AND recordings.album = albums.album_id;'''
    print_sql_query_result(querySelect_musicians_and_ensembles, cursor)