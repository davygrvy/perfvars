import musicbrainznsg
musicbrainzngs.set_useragent("perfvars plugin dev", "0.1", "davygrvy@pobox.com")

def add_album_performance_metadata(metadata, release_mbid):
    # re-get the release with our special includes
    release = musicbrainzngs.get_release_by_id(release_mbid,
                includes=['event-rels','place-rels','area-rels'])['release']
    
    # events take precidence in the heirarchy followed by place then area.
    if 'event-relation-list' in release:
        x = 0
        for relation in release['event-relation-list']:
            if relation['type-id'] == '4dda6e40-14af-46bb-bb78-ea22f4a99dfa':
                # 'recorded at' for an event
                metadata[f"~release_event{x+1}_name"] = relation['event']['name']
                # get event
                event = musicbrainzngs.get_event_by_id(relation['event']['id'],
                        includes=['place-rels','area-rels'])['event']
                if 'place-relation-list' in event:
                    y = 0
                    for place_rel in event['place-relation-list']:
                        if 'target-credit' in place_rel:
                            metadata[f"~release_event{x+1}_location{y+1}"] = place_rel['target-credit']
                            metadata[f"~release_event{x+1}_location{y+1}_unwound"] = ", ".join([place_rel['target-credit'], unwindPlace(place_rel['place']['id'])[1]])
                        else:
                            metadata[f"~release_event{x+1}_location{y+1}"] = place_rel['place']['name']
                            metadata[f"~release_event{x+1}_location{y+1}_unwound"] = ", ".join(unwindPlace(place_rel['place']['id']))
                        y +=1
                
                x += 1
        
        return
    
    
                if 'target-credit' in place:
                    metadata[f"~release_event{i}_location"] = place['target-credit']
                else:
                    metadata[f"~release_event{i}_location"] = place['name']
                metadata[f"~release_event{i}_location_unwound"] = unwindPlace(place['id'])[i]

    event = musicbrainzngs.get_event_by_id(release['event-relation-list'][0]['event']['id'], includes=['place-rels','area-rels'])['event']
    place = musicbrainzngs.get_place_by_id(event['place-relation-list'][0]['place']['id'], includes=['area-rels'])['place']
    area = musicbrainzngs.get_area_by_id(place['area']['id'], includes=['area-rels'])['area']



", ".join([place['name'], ", ".join(unwindArea(area['id']))])

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

