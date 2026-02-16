PLUGIN_NAME = "Performance Variables plugin"
PLUGIN_AUTHOR = "David Gravereaux <davygrvy@pobox.com>"
PLUGIN_DESCRIPTION = """
This plugin provides the 'recorded at' attributes for live releases
and recordings as variables for use in filenaming and tagger
scripts.  If the location is an event, 'held at' is used instead.
Two additional functions are provided that filter
Live-Bootleg-Style from release and recording disambig comments.

This plugin caches data requests, so it will be kind to our server ;)
"""
PLUGIN_VERSION = '0.1'
PLUGIN_API_VERSIONS = ['2.7', '2.8']
PLUGIN_LICENSE = "0BSD aka Public Domain"
PLUGIN_LICENSE_URL = "https://spdx.org/licenses/0BSD.html"
PLUGIN_USER_GUIDE_URL = "https://github.com/davygrvy/perfvars/wiki"

import re
from picard import config, log
from picard.metadata import register_album_metadata_processor, register_track_metadata_processor
from picard.script import register_script_function
from picard.plugin import PluginPriority
from picard.plugin.perfvars.perfvars import(
    add_album_performance_metadata
    add_track_performance_metadata
)

class release_cache(dict):
    def __missing__(self, key):
        return False

def process_album(tagger, metadata, release):
    if not release_cache[release['id']]:
        tagger.webservice.get_release_by_id(release['id'], on_result, includes=["area-rels","place-rels","event-rels"])
    else:
        add_album_performance_metadata(metadata, release_cache[release['id']])

    def on_result(response, reply, error):
        if not error:
            release_cache[response['release']['id']] = response['release']
            add_album_performance_metadata(metadata, response)


def filter_disambig(parser, disambig):
    return disambig

register_album_metadata_processor(process_album, priority=PluginPriority.HIGH)
#register_track_metadata_processor(process_track)
register_script_function(filter_disambig)
