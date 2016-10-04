--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: hstore; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;


--
-- Name: EXTENSION hstore; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hstore IS 'data type for storing sets of (key, value) pairs';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: chat; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE chat (
    id integer NOT NULL,
    user_from integer NOT NULL,
    user_to integer NOT NULL
);


ALTER TABLE public.chat OWNER TO bot;

--
-- Name: chat_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.chat_id_seq OWNER TO bot;

--
-- Name: chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE chat_id_seq OWNED BY chat.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    data bytea,
    text text,
    chat_id integer NOT NULL
);


ALTER TABLE public.message OWNER TO bot;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO bot;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE message_id_seq OWNED BY message.id;


--
-- Name: request; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE request (
    id integer NOT NULL,
    type_id integer NOT NULL,
    text text,
    state_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.request OWNER TO bot;

--
-- Name: request_chat_through; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE request_chat_through (
    id integer NOT NULL,
    request_id integer NOT NULL,
    chat_id integer NOT NULL
);


ALTER TABLE public.request_chat_through OWNER TO bot;

--
-- Name: request_chat_through_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE request_chat_through_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.request_chat_through_id_seq OWNER TO bot;

--
-- Name: request_chat_through_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE request_chat_through_id_seq OWNED BY request_chat_through.id;


--
-- Name: request_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.request_id_seq OWNER TO bot;

--
-- Name: request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE request_id_seq OWNED BY request.id;


--
-- Name: requestcomment; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE requestcomment (
    id integer NOT NULL,
    text text,
    rating real NOT NULL,
    date_start timestamp without time zone NOT NULL,
    date_finished timestamp without time zone NOT NULL
);


ALTER TABLE public.requestcomment OWNER TO bot;

--
-- Name: requestcomment_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE requestcomment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requestcomment_id_seq OWNER TO bot;

--
-- Name: requestcomment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE requestcomment_id_seq OWNED BY requestcomment.id;


--
-- Name: requeststate; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE requeststate (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.requeststate OWNER TO bot;

--
-- Name: requeststate_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE requeststate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requeststate_id_seq OWNER TO bot;

--
-- Name: requeststate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE requeststate_id_seq OWNED BY requeststate.id;


--
-- Name: section; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE section (
    id integer NOT NULL,
    name text NOT NULL,
    parent_section_id integer,
    click_count integer NOT NULL
);


ALTER TABLE public.section OWNER TO bot;

--
-- Name: section_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.section_id_seq OWNER TO bot;

--
-- Name: section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE section_id_seq OWNED BY section.id;


--
-- Name: stp; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE stp (
    id integer NOT NULL,
    staff_id integer,
    user_id integer NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.stp OWNER TO bot;

--
-- Name: stp_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE stp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stp_id_seq OWNER TO bot;

--
-- Name: stp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE stp_id_seq OWNED BY stp.id;


--
-- Name: stp_section_through; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE stp_section_through (
    id integer NOT NULL,
    stp_id integer NOT NULL,
    section_id integer NOT NULL
);


ALTER TABLE public.stp_section_through OWNER TO bot;

--
-- Name: stp_section_through_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE stp_section_through_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stp_section_through_id_seq OWNER TO bot;

--
-- Name: stp_section_through_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE stp_section_through_id_seq OWNED BY stp_section_through.id;


--
-- Name: stprequest; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE stprequest (
    id integer NOT NULL,
    request_id integer NOT NULL,
    stp_id integer NOT NULL,
    comment_id integer
);


ALTER TABLE public.stprequest OWNER TO bot;

--
-- Name: stprequest_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE stprequest_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stprequest_id_seq OWNER TO bot;

--
-- Name: stprequest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE stprequest_id_seq OWNED BY stprequest.id;


--
-- Name: type; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE type (
    id integer NOT NULL,
    name text NOT NULL,
    section_id integer,
    parent_type_id integer,
    click_count integer NOT NULL,
    comment_required boolean NOT NULL
);


ALTER TABLE public.type OWNER TO bot;

--
-- Name: type_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.type_id_seq OWNER TO bot;

--
-- Name: type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE type_id_seq OWNED BY type.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: bot; Tablespace: 
--

CREATE TABLE "user" (
    id integer NOT NULL,
    telegram_user_id integer NOT NULL,
    telegram_chat_id integer NOT NULL,
    username text,
    additional_data json,
    state text NOT NULL,
    phone text,
    is_active boolean NOT NULL
);


ALTER TABLE public."user" OWNER TO bot;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: bot
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO bot;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: bot
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY chat ALTER COLUMN id SET DEFAULT nextval('chat_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY message ALTER COLUMN id SET DEFAULT nextval('message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request ALTER COLUMN id SET DEFAULT nextval('request_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request_chat_through ALTER COLUMN id SET DEFAULT nextval('request_chat_through_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY requestcomment ALTER COLUMN id SET DEFAULT nextval('requestcomment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY requeststate ALTER COLUMN id SET DEFAULT nextval('requeststate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY section ALTER COLUMN id SET DEFAULT nextval('section_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stp ALTER COLUMN id SET DEFAULT nextval('stp_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stp_section_through ALTER COLUMN id SET DEFAULT nextval('stp_section_through_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stprequest ALTER COLUMN id SET DEFAULT nextval('stprequest_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY type ALTER COLUMN id SET DEFAULT nextval('type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: bot
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Data for Name: chat; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY chat (id, user_from, user_to) FROM stdin;
\.


--
-- Name: chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('chat_id_seq', 1, false);


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY message (id, user_id, data, text, chat_id) FROM stdin;
\.


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('message_id_seq', 1, false);


--
-- Data for Name: request; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY request (id, type_id, text, state_id, created_at, user_id) FROM stdin;
4	2		1	2016-10-04 13:34:12.556271	10
\.


--
-- Data for Name: request_chat_through; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY request_chat_through (id, request_id, chat_id) FROM stdin;
\.


--
-- Name: request_chat_through_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('request_chat_through_id_seq', 1, false);


--
-- Name: request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('request_id_seq', 4, true);


--
-- Data for Name: requestcomment; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY requestcomment (id, text, rating, date_start, date_finished) FROM stdin;
\.


--
-- Name: requestcomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('requestcomment_id_seq', 1, false);


--
-- Data for Name: requeststate; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY requeststate (id, name) FROM stdin;
1	создана
\.


--
-- Name: requeststate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('requeststate_id_seq', 1, true);


--
-- Data for Name: section; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY section (id, name, parent_section_id, click_count) FROM stdin;
3	Сотрудники	2	23
2	Магазин здесь вложенность	\N	25
6	Тест2	\N	1
4	Товары	2	0
5	Тест1	\N	0
7	Тест3	\N	0
8	Тест4	\N	0
9	Тест5	\N	0
10	Тест6	\N	0
11	Тест7	\N	0
12	Тест8	\N	0
13	Тест9	\N	0
14	Тест10	\N	0
15	Работа	2	0
16	Организация	2	0
17	Обслуживание	2	0
18	Тест11	2	0
19	Тест12	2	0
20	Тест13	2	0
21	Тест14	2	0
22	Тест15	2	0
23	Тест16	2	0
24	Тест17	2	0
25	Тест18	2	0
26	Тест19	25	0
1	ИМКЦ	\N	8
\.


--
-- Name: section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('section_id_seq', 26, true);


--
-- Data for Name: stp; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY stp (id, staff_id, user_id, is_active) FROM stdin;
\.


--
-- Name: stp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('stp_id_seq', 1, false);


--
-- Data for Name: stp_section_through; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY stp_section_through (id, stp_id, section_id) FROM stdin;
\.


--
-- Name: stp_section_through_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('stp_section_through_id_seq', 1, false);


--
-- Data for Name: stprequest; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY stprequest (id, request_id, stp_id, comment_id) FROM stdin;
\.


--
-- Name: stprequest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('stprequest_id_seq', 1, false);


--
-- Data for Name: type; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY type (id, name, section_id, parent_type_id, click_count, comment_required) FROM stdin;
16	Тест11	3	3	2	f
3	Тест1 здесь вложенность	3	\N	2	f
1	Другое	3	\N	3	t
2	Не покупается товар	3	\N	17	f
4	Тест2	3	\N	0	f
5	Тест3	3	\N	0	f
6	Тест4	3	\N	0	f
7	Тест5	3	\N	0	f
8	Тест6	3	\N	0	f
9	Тест7	3	\N	0	f
10	Тест8	3	\N	0	f
11	Тест9	3	\N	0	f
14	Тест12	3	\N	0	f
15	Тест13	3	\N	0	f
12	Тест10	3	\N	0	f
13	Тест11	3	\N	0	f
17	Тест12	3	3	0	f
18	Тест13	3	3	0	f
19	Тест14	3	3	0	f
20	Тест15	3	3	0	f
21	Тест16	3	3	0	f
\.


--
-- Name: type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('type_id_seq', 21, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: bot
--

COPY "user" (id, telegram_user_id, telegram_chat_id, username, additional_data, state, phone, is_active) FROM stdin;
10	150483027	150483027	demty	{}	main_menu	\N	t
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bot
--

SELECT pg_catalog.setval('user_id_seq', 10, true);


--
-- Name: chat_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY chat
    ADD CONSTRAINT chat_pkey PRIMARY KEY (id);


--
-- Name: message_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: request_chat_through_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY request_chat_through
    ADD CONSTRAINT request_chat_through_pkey PRIMARY KEY (id);


--
-- Name: request_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_pkey PRIMARY KEY (id);


--
-- Name: requestcomment_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY requestcomment
    ADD CONSTRAINT requestcomment_pkey PRIMARY KEY (id);


--
-- Name: requeststate_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY requeststate
    ADD CONSTRAINT requeststate_pkey PRIMARY KEY (id);


--
-- Name: section_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY section
    ADD CONSTRAINT section_pkey PRIMARY KEY (id);


--
-- Name: stp_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY stp
    ADD CONSTRAINT stp_pkey PRIMARY KEY (id);


--
-- Name: stp_section_through_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY stp_section_through
    ADD CONSTRAINT stp_section_through_pkey PRIMARY KEY (id);


--
-- Name: stprequest_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY stprequest
    ADD CONSTRAINT stprequest_pkey PRIMARY KEY (id);


--
-- Name: type_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY type
    ADD CONSTRAINT type_pkey PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: bot; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: message_chat_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX message_chat_id ON message USING btree (chat_id);


--
-- Name: message_user_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX message_user_id ON message USING btree (user_id);


--
-- Name: request_chat_through_chat_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX request_chat_through_chat_id ON request_chat_through USING btree (chat_id);


--
-- Name: request_chat_through_request_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX request_chat_through_request_id ON request_chat_through USING btree (request_id);


--
-- Name: request_chat_through_request_id_chat_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE UNIQUE INDEX request_chat_through_request_id_chat_id ON request_chat_through USING btree (request_id, chat_id);


--
-- Name: request_state_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX request_state_id ON request USING btree (state_id);


--
-- Name: request_type_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX request_type_id ON request USING btree (type_id);


--
-- Name: section_parent_section_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX section_parent_section_id ON section USING btree (parent_section_id);


--
-- Name: stp_section_through_section_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX stp_section_through_section_id ON stp_section_through USING btree (section_id);


--
-- Name: stp_section_through_stp_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX stp_section_through_stp_id ON stp_section_through USING btree (stp_id);


--
-- Name: stp_section_through_stp_id_section_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE UNIQUE INDEX stp_section_through_stp_id_section_id ON stp_section_through USING btree (stp_id, section_id);


--
-- Name: stp_user_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX stp_user_id ON stp USING btree (user_id);


--
-- Name: stprequest_comment_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX stprequest_comment_id ON stprequest USING btree (comment_id);


--
-- Name: stprequest_request_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX stprequest_request_id ON stprequest USING btree (request_id);


--
-- Name: stprequest_stp_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX stprequest_stp_id ON stprequest USING btree (stp_id);


--
-- Name: type_parent_type_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX type_parent_type_id ON type USING btree (parent_type_id);


--
-- Name: type_section_id; Type: INDEX; Schema: public; Owner: bot; Tablespace: 
--

CREATE INDEX type_section_id ON type USING btree (section_id);


--
-- Name: message_chat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY message
    ADD CONSTRAINT message_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES chat(id);


--
-- Name: message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY message
    ADD CONSTRAINT message_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: request_chat_through_chat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request_chat_through
    ADD CONSTRAINT request_chat_through_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES chat(id);


--
-- Name: request_chat_through_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request_chat_through
    ADD CONSTRAINT request_chat_through_request_id_fkey FOREIGN KEY (request_id) REFERENCES request(id);


--
-- Name: request_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_state_id_fkey FOREIGN KEY (state_id) REFERENCES requeststate(id);


--
-- Name: request_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_type_id_fkey FOREIGN KEY (type_id) REFERENCES type(id);


--
-- Name: request_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY request
    ADD CONSTRAINT request_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: section_parent_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY section
    ADD CONSTRAINT section_parent_section_id_fkey FOREIGN KEY (parent_section_id) REFERENCES section(id);


--
-- Name: stp_section_through_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stp_section_through
    ADD CONSTRAINT stp_section_through_section_id_fkey FOREIGN KEY (section_id) REFERENCES section(id);


--
-- Name: stp_section_through_stp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stp_section_through
    ADD CONSTRAINT stp_section_through_stp_id_fkey FOREIGN KEY (stp_id) REFERENCES stp(id);


--
-- Name: stp_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stp
    ADD CONSTRAINT stp_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: stprequest_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stprequest
    ADD CONSTRAINT stprequest_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES requestcomment(id);


--
-- Name: stprequest_request_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stprequest
    ADD CONSTRAINT stprequest_request_id_fkey FOREIGN KEY (request_id) REFERENCES request(id);


--
-- Name: stprequest_stp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY stprequest
    ADD CONSTRAINT stprequest_stp_id_fkey FOREIGN KEY (stp_id) REFERENCES stp(id);


--
-- Name: type_parent_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY type
    ADD CONSTRAINT type_parent_type_id_fkey FOREIGN KEY (parent_type_id) REFERENCES type(id);


--
-- Name: type_section_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: bot
--

ALTER TABLE ONLY type
    ADD CONSTRAINT type_section_id_fkey FOREIGN KEY (section_id) REFERENCES section(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

