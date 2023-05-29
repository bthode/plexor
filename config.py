import os

database_file = "database.db"
script_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_dir, database_file)

ATOM_NS = "{http://www.w3.org/2005/Atom}"

entry = f"{ATOM_NS}entry"
entry_link = f"{ATOM_NS}link[@rel='alternate']"
entry_title = f"{ATOM_NS}title"
entry_published = f"{ATOM_NS}published"

iso_8601_tz = "%Y-%m-%dT%H:%M:%S%z"

# TODO Merge with above...
CHANNEL_URL = './/{http://www.w3.org/2005/Atom}link[@rel="alternate"]'

CHANNEL_NAME = '{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name'

ATOM_LINK_REL_ALTERNATE_ = "{http://www.w3.org/2005/Atom}link[@rel='alternate']"

ORG_ATOM_TITLE = "{http://www.w3.org/2005/Atom}title"
