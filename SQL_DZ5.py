import psycopg2

conn = psycopg2.connect(database="clientsdb", user="postgres", password="postgres")

def create_db():
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                id serial PRIMARY KEY,
                last_name VARCHAR(50) NOT NULL,
                fist_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS phones(
                id serial PRIMARY KEY,
                clients_id int references clients(id),
                phone VARCHAR(50)
                );
                """)

        conn.commit()




def add_client():
    with conn.cursor() as cur:
        fist_names = input("Введите имя:")
        last_names = input("Введите фамилию:")
        emails = input("Введите эл.почту:")

        cur.execute("""
                insert into clients(fist_name, last_name, email)
                values(%s, %s, %s);
                """, (fist_names, last_names, emails))

        conn.commit()




def add_phone():
    with conn.cursor() as cur:
        client_id = input("Введите ID клиента:")
        phones = input("Введите номер телефона:")

        cur.execute("""
                insert into phones(clients_id, phone)
                values(%s, %s) RETURNING ID;
                """, (client_id, phones))

        conn.commit()




def change_client():
    with conn.cursor() as cur:
        client_id = input("Введите ID клиента которого хотите изменить:")
        fist_names = input("Введите имя:")
        last_names = input("Введите фамилию:")
        emails = input("Введите эл.почту:")
        phones = input("Введите номер телефона:")

        cur.execute("""
                UPDATE clients SET last_name=%s, fist_name=%s, email=%s WHERE id=%s;
                """, (last_names, fist_names, emails, client_id))

        cur.execute("""
                UPDATE phones SET phone=%s WHERE clients_id=%s;
                """, (phones, client_id))

        conn.commit()




def delete_phone():
    with conn.cursor() as cur:
        client_id = input("Введите ID клиента у которого хотите удалить номер телефона:")

        cur.execute("""
                DELETE FROM phones WHERE clients_id=%s;
                """, (client_id,))

        conn.commit()




def delete_client():
    with conn.cursor() as cur:
        client_id = input("Введите ID клиента которого хотите удалить:")

        cur.execute("""
                DELETE FROM clients WHERE id=%s;
                """, (client_id,))

        conn.commit()




def find_client():
    with conn.cursor() as cur:
        client_search = input("Введдите данные:")

        cur.execute("""
                SELECT id, last_name, fist_name, email FROM clients WHERE fist_name=%s;
                """, (client_search,))
        print(cur.fetchall())

        cur.execute("""
                    SELECT id, last_name, fist_name, email FROM clients WHERE last_name=%s;
                    """, (client_search,))
        print(cur.fetchall())

        cur.execute("""
                    SELECT id, last_name, fist_name, email FROM clients WHERE email=%s;
                    """, (client_search,))
        print(cur.fetchall())

        cur.execute("""
                    SELECT id, clients_id, phone FROM phones WHERE phone=%s;
                    """, (client_search,))
        print(cur.fetchall())


with psycopg2.connect(database="clientsdb", user="postgres", password="postgres") as conn:
    add_client()
    find_client()
    add_phone()
    change_client()
    delete_phone()
    delete_client()


conn.close()
