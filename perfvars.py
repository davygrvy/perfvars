import musicbrainznsg
musicbrainzngs.set_useragent("perfvars plugin dev", "0.1", "davygrvy@pobox.com")
musicbrainzngs.set_rate_limit(0.5, 2)

class Count:
  def __init__(self):
   a = 1
  def incr()
   a += 1
  def val()
   return a


def add_album_performance_metadata(metadata, release_mbid):
    # re-get the release with our special includes
    release = musicbrainzngs.get_release_by_id(release_mbid,
            includes=['release-groups','event-rels','place-rels','area-rels'])['release']
    
    Count count()
    
    # events take precidence in the heirarchy followed by place then area.
    if 'event-relation-list' in release:
        processEventRelations(release['event-relation-list'], metadata, count)
        return
    
    release_group = musicbrainzngs.get_release_group_by_id(release['release-group']['id'],
            includes=['event-rels','place-rels','area-rels'])['release-group']
    
    # check if there is an event relationships on the release-group
    # we do this second as release events take precidence
    if 'event-relation-list' in release_group:
        processEventRelations(release_group['event-relation-list'], metadata, count)
        return
    
    # any place relations?
    if 'place-relation-list' in release:
        processPlaceRelations(release['place-relation-list'], metadata, count)
        return
    
    # any place relations on the release-group?
    if 'place-relation-list' in release_group:
        processPlaceRelations(release_group['place-relation-list'], metadata, count)
        return
    
    # any area relations?
    if 'area-relation-list' in release:
        processAreaRelations(release['area-relation-list'], metadata, count)
        return
    
    # any area relations on the release-group?
    if 'area-relation-list' in release_group:
        processAreaRelations(release_group['area-relation-list'], metadata, count)
        return
    
    return


def processEventRelations(event_relation_list, metadata, count):
    for relation in event_relation_list:
        if relation['type-id'] == '4dda6e40-14af-46bb-bb78-ea22f4a99dfa':
            # 'recorded at' for an event
            metadata[f"~release_event{count.val()}_name"] = relation['event']['name']
            if relation['event']['life-span']['begin'] == relation['event']['life-span']['end']:
                metadata[f"~release_event{count.val()}_date"] = relation['event']['life-span']['begin']
            else:
                metadata[f"~release_event{count.val()}_date"] = f"{relation['event']['life-span']['begin']} - {relation['event']['life-span']['end']}"
            
            # get event
            event = musicbrainzngs.get_event_by_id(relation['event']['id'],
                    includes=['place-rels','area-rels'])['event']
            
            if 'place-relation-list' in event:
                processPlaceRelations(event['place-relation-list'], metadata, count)


def processPlaceRelations(place_relation_list, metadata, count):
    for place_rel in place_relation_list:
        if place_rel['type-id'] == '3b1fae9f-5b22-42c5-a40c-d1e5c9b90251':
            # 'recorded at' for a place
            if place_rel['begin'] == place_rel['end']:
                metadata[f"~release_performance{count.val()}_date"] = place_rel['begin']
            else:
                metadata[f"~release_performance{count.val()}_date"] = f"{place_rel['begin']} - {place_rel['end']}"
            if 'target-credit' in place_rel:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['target-credit']
                metadata[f"~release_performance{count.val()}_location_unwound"] = ", ".join([place_rel['target-credit'], unwindPlace(place_rel['place']['id'])[1]])
            else:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['place']['name']
                metadata[f"~release_performance{count.val()}_location_unwound"] = ", ".join(unwindPlace(place_rel['place']['id']))
            count.incr()


def processAreaRelations(area_relation_list, metadata, count):
    for area_rel in area_relation_list:
        if area_rel['type-id'] == '':
            # 'recorded in' for an area
            if area_rel['begin'] == area_rel['end']:
                metadata[f"~release_performance{count.val()}_date"] = area_rel['begin']
            else:
                metadata[f"~release_performance{count.val()}_date"] = f"{area_rel['begin']} - {area_rel['end']}"
            if 'target-credit' in area_rel:
                metadata[f"~release_performance{count.val()}_location"] = area_rel['target-credit']
                metadata[f"~release_performance{count.val()}_location_unwound"] = ", ".join([area_rel['target-credit'], unwindArea(area_rel['area']['id'])[1]])
            else:
                metadata[f"~release_performance{count.val()}_location"] = place_rel['area']['name']
                metadata[f"~release_performance{count.val()}_location_unwound"] = ", ".join(unwindPlace(area_rel['area']['id']))
            count.incr()


def unwindPlace(mbid):
    place = musicbrainzngs.get_place_by_id(mbid, includes=['place-rels','area-rels'])['place']
    if 'place-relation-list' in place:
        for relation in place['place-relation-list']:
            if relation['direction'] == 'backward' and relation['type-id'] == 'ff683f48-eff1-40ab-a58f-b128098ffe92':
                return [place['name'], ", ".join(unwindPlace(relation['place']['id']))]
    
    # when no backward relation exists, we are at the top, unwind area next                
    return [place['name'], ", ".join(unwindArea(place['area']['id']))]


def unwindArea(mbid):
    # town, county, municipality, state (subdivision), country
    area = musicbrainzngs.get_area_by_id(mbid, includes=["area-rels"])['area']
    if 'area-relation-list' in area:
       for relation in area['area-relation-list']:
          if relation['direction'] == 'backward' and relation['type-id'] == 'de7cc874-8b1b-3a05-8272-f3834c968fb7':
              # skip County or Municipality
             if area['type'] == ('County' or 'Municipality'):
                return unwindArea(relation['area']['id'])
             else:
                return [area['name'], ", ".join(unwindArea(relation['area']['id']))]
    
    # when no backward relation exists, we are at the top and done
    return [area['iso-3166-1-code-list'][0]]
