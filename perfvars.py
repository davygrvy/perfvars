import musicbrainznsg
musicbrainzngs.set_useragent("perfvars plugin dev", "0.1", "davygrvy@pobox.com")
musicbrainzngs.set_rate_limit(0.5, 2)

class Count:
  def __init__(self):
   self.a = 1
  def incr(self):
   self.a += 1
  def val(self):
   return self.a


def add_album_performance_metadata(metadata, release_mbid):
    # re-get the release with our special includes
    release = musicbrainzngs.get_release_by_id(release_mbid,
            includes=['release-groups','event-rels','place-rels','area-rels'])['release']
    
    count = Count()
    just_once = 1
    
    while(just_once):
        just_once = 0
        
        # events take precidence in the heirarchy followed by place then area.
        if 'event-relation-list' in release:
            processEventRelations(release['event-relation-list'], metadata, count)
            break
        
        release_group = musicbrainzngs.get_release_group_by_id(release['release-group']['id'],
                includes=['event-rels','place-rels','area-rels'])['release-group']
    
        # check if there is an event relationships on the release-group
        # we do this second as release events take precidence
        if 'event-relation-list' in release_group:
            processEventRelations(release_group['event-relation-list'], metadata, count)
            break
        
        # any place relations?
        if 'place-relation-list' in release:
            processPlaceRelations(release['place-relation-list'], metadata, count)
            break
        
        # any place relations on the release-group?
        if 'place-relation-list' in release_group:
            processPlaceRelations(release_group['place-relation-list'], metadata, count)
            break
        
        # any area relations?
        if 'area-relation-list' in release:
            processAreaRelations(release['area-relation-list'], metadata, count)
            break
    
        # any area relations on the release-group?
        if 'area-relation-list' in release_group:
            processAreaRelations(release_group['area-relation-list'], metadata, count)
            break
    
    metadata["~release_performance_count"] = count.val()-1
    return


def processEventRelations(event_relation_list, metadata, count):
    for event_rel in event_relation_list:
        if event_rel['type-id'] in ['4dda6e40-14af-46bb-bb78-ea22f4a99dfa','a64a9085-505b-4588-bff9-214d7dda61c4']:
            # 'recorded at' on a release https://musicbrainz.org/relationship/4dda6e40-14af-46bb-bb78-ea22f4a99dfa
            # 'performed at' on a release-group https://musicbrainz.org/relationship/a64a9085-505b-4588-bff9-214d7dda61c4
            metadata[f"~release_performance{count.val()}_name"] = event_rel['event']['name']
            if event_rel['event']['life-span']['begin'] == event_rel['event']['life-span']['end']:
                metadata[f"~release_performance{count.val()}_date"] = event_rel['event']['life-span']['begin']
            else:
                metadata[f"~release_performance{count.val()}_date"] = (
                        f"{event_rel['event']['life-span']['begin']} - {event_rel['event']['life-span']['end']}")
            
            if 'time' in event_rel['event']:
                metadata[f"~release_performance{count.val()}_time"] = event_rel['event']['time']
                
            # now get the event for a deeper look
            event = musicbrainzngs.get_event_by_id(event_rel['event']['id'],
                    includes=['place-rels','area-rels'])['event']
            
            if 'place-relation-list' in event:
                processPlaceRelations(event['place-relation-list'], metadata, count)
            
            # not likely 
            if 'area-relation-list' in event:
                processAreaRelations(event['area-relation-list'], metadata, count)


def processPlaceRelations(place_relation_list, metadata, count):
    for place_rel in place_relation_list:
        if place_rel['type-id'] == 'e2c6f697-07dc-38b1-be0b-83d740165532':
            # 'held at' on an event https://musicbrainz.org/relationship/e2c6f697-07dc-38b1-be0b-83d740165532
            if 'target-credit' in place_rel:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['target-credit']
                metadata[f"~release_performance{count.val()}_location_unwound"] = (
                        ", ".join([place_rel['target-credit'], unwindPlace(place_rel['place']['id'])[1]]))
            else:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['place']['name']
                metadata[f"~release_performance{count.val()}_location_unwound"] = (
                        ", ".join(unwindPlace(place_rel['place']['id'])))
            count.incr()
            continue
        
        if place_rel['type-id'] in ['3b1fae9f-5b22-42c5-a40c-d1e5c9b90251','a64a9085-505b-4588-bff9-214d7dda61c4']:
            # 'recorded at' on a release https://musicbrainz.org/relationship/3b1fae9f-5b22-42c5-a40c-d1e5c9b90251
            # 'recorded at' on a release-group https://musicbrainz.org/relationship/a64a9085-505b-4588-bff9-214d7dda61c4
            if place_rel['begin'] == place_rel['end']:
                metadata[f"~release_performance{count.val()}_date"] = place_rel['begin']
            else:
                metadata[f"~release_performance{count.val()}_date"] = f"{place_rel['begin']} - {place_rel['end']}"
            if 'target-credit' in place_rel:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['target-credit']
                metadata[f"~release_performance{count.val()}_location_unwound"] = (
                        ", ".join([place_rel['target-credit'], unwindPlace(place_rel['place']['id'])[1]]))
            else:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['place']['name']
                metadata[f"~release_performance{count.val()}_location_unwound"] = (
                        ", ".join(unwindPlace(place_rel['place']['id'])))
            count.incr()


def processAreaRelations(area_relation_list, metadata, count):
    for area_rel in area_relation_list:
        if area_rel['type-id'] in ['354043e1-bdc2-4c7f-b338-2bf9c1d56e88','542f8484-8bc7-3ce5-a022-747850b2b928']:
            # 'recorded in' on a release https://musicbrainz.org/relationship/354043e1-bdc2-4c7f-b338-2bf9c1d56e88
            # 'held in' on an event https://musicbrainz.org/relationship/542f8484-8bc7-3ce5-a022-747850b2b928
            if area_rel['begin'] == area_rel['end']:
                metadata[f"~release_performance{count.val()}_date"] = area_rel['begin']
            else:
                metadata[f"~release_performance{count.val()}_date"] = f"{area_rel['begin']} - {area_rel['end']}"
            if 'target-credit' in area_rel:
                metadata[f"~release_performance{count.val()}_location"] = area_rel['target-credit']
                metadata[f"~release_performance{count.val()}_location_unwound"] = (
                        ", ".join([area_rel['target-credit'], unwindArea(area_rel['area']['id'])[1]]))
            else:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['area']['name']
                metadata[f"~release_performance{count.val()}_location_unwound"] = (
                        ", ".join(unwindArea(area_rel['area']['id'])))
            count.incr()


def unwindPlace(mbid):
    place = musicbrainzngs.get_place_by_id(mbid, includes=['place-rels','area-rels'])['place']
    if 'place-relation-list' in place:
        for place_rel in place['place-relation-list']:
            if place_rel['direction'] == 'backward' and place_rel['type-id'] == 'ff683f48-eff1-40ab-a58f-b128098ffe92':
                return [place['name'], ", ".join(unwindPlace(place_rel['place']['id']))]
    
    # when no backward relation exists, we are at the top, unwind area next                
    return [place['name'], ", ".join(unwindArea(place['area']['id']))]


def unwindArea(mbid):
    # town/city, district, county, municipality, subdivision (state), country
    area = musicbrainzngs.get_area_by_id(mbid, includes=["area-rels"])['area']
    if 'area-relation-list' in area:
       for area_rel in area['area-relation-list']:
          if (area_rel['direction'] == 'backward' and 
                  area_rel['type-id'] == 'de7cc874-8b1b-3a05-8272-f3834c968fb7' and
                  area_rel['area']['type'] != 'Island'):
             if area['type'] in ['County','Municipality']:
                # skip County or Municipality
                return unwindArea(area_rel['area']['id'])
             elif area['type'] == 'Subdivision':
                # use abreviation for Subdivision, if exist
                if 'iso-3166-2-code-list' in area:
                    return [area['iso-3166-2-code-list'][0], ", ".join(unwindArea(area_rel['area']['id']))]
                else:
                    return [area['name'], ", ".join(unwindArea(area_rel['area']['id']))]
             else:
                return [area['name'], ", ".join(unwindArea(area_rel['area']['id']))]
    
    # when no backward relation exists, we are at the top and done
    return [area['iso-3166-1-code-list'][0]]
