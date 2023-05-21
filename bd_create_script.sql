DROP TABLE IF EXISTS musicians, roles, types_of_ensemble, albums, musical_instruments, ensembles, musicians_and_ensembles, musical_works, recordings, instruments_of_the_performer_of_a_musical_work;

CREATE TABLE musicians (
    musician_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE roles (
    role_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE types_of_ensemble (
    type_of_ensemble_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE albums (
    album_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE musical_instruments (
    musical_instrument_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE ensembles (
    ensemble_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type_of_ensemble INT,
    CONSTRAINT fk_type_of_ensemble FOREIGN KEY (type_of_ensemble) REFERENCES types_of_ensemble (type_of_ensemble_id)
);

CREATE TABLE musicians_and_ensembles (
    musicians_and_ensembles_id serial PRIMARY KEY,
    musician INT,
    ensemble INT,
    role INT,
    CONSTRAINT fk_musician FOREIGN KEY (musician) REFERENCES musicians (musician_id),
    CONSTRAINT fk_ensemble FOREIGN KEY (ensemble) REFERENCES ensembles (ensemble_id),
    CONSTRAINT fk_role FOREIGN KEY (role) REFERENCES roles (role_id)
);

CREATE TABLE musical_works (
    musical_work_id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    author INT,
    CONSTRAINT fk_author FOREIGN KEY (author) REFERENCES musicians (musician_id)
);

CREATE TABLE recordings (
    recording_id serial PRIMARY KEY,
    musical_work INT,
    ensemble INT,
    album INT,
    CONSTRAINT fk_musical_work FOREIGN KEY (musical_work) REFERENCES musical_works (musical_work_id),
    CONSTRAINT fk_ensemble FOREIGN KEY (ensemble) REFERENCES ensembles (ensemble_id),
    CONSTRAINT fk_album FOREIGN KEY (album) REFERENCES albums (album_id)
);

CREATE TABLE instruments_of_the_performer_of_a_musical_work (
    instrument_of_the_performer_of_a_musical_work_id serial PRIMARY KEY,
    musician INT,
    musical_work INT,
    musical_instrument INT,
    CONSTRAINT fk_musician FOREIGN KEY (musician) REFERENCES musicians (musician_id),
    CONSTRAINT fk_musical_work FOREIGN KEY (musical_work) REFERENCES musical_works (musical_work_id),
    CONSTRAINT fk_musical_instrument FOREIGN KEY (musical_instrument) REFERENCES musical_instruments (musical_instrument_id)
);