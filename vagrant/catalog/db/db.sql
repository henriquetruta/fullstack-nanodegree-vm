--
-- PostgreSQL database creation
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

INSERT INTO category (name) VALUES
('Football'),
('Basketball'),
('Baseball'),
('Frisbee'),
('Snowboarding'),
('Rock Climbing'),
('Foosball'),
('Skating'),
('Hockey');