import os
import sys
import io
import errno
import requests
import pandas as pd

APPEND = True

BASE_URL = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

ATTRIBUTES = ['Overall', 'Attack', 'Defence', 'Strength', 'Hitpoints', 'Ranged', 'Prayer', 'Magic', 'Cooking',
              'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining', 'Herblore',
              'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecrafting', 'Hunter', 'Construction',
              'League Points', 'Bounty Hunter - Hunter', 'Bounty Hunter - Rogue',
              'Clue Scrolls (all)', 'Clue Scrolls (beginner)', 'Clue Scrolls (easy)', 'Clue Scrolls (medium)',
              'Clue Scrolls (hard)', 'Clue Scrolls (elite)', 'Clue Scrolls (master)',
              'LMS - Rank',
              'Abyssal Sire', 'Alchemical Hydra', 'Barrows Chests', 'Bryophyta', 'Callisto', 'Cerberus',
              'Chambers of Xeric', 'Chambers of Xeric: Challenge Mode', 'Chaos Elemental', 'Chaos Fanatic',
              'Commander Zilyana', 'Corporeal Beast', 'Crazy Archaeologist', 'Dagannoth Prime', 'Dagannoth Rex',
              'Dagannoth Supreme', 'Deranged Archaeologist', 'General Graardor', 'Giant Mole', 'Grotesque Guardians',
              'Hespori', 'Kalphite Queen', 'King Black Dragon', 'Kraken', "Kree'Arra", "K'ril Tsutsaroth", 'Mimic',
              'Obor', 'Sarachnis', 'Scorpia', 'Skotizo', 'The Gauntlet', 'The Corrupted Gauntlet', 'Theatre of Blood',
              'Thermonuclear Smoke Devil', 'TzKal-Zuk', 'TzTok-Jad', 'Venenatis', "Vet'ion", 'Vorkath', 'Wintertodt',
              'Zalcano', 'Zulrah']


def get_filename(path, user):
    return os.path.join(path, user + ".csv")


def make_dir(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


def init(path):
    # Does folder exist
    if not os.path.exists(path):
        # create folder
        make_dir(path)

    elif not os.path.isdir(path):
        # its not a folder?
        print("Path exists but its not a folder. Path must be directory: ", path)


def fetch_hiscores(username):
    # Fetch hiscore data from web
    s = requests.get(BASE_URL + username).content

    # Read csv html content into a dataframe and assign headers
    df = pd.read_csv(io.StringIO(s.decode('utf-8')), header=None, names=['Rank', 'Level', 'XP'])

    # Grab arrays corresponding to Rank and XP (level is a function of XP, no need to store)
    xp_data = df['XP']
    rank_data = df['Rank']

    # convert the two lists to a list of tuples
    # scores = list(map(list, zip(xp_data, rank_data)))

    scores = xp_data + rank_data

    return scores


def load_database(path, user):
    filename = get_filename(path, user)
    df = pd.read_csv(filename, index_col='Date')
    return df


def create_database(path, user):
    filename = get_filename(path, user)

    if os.path.isfile(filename):
        # database for this user exists, nothing to do here
        return

    cols = ['Date'] + ATTRIBUTES + ["rank_" + x for x in ATTRIBUTES]
    df = pd.DataFrame(columns=cols)

    print("Created new database for user", user)

    df.to_csv(filename, index=False)


def store_hiscores(path, user, time):
    # Should have already checked whether folder exists

    # TODO: instead of loading csv in every time, just append row to the end
    filename = get_filename(path, user)

    if not os.path.exists(filename):
        create_database(path, user)

    print("Fetching hiscores for", user)
    scores = fetch_hiscores(user)

    if APPEND:
        with open(filename, "a") as f:
            line = str(time) + ',' + ','.join(map(str, scores)) + '\n'
            f.write(line)

    else:
        df = load_database(path, user)

        # Create a new row for the database using the time as an index and list of tuples (xp, rank) as features
        scores = fetch_hiscores(user)

        df.loc[time] = scores

        print("Saving updated csv...")
        df.to_csv(filename, index=True)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: fetch.py data_path username1, username2, ... usernameN")

    else:
        path = sys.argv[1]
        users = sys.argv[2:]

        init(path)   # create databases for users if not exist

        time = pd.Timestamp.now().round('min')

        for user in users:
            store_hiscores(path, user, time)
