# Fauxcasts

## Rationale

Libraries often have large collections of audiobooks on CDs. However, I don't listen to anything on CDs anymore—I actually only have one device with an optical drive anymore (an ancient Mac Mini). 

I use an iPhone or iPad to listen to everything, and getting these CDs onto these devices is trivial. However, playing audiobooks through Apple's native music app feels somewhat limited. I'm a huge fan of modern podcasting apps like [Overcast](https://overcast.fm/) that speed up podcasts intelligibly (Smart Speed!). Wouldn't it be fantastic to listen to CD-based audiobooks in [Overcast](https://overcast.fm/), [Downcast](http://www.downcastapp.com/),[Pocketcasts](http://www.shiftyjelly.com/pocketcasts), or whatever your favorite app is?

This little script lets you do that!

## Installation

The script requires a few external libraries. Install these using this command:

	pip install -r requirements.txt

Or for Python 3:

	pip3 install -r requirements.txt

## Usage

1. Rip the tracks as MP3 files from the audiobook CDs, following this naming convention:

		n-xx Name of the track.mp3

	Where `n` is the disc number and `xx` is the track number (with a leading zero. For example:

		2-03 Act III Scene II.mp3

2. Upload this folder and a cover image to some public server somewhere (even Dropbox should work) and take note of the URL.
3. Edit the variables at the top of the `generate_feed.py` and run it from a terminal window:

		python3 generate_feed.py

4. Upload the resulting `feed.rss` file to the same folder as the MP3 files and the cover image.
5. Subscribe to your new feed using your favorite podcast app and enjoy a faster, better sounding book.
6. (For copyright reasons, you probably don't want to share the feed. Keep it secret. Keep it safe.)
