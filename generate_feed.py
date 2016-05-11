#!/usr/bin/env python3
import glob
import os
import re
from datetime import datetime, timedelta
from feedgen.feed import FeedGenerator
from mutagen.mp3 import MP3
import pytz


# ----------------------------------
# Configure variables for the feed
# ----------------------------------
# Base URL for where the podcast files and feed will ultimately live
base_url = 'http://files.example.com/fauxcasts/book_name/'

# Name for the RSS file
feed_name = 'feed.rss'
feed_url = base_url + feed_name

# Information about the podcast
feed_title = 'Podcast title'
feed_description = "Description of podcast"
feed_author = 'Some name here'
feed_author_email = 'blah@example.com'
feed_homepage = 'http://www.example.com'

# Name of the pre-uploaded podcast cover image
cover_image = base_url + 'cover.jpg'

# Absolute or relateive path to MP3 files on your local computer
#
# NB: Use the *.mp3 syntax to select and parse all MP3s in the folder
# Also NB: Make sure each file follows this naming convention:
#   n-xx Name of the track.mp3
# where `n` is the disc number (e.g. 1), and `xx` is the track number (e.g. 07)
#   Example: 2-14 Act IV Scene iii.mp3
#
# If you want, you can change the regular expression that parses these
# filenames below at `track_name_raw = re.match(...)`
# local_location = '/path/to/ripped/mp3s/*.mp3'
local_location = 'path/to/mp3_files/*.mp3'


# ----------------------
# Generate actual feed
# ----------------------
# Generate feed
fg = FeedGenerator()
fg.load_extension('podcast')

# Add descriptive variables to the feed
fg.id(feed_url)
fg.title(feed_title)
fg.author({'name': feed_author, 'email': feed_author_email})
fg.link(href=feed_homepage, rel='alternate')
fg.logo(cover_image)
fg.subtitle(feed_description)
fg.link(href=feed_url, rel='self')
fg.language('en')
fg.podcast.itunes_block(True)
fg.podcast.itunes_complete(True)


# Loop through each MP3 and add it to the feed as an episode
for i, track in enumerate(sorted(glob.glob(local_location))):
    # Some podcast players respect the itunes_order attribute, which is set
    # below, but many only look at the date and time of the episode. So, here
    # we pretend that the first episode happened 7 days ago, and each
    # subsequent episode is released 1 hour later.
    episode_date = (datetime.now(tz=pytz.utc) -
                    timedelta(days=7) +
                    timedelta(hours=i + 1))

    # Get the file size
    file_size = os.path.getsize(track)

    # Remove the disk and track numbers from the file names and use just the
    # title as the episode name
    track_filename = os.path.basename(track)
    track_name_raw = re.match(r"\d-\d{2} (.*)\.mp3", track_filename)
    track_name = track_name_raw.group(1)

    # Get the duration
    audio = MP3(track)
    m, s = divmod(audio.info.length, 60)  # Convert seconds to h:m:s
    h, m = divmod(m, 60)
    if h == 0:
        duration = "%02d:%02d" % (m, s)
    else:
        duration = "%d:%02d:%02d" % (h, m, s)

    # Generate entry
    fe = fg.add_entry()
    fe.guid(base_url + track_filename)
    fe.link({'href': base_url + track_filename})
    fe.title(track_name)
    fe.description(track_name)
    fe.published(episode_date)
    fe.enclosure(base_url + track_filename, str(file_size), 'audio/mpeg')
    fe.podcast.itunes_order(i + 1)
    fe.podcast.itunes_duration(duration)

# Write the feed to a file
fg.rss_file(feed_name, pretty=True)
