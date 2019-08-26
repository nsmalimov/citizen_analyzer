CREATE TYPE GENDER_TYPE AS ENUM ('male', 'female');

CREATE TABLE IF NOT EXISTS imports_data
(
    id           SERIAL PRIMARY KEY,
    import_id    TEXT        NOT NULL,
    citizen_id   INT         NOT NULL,
    town         TEXT        NOT NULL,
    street       TEXT        NOT NULL,
    building     TEXT        NOT NULL,
    apartment    INT         NOT NULL,
    citizen_name TEXT        NOT NULL,
    birth_date   DATE        NOT NULL,
    gender       GENDER_TYPE NOT NULL,
    relatives    INT[]       NOT NULL
);

