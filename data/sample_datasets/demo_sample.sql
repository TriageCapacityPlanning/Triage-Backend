-------------------------------------------------------------------------------
--  Schema creation
-------------------------------------------------------------------------------

DROP SCHEMA IF EXISTS TriageData CASCADE;
CREATE SCHEMA IF NOT EXISTS TriageData;

-------------------------------------------------------------------------------
--  Create all necessary tables
-------------------------------------------------------------------------------


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
    CONSTRAINT pk PRIMARY KEY (clinic_id, severity),
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
            REFERENCES TriageData.Clinic(id)
);
CREATE TABLE TriageData.Models (
    id          SERIAL PRIMARY KEY,
    file_path   varchar,
    clinic_id   integer,
    severity    integer,
    accuracy    float,
    created     DATE NOT NULL DEFAULT CURRENT_DATE,
    in_use      boolean,
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id),
    CONSTRAINT fk_triage_class
        FOREIGN KEY(clinic_id, severity)
            REFERENCES TriageData.TriageClasses(clinic_id, severity)
);
CREATE TABLE TriageData.Schedules (
    id          SERIAL PRIMARY KEY,
    data        varchar,
    clinic_id   integer,
    CONSTRAINT fk_clinic
        FOREIGN KEY(clinic_id)
            REFERENCES TriageData.Clinic(id)
);

-------------------------------------------------------------------------------
--  Create required indexes on various attributes
-------------------------------------------------------------------------------

CREATE INDEX username_idx ON TriageData.Users (username);
CREATE INDEX clinic_schedule_idx ON TriageData.Schedules (clinic_id);
CREATE INDEX clinic_models_idx ON TriageData.Models (clinic_id);
CREATE INDEX clinic_triage_classes_idx ON TriageData.TriageClasses (clinic_id);

-------------------------------------------------------------------------------
--  User Roles to limit API access for various endpoints.
-------------------------------------------------------------------------------

DROP USER IF EXISTS triage_class_handler;
CREATE USER triage_class_handler WITH
    PASSWORD 'password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1;
GRANT INSERT, SELECT, UPDATE ON TriageData.TriageClasses TO triage_class_handler;

DROP USER IF EXISTS model_handler;
CREATE USER model_handler WITH
    PASSWORD 'password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1;
GRANT INSERT, SELECT, UPDATE ON TriageData.Models TO model_handler;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA TriageData TO model_handler;

DROP USER IF EXISTS predict_handler;
CREATE USER predict_handler WITH
    PASSWORD 'password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1;
GRANT SELECT ON TriageData.TriageClasses TO predict_handler;

DROP USER IF EXISTS historic_data_handler;
CREATE USER historic_data_handler WITH
    PASSWORD 'password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1;
GRANT INSERT, DELETE ON TriageData.HistoricData TO historic_data_handler;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA TriageData TO historic_data_handler;

DROP USER IF EXISTS triage_controller;
CREATE USER triage_controller WITH
    PASSWORD 'password'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1;
GRANT SELECT ON TriageData.HistoricData TO triage_controller;

CREATE GROUP api_handlers;
ALTER GROUP api_handlers ADD USER triage_class_handler, model_handler, predict_handler, historic_data_handler, triage_controller;
GRANT USAGE ON SCHEMA TriageData TO GROUP api_handlers;


--
-- Data for Name: clinic; Type: TABLE DATA; Schema: triagedata; Owner: admin
--

INSERT INTO triagedata.clinic (id, name) VALUES (1, 'Test Clinic 1');
INSERT INTO triagedata.clinic (id, name) VALUES (2, 'Capstone Clinic');
INSERT INTO triagedata.clinic (id, name) VALUES (3, 'Clinic A');
INSERT INTO triagedata.clinic (id, name) VALUES (4, 'Clinic B');
INSERT INTO triagedata.clinic (id, name) VALUES (5, 'Clinic C');

--
-- Data for Name: triageclasses; Type: TABLE DATA; Schema: triagedata; Owner: admin
--

INSERT INTO triagedata.triageclasses (clinic_id, severity, name, duration, proportion) VALUES (1, 1, 'Urgent', 2, 0.95);
INSERT INTO triagedata.triageclasses (clinic_id, severity, name, duration, proportion) VALUES (1, 2, 'Semi-Urgent', 12, 0.8);
INSERT INTO triagedata.triageclasses (clinic_id, severity, name, duration, proportion) VALUES (1, 3, 'Standard', 23, 0.6);
INSERT INTO triagedata.triageclasses (clinic_id, severity, name, duration, proportion) VALUES (1, 4, 'Low-Urgency', 52, 0.5);


--
-- Data for Name: historicdata; Type: TABLE DATA; Schema: triagedata; Owner: admin
--

INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-01', '2019-01-14');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-02', '2019-01-15');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-03', '2019-01-16');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-04', '2019-01-17');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-05', '2019-01-18');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-06', '2019-01-19');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-07', '2019-01-20');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-08', '2019-01-21');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-09', '2019-01-22');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-10', '2019-01-23');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-11', '2019-01-24');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-12', '2019-01-25');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-13', '2019-01-26');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-14', '2019-01-27');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-15', '2019-01-28');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-16', '2019-01-29');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-17', '2019-01-30');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-18', '2019-01-31');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-19', '2019-02-01');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-20', '2019-02-02');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-21', '2019-02-03');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-22', '2019-02-04');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-23', '2019-02-05');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-24', '2019-02-06');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-25', '2019-02-07');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-26', '2019-02-08');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-27', '2019-02-09');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-28', '2019-02-10');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-29', '2019-02-11');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-30', '2019-02-12');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-01-31', '2019-02-13');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-01', '2019-02-14');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-02', '2019-02-15');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-03', '2019-02-16');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-04', '2019-02-17');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-05', '2019-02-18');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-06', '2019-02-19');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-07', '2019-02-20');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-08', '2019-02-21');
INSERT INTO triagedata.historicdata (clinic_id, severity, date_received, date_seen) VALUES (1, 1, '2019-02-09', '2019-02-22');
