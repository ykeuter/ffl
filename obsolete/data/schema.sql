--
-- PostgreSQL database dump
--

-- Dumped from database version 9.3.13
-- Dumped by pg_dump version 9.3.13
-- Started on 2016-08-18 18:23:43 CEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 1 (class 3079 OID 11789)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2011 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_with_oids = false;

--
-- TOC entry 174 (class 1259 OID 16420)
-- Name: game; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE game (
    id integer NOT NULL,
    home_team_id integer,
    season_week integer,
    visiting_team_id integer
);


--
-- TOC entry 173 (class 1259 OID 16416)
-- Name: game_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE game_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2012 (class 0 OID 0)
-- Dependencies: 173
-- Name: game_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE game_id_seq OWNED BY game.id;


--
-- TOC entry 176 (class 1259 OID 16455)
-- Name: player; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE player (
    id integer NOT NULL,
    player_name character varying,
    team_id integer,
    projected_points real,
    position_id integer
);


--
-- TOC entry 175 (class 1259 OID 16453)
-- Name: player_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE player_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2013 (class 0 OID 0)
-- Dependencies: 175
-- Name: player_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE player_id_seq OWNED BY player.id;


--
-- TOC entry 178 (class 1259 OID 16471)
-- Name: position; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "position" (
    id integer NOT NULL,
    position_name character varying
);


--
-- TOC entry 177 (class 1259 OID 16469)
-- Name: position_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE position_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2014 (class 0 OID 0)
-- Dependencies: 177
-- Name: position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE position_id_seq OWNED BY "position".id;


--
-- TOC entry 172 (class 1259 OID 16407)
-- Name: team; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE team (
    id integer NOT NULL,
    team_name character varying,
    bye_week integer,
    projected_defense_points real
);


--
-- TOC entry 171 (class 1259 OID 16405)
-- Name: team_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 2015 (class 0 OID 0)
-- Dependencies: 171
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE team_id_seq OWNED BY team.id;


--
-- TOC entry 1883 (class 2604 OID 16423)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY game ALTER COLUMN id SET DEFAULT nextval('game_id_seq'::regclass);


--
-- TOC entry 1884 (class 2604 OID 16458)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY player ALTER COLUMN id SET DEFAULT nextval('player_id_seq'::regclass);


--
-- TOC entry 1885 (class 2604 OID 16474)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "position" ALTER COLUMN id SET DEFAULT nextval('position_id_seq'::regclass);


--
-- TOC entry 1882 (class 2604 OID 16410)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY team ALTER COLUMN id SET DEFAULT nextval('team_id_seq'::regclass);


--
-- TOC entry 1889 (class 2606 OID 16426)
-- Name: game_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY game
    ADD CONSTRAINT game_pkey PRIMARY KEY (id);


--
-- TOC entry 1891 (class 2606 OID 16463)
-- Name: player_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_pkey PRIMARY KEY (id);


--
-- TOC entry 1893 (class 2606 OID 16479)
-- Name: position_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "position"
    ADD CONSTRAINT position_pkey PRIMARY KEY (id);


--
-- TOC entry 1887 (class 2606 OID 16415)
-- Name: team_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- TOC entry 1894 (class 2606 OID 16427)
-- Name: game_home_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY game
    ADD CONSTRAINT game_home_team_id_fkey FOREIGN KEY (home_team_id) REFERENCES team(id);


--
-- TOC entry 1895 (class 2606 OID 16486)
-- Name: game_visiting_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY game
    ADD CONSTRAINT game_visiting_team_id_fkey FOREIGN KEY (visiting_team_id) REFERENCES team(id);


--
-- TOC entry 1897 (class 2606 OID 16480)
-- Name: player_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_position_id_fkey FOREIGN KEY (position_id) REFERENCES "position"(id);


--
-- TOC entry 1896 (class 2606 OID 16464)
-- Name: player_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY player
    ADD CONSTRAINT player_team_id_fkey FOREIGN KEY (team_id) REFERENCES team(id);


-- Completed on 2016-08-18 18:23:43 CEST

--
-- PostgreSQL database dump complete
--

