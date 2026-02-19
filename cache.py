# TODO: use musicbrainzngs for now, but redo for album.tagger.webservice
import musicbrainzngs
musicbrainzngs.set_useragent("perfvars plugin dev", "0.1", "davygrvy@pobox.com")
musicbrainzngs.set_rate_limit(0.5, 2)

release_group_cache = dict()
release_cache = dict()
event_cache = dict()
place_cache = dict()
area_cache = dict()


def clear_cache ():
    global release_group_cache,release_cache,event_cache,place_cache,area_cache
    
    release_group_cache = dict()
    release_cache = dict()
    event_cache = dict()
    place_cache = dict()
    area_cache = dict()
    

# try to be somewhat kind to our server while we abuse it

def get_release_group (mbid):
    if mbid in release_group_cache:
        return release_group_cache[mbid]
    else:
        release_group = musicbrainzngs.get_release_group_by_id(mbid,
                includes=['event-rels','place-rels','area-rels'])['release-group']
        release_group_cache[mbid] = release_group
        return release_group

def get_release (mbid):
    if mbid in release_cache:
        return release_cache[mbid]
    else:
        release = musicbrainzngs.get_release_by_id(mbid,
                includes=['release-groups','event-rels','place-rels','area-rels'])['release']
        release_cache[mbid] = release
        return release

def get_event (mbid):
    if mbid in event_cache:
        return event_cache[mbid]
    else:
        event = musicbrainzngs.get_event_by_id(mbid,
                includes=['annotation','place-rels','area-rels'])['event']
        event_cache[mbid] = event
        return event

def get_place (mbid):
    if mbid in place_cache:
        return place_cache[mbid]
    else:
        place = musicbrainzngs.get_place_by_id(mbid,
                includes=['annotation','place-rels','area-rels'])['place']
        event_cache[mbid] = place
        return place

def get_area (mbid):
    if mbid in area_cache:
        return area_cache[mbid]
    else:
        area = musicbrainzngs.get_area_by_id(mbid,
                includes=["area-rels"])['area']
        area_cache[mbid] = area
        return area
