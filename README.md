# PCKT

A CLI for [Pocket](https://getpocket.com/) following [12 Factor CLI APP](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46).

## API and credentials

For accessing your Pocket items you must obtain a free API access. [James Mackenzie](https://www.jamesfmackenzie.com/getting-started-with-the-pocket-developer-api/) provide an excellent guide.

With your credentials create a file named `conf.yaml` with the following content:

```yaml
credentials:
  consumer_key: '<your-key>'
  access_token: '<your-token>'
```

## Functionality

1. Retrieve all Pocket entries from your account
1. Store `url`, `title`, and `tags` in a local sqlite3 database
1. Handle and mark missing fields (e.g. missing title)
1. Print simple statistics about tags
1. Filter and out stored entries as ascii table or parsable

## Commands

```bash
$ python main.py
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  CLI for interacting with the Pocket API

Options:
  --help  Show this message and exit.

Commands:
  filter  Filter and list entries
  tags    Prints tags and their figures
  update  Updates/recreates the database containing all information
```

### Create / update local database
```bash
$ python main.py update --help
Usage: main.py update [OPTIONS]

  Updates/recreates the database containing all information

Options:
  --count INTEGER  number of entries to fetch
  --path TEXT      path to sqlite3 file
  --help           Show this message and exit.
```

### List and filter entries

```bash
$ python main.py filter --help
Usage: main.py filter [OPTIONS] [KEYWORDS]...

  Filter and list entries

Options:
  --path TEXT                 path to sqlite3 file
  --width INTEGER             column width of url and title
  --col TEXT                  Which column to search
  --count / --no-count        Prints number of items
  --parsable / --no-parsable  Output no asci table
  --help                      Show this message and exit.
```

### Print tag stats

```bash
$ python main.py tags --help
Usage: main.py tags [OPTIONS]

  Prints tags and their figures

Options:
  --path TEXT         path to sqlite3 file
  --sort / --no-sort  sort by tag numbers
  --help              Show this message and exit.
```

## Roadmap

- [ ] Tests :wink:
- [ ] Formalize structure according to python standards :cop:
- [ ] PyPi upload :v:
- [ ] Error handling :grin:
- [ ] Single executable packaging :100:
