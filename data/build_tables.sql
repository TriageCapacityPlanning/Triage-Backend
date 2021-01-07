DROP SCHEMA IF EXISTS TriageData CASCADE;
CREATE SCHEMA IF NOT EXISTS TriageData;
CREATE TABLE TriageData.Clinic (
    id          SERIAL PRIMARY KEY,
    name        varchar(255) NOT NULL
);
CREATE TABLE TriageData.Users (
    username    varchar(40) PRIMARY KEY,
    password    varchar,
    salt        varchar,
    clinic_id   integer,
    admin       boolean,
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id)
);
CREATE TABLE TriageData.TriageClasses (
    clinic_id   integer,
    severity    integer,
    name        varchar(255),
    duration    integer,
    proportion  float,
    PRIMARY KEY (clinic_id, severity)
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id)
);
CREATE TABLE TriageData.HistoricData (
    id              SERIAL PRIMARY KEY,
    clinic_id       integer,
    severity        integer,
    date_received   DATE,
    date_seen       DATE,
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id),
    CONSTRAINT fk_triage_classes
        FOREIGN KEY(clinic_id, severity)
            REFERENCES TriageData.TriageClasses(clinic_id, severity)
);
CREATE TABLE TriageData.Models (
    id          SERIAL PRIMARY KEY,
    data        bytea,
    clinic_id   integer,
    accuracy    float,
    created     DATE NOT NULL DEFAULT CURRENT_DATE,
    in_use      boolean,
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id)
);
CREATE TABLE TriageData.Schedules (
    id          SERIAL PRIMARY KEY,
    data        varchar,
    clinic_id   integer,
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id)
);
CREATE INDEX username_idx ON TriageData.Users (username);
CREATE INDEX clinic_schedule_idx ON TriageData.Schedules (clinic_id);
CREATE INDEX clinic_models_idx ON TriageData.Models (clinic_id);
CREATE INDEX clinic_triage_classes_idx ON TriageData.TriageClasses (clinic_id);