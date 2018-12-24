from db import create_db_con


def select_row(path, col):
    """Returns a given row
    0 = titles
    1 = urls
    2 = tags
    """
    con = create_db_con(path)
    con.row_factory = lambda cursor, row: row[col]
    sql = '''SELECT * FROM entries'''
    cur = con.cursor()
    return cur.execute(sql).fetchall()


def get_tags_stats(rows):
    """List statistics about tags of entries"""
    tags = {}
    for row in rows:
        for tag in row.split():
            tags[tag] = tags.get(tag, 0) + 1
    return tags


def filter_entries(*terms):
    """Functions which filters all entries by one or more keywords"""
    if terms == 0:
        print("No keyword specified")
    sql = "SELECT * FROM entries WHERE entries MATCH 'linux AND tools'"

