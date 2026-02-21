from picard.webservice.api_helpers import MBAPIHelper

class PluginCachingWebService(MBAPIHelper):
    
    def __init__ (self, webservice):
        super().__init__(webservice)
        self.release_group_cache = dict()
        self.release_cache = dict()
        self.recording_cache = dict()
        self.event_cache = dict()
        self.place_cache = dict()
        self.area_cache = dict()
    
    def clear_cache(self):
        del self.release_group_cache,self.release_cache,self.recording,self.event_cache,self.place_cache,self.area_cache
        self.release_group_cache = dict()
        self.release_cache = dict()
        self.recording_cache = dict()
        self.event_cache = dict()
        self.place_cache = dict()
        self.area_cache = dict()
    
    def get_release(self,mbid):
        # if pending condition.wait
        #    if not error return self.release_cache[mbid]
        # else
        #    set pending
        #    self._get_by_id('release',mbid,on_complete,'inc=release-groups+event-rels+place-rels+area-rels')
        #    
        # def on_complete(response, reply, error):
        #    if not error
        #       self.release_cache[mbid] = _JSON_MB_Parse(response)
        #       unset pending
        #       condition.set ?
        pass
    
    def get_release_group(self,mbid):
        pass
    
    def get_recording(self,mbid):
        pass
    
    def get_event(self,mbid):
        pass
    
    def get_place(self,mbid):
        pass
    
    def get_area(self,mbid):
        pass

    def _JSON_MB_Parse(rawtext):
        return []

# to be set from the register_album_metadata_processor callback
ourWS = PluginCachingWebService(album.tagger.webservice)
event = ourWS.get_event(mbid)
