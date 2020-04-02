import MySQLdb as mdb


def insertMovieIntoTable(movie, actor, director, viewer, rating):
    """
    Вставляет новый фильм в таблицу movie, заодно добавляя отсутвующих актеров, режисеров, обзорщиков и оценки.
    """
    db = mdb.connect('localhost', 'root', 'pass', 'qtdatabase')
    cursor = db.cursor()

    insertIntoTable("actor", actor)
    insertIntoTable("director", director)
    insertIntoTable("viewer", viewer)
    insertIntoTable("rating", rating)

    print("getrowid: " + getRowId("director", "director_name", director))

    column_str = "movie_title, director_director_id, viewer_viewer_id, actor_actor_id, rating_rating_id"
    value_str = "\"" + movie + "\" , \"" + \
                getRowId("director", "director_name", director) + "\" , \"" + \
                getRowId("viewer", "viewer_name", viewer) + "\" , \"" + \
                getRowId("actor", "actor_name", actor) + "\" , \"" + \
                getRowId("rating", "rating_value", rating) + "\""
    query = "INSERT INTO movie (" + column_str + ") VALUES (" + value_str + ");"

    print("insertMovie: " + query)

    try:
        cursor.execute(query)
        db.commit()
    except mdb.Error as e:
        return 'insertMovieIntoTable Error: ' + str(e.args[0])


def removeMovieFromTable(movie):
    """
    Удалеет из таблицы movie фильм.
    """
    deleteFromTable("movie", "movie_title", movie)


def insertIntoTable(table, value):
    """
    Вставляет в таблицу table новою строку.
    """
    db = mdb.connect('localhost', 'root', 'pass', 'qtdatabase')
    cursor = db.cursor()

    column_str = table + "_name" if table != "rating" else table + "_value"
    value_str = "\"" + value + "\"" if type(value) != int else str(value)
    query = "INSERT INTO " + table + " (" + column_str + ") VALUES (" + value_str + ");"
    print("insertIntoTable:" + query)
    try:
        cursor.execute(query)
        db.commit()
    except mdb.Error as e:
        return 'insertIntoTable Error: ' + str(e.args[0])


def deleteFromTable(table, cell, cell_value):
    """
    Удаляет из таблицы table строку, удовл. условию cell = cell_value
    """
    db = mdb.connect('localhost', 'root', 'pass', 'qtdatabase')
    cursor = db.cursor()

    value_str = "\"" + cell_value + "\"" if type(cell_value) != int else str(cell_value)
    query = "DELETE FROM " + table + " WHERE " + cell + " = " + value_str + ";"
    print("deleteFromTable: " + query)
    try:
        cursor.execute(query)
        db.commit()
    except mdb.Error as e:
        return 'deleteFromTable Error: ' + str(e.args[0])


def getRowFromTable(table, cell, cell_value):
    """
    Возвращает из таблицы table строку, удовл. условию cell = cell_value
    """
    db = mdb.connect('localhost', 'root', 'pass', 'qtdatabase')
    cursor = db.cursor()

    value_str = "\"" + cell_value + "\"" if type(cell_value) != int else str(cell_value)
    print("value str: " + value_str)
    query = "SELECT * FROM " + table + " WHERE " + cell + " = " + value_str + ";"
    print("getRowFromTable:" + query)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mdb.Error as e:
        return 'getRowFromTable Error: ' + str(e.args[0])


def getRowId(table, cell, cell_value):
    """
    Вовращает id строки.
    """
    return str(getRowFromTable(table, cell, cell_value)[0][0])


def getAllFromTable(table):
    """
    Вовращает все строки из таблицы table.
    """
    db = mdb.connect('localhost', 'root', 'pass', 'qtdatabase')
    cursor = db.cursor()

    query = "SELECT * FROM " + table + ";"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mdb.Error as e:
        return 'getAllfromTable Error: ' + str(e.args[0])


def rowToString(row):
    """
    Вовращает представление строки из таблицы movie в string виде.
    """
    result = row[1]
    director = getRowFromTable("director", "director_id", row[2])
    viewer = getRowFromTable("viewer", "viewer_id", row[3])
    actor = getRowFromTable("actor", "actor_id", row[4])
    rating = getRowFromTable("rating", "rating_id", row[5])
    result = "Title: " + result + " Dir: " + director[0][1] + " Viewer: " + viewer[0][1] + " Actor: " + actor[0][1] + " Rate: " + str(rating[0][1])
    print("rowToString: " + result)
    return result
