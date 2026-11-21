CREATE SCHEMA IF NOT EXISTS stg;

CREATE TABLE IF NOT EXISTS stg.population (
    country_code text     NOT NULL CHECK (country_code ~ '^[A-Z]{3}$'),
    year         smallint NOT NULL CHECK (year >= 1960),
    country_name text     NOT NULL CHECK (btrim(country_name) <> ''),
    population   bigint   NOT NULL CHECK (population >= 0),
    PRIMARY KEY (country_code, year)
);
