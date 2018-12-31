import sys
import json
from pprint import pprint
import texttable
from db import create_db_con


def get_cur(path):
    """Returns a cursor to the sqlite3 db"""
    con = create_db_con(path)
    cur = con.cursor()
    return cur


def select_col(path, col):
    """Returns a given col
    0 = titles
    1 = urls
    2 = tags
    3 = note
    """
    con = create_db_con(path)
    con.row_factory = lambda cursor, row: row[col]
    sql = '''SELECT * FROM entries'''
    cur = con.cursor()
    return cur.execute(sql).fetchall()


def get_tags_stats(col, sort):
    """List statistics about tags of entries"""
    tags = {}
    for row in col:
        for tag in row.split():
            tags[tag] = tags.get(tag, 0) + 1
    if sort:
        sorted_by_value = sorted(tags.items(), key=lambda kv: kv[1])
        pprint(sorted_by_value)
    else:
        print(json.dumps(tags))


def list_entries(path, width, col, count, parsable, terms):
    """Filters and lists entries"""
    cur = get_cur(path)
    sql = ""
    if col == 'complete':
        if terms:
            terms = ' AND '.join(terms)
            sql = 'SELECT * FROM entries WHERE entries MATCH ?'
            result = cur.execute(sql, (terms,)).fetchall()
        else:
            sql = 'SELECT * FROM entries'
            result = cur.execute(sql).fetchall()
    else:
        if terms:
            terms = ' AND '.join(terms)
            sql = 'SELECT * FROM entries WHERE {} MATCH ?'.format(col)
            result = cur.execute(sql, (terms,)).fetchall()
        else:
            print("Warning: col without search term not useful")
            sys.exit(1)
    if parsable:
        print(result)
    else:
        table = texttable.Texttable()
        table.set_cols_width([width, width, 15, 15])
        for row in result:
            table.add_row(list(row))
        print(table.draw() + "\n")
    if count:
        print("Found entries: {} \n".format(len(result)))
