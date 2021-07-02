import psycopg2


# Establish database connectie.
def get_sql_connection(psycopg2):
    connection = psycopg2.connect(user="postgres",
                                  password="38gAc57ip!",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    return connection


# Open database connectie.
def open_db_connection():
    global connection, cursor
    try:
        connection = get_sql_connection(psycopg2)
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connection to PostgresQL", error)


# Close database connectie.
def close_db_connection():
    if connection:
        connection.commit()
        cursor.close()
        connection.close()


# Functie om tabellen aan te maken.
def create_tables():
    cursor.execute('CREATE TABLE IF NOT EXISTS content_filtering ('
                   'product_id varchar PRIMARY KEY,'
                   'sub_sub_category varchar,'
                   'gender varchar,'
                   'recommendations varchar)')

    # Insert query met als doel om product_id, sub_sub_category en gender in hetzelfde table; content_filtering te verkrijgen.
    cursor.execute(
        'INSERT INTO content_filtering(product_id, gender, sub_sub_category) SELECT p.product_id, p.gender, pc.sub_sub_category FROM products p INNER JOIN product_categories pc ON pc.product_id = p.product_id WHERE sub_sub_category IS NOT NULL AND gender IS NOT NULL;')

    cursor.execute('CREATE TABLE IF NOT EXISTS collaborative_filtering ('
                   'product_id varchar PRIMARY KEY,'
                   'recommendations varchar)')

    # Zelfde principe met alleen product_id.
    cursor.execute(
        'INSERT INTO content_filtering(product_id) SELECT product_id FROM products;')


# Functie dat opzoek gaat naar 4 product_id's die overeenkomende sub_sub_category en gender hebben met elk record.
def fill_recommendations_content():
    cursor.execute('SELECT product_id FROM content_filtering')
    id_data = cursor.fetchall()
    cleaned_id_data = [x[0] for x in id_data]
    product_ids = []

    for c in range(len(cleaned_id_data)):
        ids = cleaned_id_data[c]
        id_data_replaced = ids.replace("'", "")
        product_ids.append(id_data_replaced)

    cursor.execute('SELECT product_id, sub_sub_category, gender FROM content_filtering')
    data = cursor.fetchall()

    temp_lst = []
    clean_lst = []

    for i in range(len(data)):
        sub_sub = data[i][1]
        gen = data[i][2]

        sub_sub_replaced = sub_sub.replace("'", "")

        cursor.execute(
            "SELECT product_id FROM content_filtering "
            "WHERE sub_sub_category = '{0}' AND gender = '{1}' limit 5".format(sub_sub_replaced, gen))
        rec_products = cursor.fetchall()

        temp_lst.append(rec_products)

    result_lst = [i[1:] for i in temp_lst]

    for y in range(len(result_lst)):
        data = result_lst[y]
        cleaned_data = [x[0] for x in data]
        clean_lst.append(cleaned_data)

    product_ids_100 = product_ids[:100]
    clean_lst_100 = clean_lst[:100]

    ct = 0
    while ct <= 100:
        for x in range(len(clean_lst_100)):
            result = clean_lst_100[x]
            if len(result) >= 4:
                rec1 = clean_lst_100[x][0]
                rec2 = clean_lst_100[x][1]
                rec3 = clean_lst_100[x][2]
                rec4 = clean_lst_100[x][3]
                recs = rec1 + ',' + rec2 + ',' + rec3 + ',' + rec4
                recs_replaced = recs.replace("'", "")
                cursor.execute("UPDATE content_filtering SET recommendations = '{0}' WHERE product_id = '{1}'".format(recs_replaced, product_ids_100[x]))
                ct += 1
                continue


# Functie dat opzoek gaat naar 4 product_id's die overeenkomende visitor_ids hebben.
def fill_recommendations_collaborative():
    cursor.execute("SELECT product_id FROM collaborative_filtering")
    data = cursor.fetchall()

    product_ids = []

    for pr in range(len(data)):
        ids = data[pr]
        id_data_replaced = ids.replace("'", "")
        product_ids.append(id_data_replaced)

    recs_lst = []


# Master function om connectie te maken met het database en daadwerkelijk de functies uitvoeren.
def fill_tables():
    open_db_connection()
    # create_tables()
    fill_recommendations_content()
    close_db_connection()
