release_group_cache = dict()
release_cache = dict()
event_cache = dict()
place_cache = dict()
area_cache = dict()

# try to be somewhat kind to our server while we abuse it
def get_release_group (ws, mbid):
    
    # if pending condition.wait
    #    if not error return release_group_cache[mbid]
    # else
    #    set pending
    #    ws.get_release_group_by_id(...,on_complete,...)
    #    
    # def on_complete(response, reply, error):
    #    if not error
    #       release_group_cache[mbid] = response['release_group']
    #       unset pending
    #       condition.set ?
    pass

def get_release (mbid):
    pass

def get_event (mbid):
    pass

def get_place (mbid):
    pass

def get_area (mbid):
    pass
