from pocket import Pocket, PocketException
import yaml


def get_pocket():
    """Create a Pocket object"""
    with open("conf.yaml", 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    pocket = Pocket(
        consumer_key=conf['credentials']['consumer_key'],
        access_token=conf['credentials']['access_token']
    )
    return pocket


def fetch_items(pocket, count=0):
    """Get entries from pocket API"""
    try:
        return pocket.retrieve(count=count, detailType='complete', offset=0)
    except PocketException as exception:
        print(exception)


def get_data(items):
    """Get data from Pocket response"""
    data = {}
    for _, v in items['list'].items():
        title = v['given_title']
        url = v['given_url']
        item_id = v['item_id']
        note = ""
        if title in (None, ''):
            print("MISSING TITLE: " + url)
            title = url
            note = "Missing title"
        try:
            tags = v['tags']
            print(tags)
        except KeyError:
            print("MISSING TAGS: " + title)
            tags = {'NA': {'item_id': item_id, 'tag': 'NA'}}
            note = "Missing tags"
        data[item_id] = [title, url, tags, note]
    return data


#  def list_entries(data_hash, typ):
#      """Return a list of entries according to a typ"""
#      entries = []
#      types = {'titles': 0, 'urls': 1, 'tags': 2}
#      print(types.get(typ, 'error'))
#      for _, v in data_hash.items():
#          try:
#              entries.append(v[types.get(typ, 'error')])
#          except KeyError:
#              print("ERROR TYP not found" + typ)
#      return entries


def get_tags(entry):
    """Returns a simple string of tags for one entry"""
    tags = ""
    for tag, _ in entry[2].items():
        tags += tag + " "
    return tags.strip()