import pip._vendor.requests as requests

def fetch_ct_tiles(ct_id='0'):
    ct_id = str(ct_id)
    
    url = "https://data.ninjakiwi.com/btd6/ct/"
    ct_resp = requests.get(url).json()
    if ct_resp['error'] is not None or ct_resp['success'] is False:
        print("CT category unavailable at the moment")
        exit()

    if ct_id == '0':
        ct_id = ct_resp['body'][0]['id']

    ct = url + ct_id + "/tiles"
    ct_resp = requests.get(ct).json()
    tiles = ct_resp['body']['tiles']
    return tiles

def fetch_race_tiles():
    tiles = fetch_ct_tiles()
    banners = []
    relics = []
    regular = []
    for tile in tiles:
        if tile['gameType'] == "Race":
            if tile['type'] == "Regular":
                regular.append(tile['id'])
            elif tile['type'] == "Banner":
                banners.append(tile['id'])
            else:
                relics.append(tile['id'])
    return sorted(regular), sorted(banners), sorted(relics)

def fetch_relevant_relics():
    tiles = fetch_ct_tiles()
    race_relics = []
    # non race relics will be an array containing all relics that are not applicable in race, mostly powers
    non_race_relics = ['CamoTrap','ElDorado', 'GlueTrap', 'HeroBoost', 'MoabMine', 'MonkeyBoost', 'RoadSpikes', 'SuperMonkeyStorm', 'TechBot', 'Thrive']
    for tile in tiles:
        if tile['type'][:5] == "Relic" and tile['type'][8:] not in non_race_relics:
            race_relics.append(tile['type'][8:])
    return race_relics

