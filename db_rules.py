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

    # Selecteer alle product_ids en extraheer.
    cursor.execute('SELECT product_id FROM content_filtering')
    id_data = cursor.fetchall()

    # Met cleaned wordt bedoelt dat de data geen onzinnige punten, kommas en haakjes bevat.
    cleaned_id_data = [x[0] for x in id_data]
    product_ids = []

    # Elk element uit de cleaned_id_data lijst wordt gechecked op " ' " om ervoor te zorgen dat het niet in conflict gaat met de sql queries.
    for c in range(len(cleaned_id_data)):
        ids = cleaned_id_data[c]
        id_data_replaced = ids.replace("'", "")
        product_ids.append(id_data_replaced)

    # Simpel Query om de product_id, sub_sub_category en gender uit content_filtering te halen.
    cursor.execute('SELECT product_id, sub_sub_category, gender FROM content_filtering')
    data = cursor.fetchall()

    temp_lst = []
    clean_lst = []

    for i in range(len(data)):

        # De desbetreffende onderdelen van benodigde data los behandeld om ook hier de onnodige " ' " te verwijderen.
        sub_sub = data[i][1]
        gen = data[i][2]

        sub_sub_replaced = sub_sub.replace("'", "")

        # Query om de recommendations te vinden dat zowel een vergelijking heeft met sub_sub als gender.
        cursor.execute(
            "SELECT product_id FROM content_filtering "
            "WHERE sub_sub_category = '{0}' AND gender = '{1}' limit 5".format(sub_sub_replaced, gen))
        rec_products = cursor.fetchall()

        temp_lst.append(rec_products)

    # Hierbij wordt het eerste onderdeel wat vaak hetzelfde product_id is als van het gekozen record, verwijdered zodat je alleen unieke producten zal verkrijgen.
    result_lst = [i[1:] for i in temp_lst]

    # For loop om de result_lst op te schonen van onnodige syntax.
    for y in range(len(result_lst)):
        data = result_lst[y]
        cleaned_data = [x[0] for x in data]
        clean_lst.append(cleaned_data)

    # Hierbij worden er alleen de eerste 100 records van zowel de product_ids als recommendations gepakt, omdat het anders veels te lang zal duren de records in te vullen [AANPASBAAR].
    product_ids_100 = product_ids[:100]
    clean_lst_100 = clean_lst[:100]

    # Count op null, per invulling van recommendation string, wordt de count met 1 verhoogd, om zo elk verkozen record van recommendation te voorzien.
    ct = 0
    while ct <= 100: # Dit getal hoort eigenlijk het rec_count te zijn omdat het alle records van de database vertegenwoordigd.
        for x in range(len(clean_lst_100)):
            result = clean_lst_100[x]
            if len(result) >= 4:
                # De recommendatie list wordt opgesplitst in fragmenten die vervolgens als string wordt verbonden omdat SQL moeilijk doet als je het niet als één grote string meegeeft als insert/update.
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