import psycopg2
conn = psycopg2.connect(database='clients', user='postgres', password='sql')
with conn.cursor() as cur:
# 1
    def createdb():



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


            cur.execute("""
            INSERT INTO client(first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id
            """, (first_name, last_name, email))
            conn.commit()

            return cur.fetchone()[0]



    # 3
    def add_phone(phone_number,client_id):


            cur.execute("""
            INSERT INTO Phone(phone_number , client_id )
            VALUES (%s, %s) RETURNING client_id
            """, (phone_number, client_id))
            return cur.fetchone()[0]
            conn.commit()



    # 4
    def update_data (first_name= None, last_name= None, email= None, id= None):


            cur.execute("""
            UPDATE client SET first_name =%s, last_name= %s, email =%s
            WHERE id =%s;
            """, (first_name, last_name, email, id))
            conn.commit()


    # 5
    def delete_phone(id):

            cur.execute("""
            DELETE FROM Phone WHERE id =%s;
            """, ( id,))
            conn.commit()



    # 6
    def delete_client(id):

            cur.execute("""
            DELETE FROM phone WHERE id =%s;
            DELETE FROM client WHERE id =%s;
            """, ( id,))
            conn.commit()

    # 7
    def search_client(first_name=None, last_name=None, email=None, phone=None):

            cur.execute("""
            SELECT id FROM client
            WHERE first_name =%s and last_name= %s and email =%s;
            """, (first_name, last_name, email,phone))
            return cur.fetchone()[0]

    createdb()
    # # 2
    new_data('anna', 'smit', '899anna@mail.com')
    # 3
    add_phone(810549752412, 1)
    # 4
    update_data(first_name=bill, last_name=None, email=None, id=2)

    # 5
    delete_phone(1)
    # 6
    delete_client(1)
    # 7
    search_client(first_name=anna, last_name=None, email=None, phone=None)


conn.close()