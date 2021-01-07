--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

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
-- Data for Name: models; Type: TABLE DATA; Schema: triagedata; Owner: admin
--

INSERT INTO triagedata.models (id, data, clinic_id, accuracy, created, in_use) VALUES (1, '\x736f6d65206d6f64656c', 1, 0.95, '2021-01-07', true);
INSERT INTO triagedata.models (id, data, clinic_id, accuracy, created, in_use) VALUES (2, '\x736f6d65206d6f64656c2032', 1, 0.92, '2021-01-07', false);
INSERT INTO triagedata.models (id, data, clinic_id, accuracy, created, in_use) VALUES (3, '\x736f6d65206d6f64656c2030', 1, 0.6, '2021-01-07', false);

--
-- PostgreSQL database dump complete
--

