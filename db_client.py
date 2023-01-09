import psycopg2
from secret import postgre_password

DBNAME = 'postgres'
USER = 'postgres'
PASSWORD = postgre_password
HOST = 'localhost'

def select_all(section_name):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM public.menu WHERE section = '{section_name}'")
            return cur.fetchall()

all_starters = select_all('starter')
all_hot_meals = select_all('hot_meals')
all_desserts = select_all('desserts')
all_drinks = select_all('drinks')

def insert_user_message(user_name, text, message_time):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as con:
        with con.cursor() as cur:
            cur.execute(f"INSERT INTO public.user_messages (user_name, text, message_time) "
                        f"VALUES ('{user_name}', '{text}', '{message_time}')")

def insert_user_click(name, click_time, button):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as con:
        with con.cursor() as cur:
            cur.execute(f"INSERT INTO public.user_click (name, click_time, button) "
                        f"VALUES ('{name}', '{click_time}', '{button}')")

def select_top_button():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT button, COUNT(click_time) AS num_click FROM public.user_click "
                        f"GROUP BY button "
                        f"ORDER BY num_clickDESC "
                        f"LIMIT 3")
            return cur.fetchall()

def select_top_user():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT name, COUNT(button) AS click FROM public.user_click "
                        f"GROUP BY name "
                        f"ORDER BY click DESC "
                        f"LIMIT 3")
            return cur.fetchall()