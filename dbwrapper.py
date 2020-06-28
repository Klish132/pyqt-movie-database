import MySQLdb as mdb


def message_analyzer(action, info):
    result = []
    if action == "ADDMOVIE":
        list = info.split("|")
        movie = list[0]
        actor = list[1]
        director = list[2]
        viewer = list[3]
        rating = int(list[4])
        insert_movie_into_table(movie, actor, director, viewer, rating)
        result.append("UPDMOV")
    elif action == "ADDACTOR":
        insert_row_into_table("actor", info)
        result.append("UPDACT")
    elif action == "ADDDIR":
        insert_row_into_table("director", info)
        result.append("UPDDIR")
    elif action == "ADDREV":
        insert_row_into_table("viewer", info)
        result.append("UPDREV")
    elif action == "REMMOV":
        remove_movie_from_table(info)
        result.append("UPDMOV")
    elif action == "REMACTOR":
        remove_row_from_table("actor", "actor_name", info)
        result.append("UPDACT")
    elif action == "REMDIR":
        remove_row_from_table("director", "director_name", info)
        result.append("UPDDIR")
    elif action == "REMREV":
        remove_row_from_table("viewer", "viewer_name", info)
        result.append("UPDREV")
    elif action == "LOADMOV":
        movies = get_all_rows_from_table("movie")
        for movie in movies:
            result.append(movie_to_string(movie))
    elif action == "LOADACTOR":
        actors = get_all_rows_from_table("actor")
        for actor in actors:
            result.append(actor_to_string(actor))
    elif action == "LOADDIR":
        directors = get_all_rows_from_table("director")
        for director in directors:
            result.append(director_to_string(director))
    elif action == "LOADREV":
        reviewers = get_all_rows_from_table("viewer")
        for reviewer in reviewers:
            result.append(reviewer_to_string(reviewer))
    else:
        result.append("ERROR")
    if len(result) == 0:
        result.append("ERROR")
    return result


def insert_movie_into_table(movie, actor, director, viewer, rating):
    """
    Вставляет новый фильм в таблицу movie, заодно добавляя отсутвующих актеров, режисеров, обзорщиков и оценки.
    """
    db = mdb.connect('localhost', 'root', 'hAj1mE132', 'qtdatabase')
    cursor = db.cursor()

    insert_row_into_table("actor", actor)
    insert_row_into_table("director", director)
    insert_row_into_table("viewer", viewer)
    insert_row_into_table("rating", rating)

    column_str = "movie_title, director_director_id, viewer_viewer_id, actor_actor_id, rating_rating_id"
    value_str = "\"" + movie + "\" , \"" + \
                get_row_id("director", "director_name", director) + "\" , \"" + \
                get_row_id("viewer", "viewer_name", viewer) + "\" , \"" + \
                get_row_id("actor", "actor_name", actor) + "\" , \"" + \
                get_row_id("rating", "rating_value", rating) + "\""
    query = "INSERT INTO movie (" + column_str + ") VALUES (" + value_str + ");"

    try:
        cursor.execute(query)
        db.commit()
    except mdb.Error as e:
        return 'insertMovieIntoTable Error: ' + str(e.args[0])


def remove_movie_from_table(movie):
    """
    Удалеет из таблицы movie фильм.
    """
    remove_row_from_table("movie", "movie_title", movie)


def insert_row_into_table(table, value):
    """
    Вставляет в таблицу table новою строку.
    """
    db = mdb.connect('localhost', 'root', 'hAj1mE132', 'qtdatabase')
    cursor = db.cursor()

    column_str = table + "_name" if table != "rating" else table + "_value"
    value_str = "\"" + value + "\"" if type(value) != int else str(value)
    query = "INSERT INTO " + table + " (" + column_str + ") VALUES (" + value_str + ");"
    try:
        cursor.execute(query)
        db.commit()
    except mdb.Error as e:
        return 'insertIntoTable Error: ' + str(e.args[0])


def remove_row_from_table(table, cell, cell_value):
    """
    Удаляет из таблицы table строку, удовл. условию cell = cell_value
    """
    db = mdb.connect('localhost', 'root', 'hAj1mE132', 'qtdatabase')
    cursor = db.cursor()

    value_str = "\"" + cell_value + "\"" if type(cell_value) != int else str(cell_value)
    query = "DELETE FROM " + table + " WHERE " + cell + " = " + value_str + ";"
    #print("deleteFromTable: " + query)
    try:
        cursor.execute(query)
        db.commit()
    except mdb.Error as e:
        return 'deleteFromTable Error: ' + str(e.args[0])


def get_row_from_table(table, cell, cell_value):
    """
    Возвращает из таблицы table строку, удовл. условию cell = cell_value
    """
    db = mdb.connect('localhost', 'root', 'hAj1mE132', 'qtdatabase')
    cursor = db.cursor()

    value_str = "\"" + cell_value + "\"" if type(cell_value) != int else str(cell_value)
    query = "SELECT * FROM " + table + " WHERE " + cell + " = " + value_str + ";"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mdb.Error as e:
        return 'getRowFromTable Error: ' + str(e.args[0])


def get_row_id(table, cell, cell_value):
    """
    Вовращает id строки.
    """
    return str(get_row_from_table(table, cell, cell_value)[0][0])


def get_all_rows_from_table(table):
    """
    Вовращает все строки из таблицы table.
    """
    db = mdb.connect('localhost', 'root', 'hAj1mE132', 'qtdatabase')
    cursor = db.cursor()

    query = "SELECT * FROM " + table + ";"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mdb.Error as e:
        return 'getAllfromTable Error: ' + str(e.args[0])


def actor_to_string(row):
    actor = row[1]
    return "[ACTOR]" + actor


def director_to_string(row):
    director = row[1]
    return "[DIRECTOR]" + director


def reviewer_to_string(row):
    reviewer = row[1]
    return "[REVIEWER]" + reviewer


def movie_to_string(row):
    movie = row[1]
    director = get_row_from_table("director", "director_id", row[2])
    viewer = get_row_from_table("viewer", "viewer_id", row[3])
    actor = get_row_from_table("actor", "actor_id", row[4])
    rating = get_row_from_table("rating", "rating_id", row[5])
    list = [movie, director[0][1], viewer[0][1], actor[0][1], str(rating[0][1])]
    result = "|".join(list)
    return "[MOVIE]" + result

