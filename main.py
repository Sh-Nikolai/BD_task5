import psycopg2

conn = psycopg2.connect(database = 'clients', user = 'postgres', password = "sql")

    # 1
def createdb():
    cur.execute("""
    DROP TABLE phone;
    DROP TABLE client;
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY ,
        first_name VARCHAR (60) ,
        last_name VARCHAR (60) ,
        email varchar (60) UNIQUE
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        phone_number integer UNIQUE,
        client_id INTEGER REFERENCES client(id) on delete cascade
        );
        """)
    conn.commit()


    # 2
def new_data(first_name, last_name, email):
    cur.execute("""
        INSERT INTO client(first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id
        """, (first_name, last_name, email))
    conn.commit()

    return cur.fetchone()[0]


    # 3
def add_phone(phone_number, client_id):
    cur.execute("""
        INSERT INTO phone(phone_number , client_id )
        VALUES (%s, %s) RETURNING client_id
        """, (phone_number, client_id))

    conn.commit()


    # 4
def update_data( id, first_name=None, last_name=None, email=None, phone=None ):

    if first_name != None:
            cur.execute("""
            UPDATE client SET first_name =%s
            WHERE id =%s;
            """, (first_name, id))
    else:
        pass

    if last_name != None:
            cur.execute("""
            UPDATE client SET last_name =%s
            WHERE id =%s;
            """, (last_name, id))
    else:
        pass
    if phone != None:
        cur.execute("""
                UPDATE client SET phone =%s
                WHERE id =%s;
                """, (phone, id))
    else:
        pass
    if email != None:
        cur.execute("""
                UPDATE client SET email =%s
                WHERE id =%s;
                """, (email, id))
    else:
        pass


    conn.commit()


    # 5
def delete_phone(client_id):
    cur.execute("""
    DELETE FROM phone WHERE client_id =%s;
    """, (client_id,))
    conn.commit()


    # 6
def delete_client(id):

    cur.execute("""
        DELETE FROM client WHERE id =%s;    
        """, (id,))
    conn.commit()


    # 7
def search_client(first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
        SELECT first_name, last_name, email, phone FROM client
        left join phone on client.id = phone.client_id
        WHERE first_name =%s or last_name= %s or email =%s or email = %s;
        """, (first_name, last_name, email, phone))
    print('fetchall', cur.fetchall())
    conn.close()


conn = psycopg2.connect(database = 'clients', user = 'postgres', password = "sql")
with conn.cursor() as cur:
    createdb()
    new_data('fill', 'jonson', 'fill32@mail.ru')
    new_data('bill', 'jonson', 'bill@mail.ru')
    new_data('billy', 'jon', 'ssss@mail.ru')
    add_phone('5555555', 1)
    add_phone('44444', 2)
    add_phone('234234234', 2)
    update_data(first_name = 'georg', id =1)
    update_data(email='@@@@@', id=2)
    delete_phone(3)
    delete_client(2)
    search_client(last_name = 'jonson')

conn.close()
