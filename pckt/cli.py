import click
from db import clear_db, update_db
from fetch import get_data, fetch_items, get_pocket
from read import get_tags_stats, select_col, list_entries, view_entries


@click.group()
def main():
    """CLI for interacting with the Pocket API"""
    pass


@main.command()
@click.option('--count', default=10, help='number of entries to fetch')
@click.option('--path', default='pckt.db', help='path to sqlite3 file')
def update(count, path):
    """Updates/recreates the database containing all information"""
    clear_db(path)
    update_db(path, get_data(fetch_items(get_pocket(), count)))


@main.command()
@click.option('--path', default='pckt.db', help='path to sqlite3 file')
@click.option('--sort/--no-sort', default=False, help='sort by tag numbers')
def tags(path, sort):
    """Prints tags and their figures"""
    get_tags_stats(select_col(path, 2), sort)


@main.command()
@click.option('--path', default='pckt.db', help='path to sqlite3 file')
@click.option('--width', default=90, help='column width of url and title')
@click.option('--col', default='complete', help='Which column to search')
@click.option('--count/--no-count', default=False, help='Prints number of items')
@click.option('--parsable/--no-parsable', default=False, help='Output no asci table')
@click.argument('keywords', nargs=-1)
def filter(path, width, col, count, parsable, keywords):
    """Filter and list entries"""
    view_entries(list_entries(path, col, keywords), width, count, parsable)
