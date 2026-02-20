from picard.webservice.api_helpers import APIHelper

class PluginCachingWebService(APIHelper):
    def __init__ (self, webservice):
       super().__init__(webservice)
       self.release_group_cache = dict()
       self.release_cache = dict()
       self.event_cache = dict()
       self.place_cache = dict()
       self.area_cache = dict()
    def clear_cache(self):
       del self.release_group_cache,self.release_cache,self.event_cache,self.place_cache,self.area_cache
       self.release_group_cache = dict()
       self.release_cache = dict()
       self.event_cache = dict()
       self.place_cache = dict()
       self.area_cache = dict()
    def get_release_by_id(self,mbid):
        # if pending condition.wait
        #    if not error return self.release_group_cache[mbid]
        # else
        #    set pending
        #    ws.get_release_group_by_id(...,on_complete,...)
        #    
        # def on_complete(response, reply, error):
        #    if not error
        #       self.release_group_cache[mbid] = response['release_group']
        #       unset pending
        #       condition.set ?
       pass
    def get_release_group_by_id(self,mbid):
       pass
    def get_event_by_id(self,mbid):
       pass
    def get_place_by_id(self,mbid):
       pass
    def get_area_by_id(self,mbid):
       pass

ourWS = PluginCachingWebService(album.tagger.webservice)
event = ourWS.get_event_by_id(mbid)
