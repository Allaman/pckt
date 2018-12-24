from pocket import PocketException


def fetch_items(pocket, count=0):
    """Get entries from pocket API"""
    try:
        return pocket.retrieve(count=count, detailType='complete', offset=0)
    except PocketException as exception:
        print(exception)


def get_data(items):
    """Get data from Pocket response"""
    data = {}
    for k, v in items['list'].items():
        title = v['given_title']
        url = v['given_url']
        id = v['item_id']
        if title == None or title == '':
            print("MISSING TITLE: " + url)
            title = url
        try:
            tags = v['tags']
        except KeyError:
            print("MISSING TAGS: " + title)
        data[id] = [title, url, tags]
    return data


def list_entries(data_hash, typ):
    """Return a list of entries according to a typ"""
    entries = []
    types = {'titles': 0, 'urls': 1, 'tags': 2}
    print(types.get(typ, 'error'))
    for _, v in data_hash.items():
        try:
            entries.append(v[types.get(typ, 'error')])
        except KeyError:
            print("ERROR TYP not found" + typ)
    return entries


def get_tags(entry):
    """Returns a simple list of tags for one entry"""
    tags = ""
    for tag, _ in entry[2].items():
        tags += " " + tag
    return tags


