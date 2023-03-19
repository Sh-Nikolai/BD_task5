import psycopg2
conn = psycopg2.connect(database='clients', user='postgres', password='sql')

# 1
def createdb():
        with conn.cursor() as cur:


                cur.execute("""
                DROP TABLE Phone;
                DROP TABLE client;
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR (60) ,
                last_name VARCHAR (60) ,
                email varchar (60) UNIQUE
                );
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS Phone(
                id SERIAL PRIMARY KEY,
                phone_number integer UNIQUE,
                client_id INTEGER REFERENCES client(id)
                );
                """)
                conn.commit()

# 2
def new_data( first_name, last_name, email, phones = None):
    with psycopg2.connect(database='clients', user='postgres', password='sql') as conn:
        with conn.cursor() as cur:

            cur.execute("""
            INSERT INTO client(first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id
            """, (first_name, last_name, email))
            conn.commit()

            return cur.fetchone()[0]



    # 3
def add_phone(phone_number,client_id):
    with psycopg2.connect(database='clients', user='postgres', password='sql') as conn:
        with conn.cursor() as cur:

            cur.execute("""
            INSERT INTO Phone(phone_number , client_id )
            VALUES (%s, %s) RETURNING client_id
            """, (phone_number, client_id))
            return cur.fetchone()[0]
            conn.commit()



    # 4
def update_data (first_name, last_name, email, id):
    with psycopg2.connect(database='clients', user='postgres', password='sql') as conn:
        with conn.cursor() as cur:

            cur.execute("""
            UPDATE client SET first_name =%s, last_name= %s, email =%s
            WHERE id =%s;
            """, (first_name, last_name, email, id))
            conn.commit()


    # 5
def delete_phone(id):
    with psycopg2.connect(database='clients', user='postgres', password='sql') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM Phone WHERE id =%s;
            """, ( id,))
            conn.commit()



    # 6
def delete_client(id):
    with psycopg2.connect(database='clients', user='postgres', password='sql') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM client WHERE id =%s;
            """, ( id,))
            conn.commit()

    # 7
def search_client(first_name, last_name, email):
    with psycopg2.connect(database='clients', user='postgres', password='sql') as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT id FROM client
            WHERE first_name =%s and last_name= %s and email =%s;
            """, (first_name, last_name, email))
            return cur.fetchone()[0]

