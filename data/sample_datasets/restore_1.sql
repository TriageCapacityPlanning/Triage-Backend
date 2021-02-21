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

--
-- PostgreSQL database dump complete
--

