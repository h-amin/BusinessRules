for k in range(len(clean_lst) - 1):
    p = clean_lst[k]
    if p == 4:
        p_1 = clean_lst[k][0]
        p_2 = clean_lst[k][1]
        p_3 = clean_lst[k][2]
        p_4 = clean_lst[k][3]
        full_p = p_1 + ' ' + p_2 + ' ' + p_3 + ' ' + p_4
    elif p == 3:
        p_1 = clean_lst[k][0]
        p_2 = clean_lst[k][1]
        p_3 = clean_lst[k][2]
        full_p = p_1 + ' ' + p_2 + ' ' + p_3
    elif p == 2:
        p_1 = clean_lst[k][0]
        p_2 = clean_lst[k][1]
        full_p = p_1 + ' ' + p_2
    else:
        full_p = 'None'

        for k in range(len(clean_lst)):
            for n in range(len(product_ids)):
                recs = clean_lst[k]
                string = ', '.join([str(item) for item in recs])
                print(string)
                cursor.execute(
                    "UPDATE content_filtering SET recommendations = '{0}' WHERE product_id = '{1}' AND sub_sub_category = '{2}' AND gender = '{3}'".format(
                        string, p_id, sub_sub, gen))

    for h in range(len(clean_lst)):
        recs = clean_lst[h]
        string = ', '.join([str(item) for item in recs])
        print(string)
        cursor.execute("UPDATE content_filtering SET recommendations = '{0}' WHERE product_id = '{1}'".format(recs,product_ids_100[products]))