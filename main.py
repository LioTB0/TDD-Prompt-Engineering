"""
Concert Itinerary Builder

This module provides functionality to build an itinerary of upcoming concerts.
"""

from collections import defaultdict
import math
from datetime import datetime

class Concert:
    """
    Represents a concert event.
    
    Attributes:
        artist (str): The name of the artist performing.
        date (str): The date of the concert in 'YYYY-MM-DD' format.
        location (str): The location where the concert will take place.
        latitude (float): Latitude coordinate of the concert location.
        longitude (float): Longitude coordinate of the concert location.
    """

    def __init__(self, artist, date, location, latitude, longitude):
        self.artist = artist
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

class ItineraryBuilder:
    """
    A class to build concert itineraries. 
    """

    def globe_distance(self, lat1, lon1, lat2, lon2):
        '''Function to compare distances on earth, double checked to make sure ChatGPT got it right'''
        earth_radius = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        distance = earth_radius * 2 * math.asin(math.sqrt(a))
        return distance

    def build_itinerary(self, concerts):
        """
        A function to build concert itineraries. 
        """

        # Count concerts per artist
        artist_counts = defaultdict(int)
        for concert in concerts:
            artist_counts[concert.artist] += 1

        all_artists = set()
        # Group concerts by date and collect all artists
        concerts_by_date = defaultdict(list)
        for concert in concerts:
            concerts_by_date[concert.date].append(concert)
            all_artists.add(concert.artist)

        # Sort all dates
            sorted_dates = sorted(concerts_by_date.keys(), key=lambda d: datetime.strptime(d, '%Y-%m-%d'))

        i_list = []
        included_artists = set()
        last_concert = None


        for date in sorted_dates:
            same_day_concerts = concerts_by_date[date]

            # Remove concerts by artists already included
            filtered = [c for c in same_day_concerts if c.artist not in included_artists]
            if not filtered:
                continue

            # Prioritize solo artists
            solo = [c for c in filtered if artist_counts[c.artist] == 1]

            if solo:
                # If multiple solo artists, choose the closest to previous concert
                chosen = min(solo, key=lambda c: self.globe_distance(last_concert.latitude, last_concert.longitude, c.latitude, c.longitude)) if last_concert else solo[0]
            else:
                # No solo artists → pick closest to previous
                chosen = min(filtered, key=lambda c: self.globe_distance(last_concert.latitude, last_concert.longitude, c.latitude, c.longitude)) if last_concert else filtered[0]

            i_list.append(chosen)
            included_artists.add(chosen.artist)
            last_concert = chosen

        missing_artists = all_artists - included_artists
        for artist in missing_artists:
            i_list.append(Concert(artist=artist, date=None, location="No concert", latitude=None, longitude=None))

        return i_list

if __name__ == "__main__":
    from concerts_data import get_all_concerts

    all_concerts = get_all_concerts()
    builder = ItineraryBuilder()
    itinerary = builder.build_itinerary(all_concerts)

    for c in itinerary:
        if c.date is None:
            print(c.artist + ' has no concert in this itinerary. :(')
        else:
            print(c.artist + ' on '
                + c.date + ' in '
                + c.location + ' at: '
                + str(c.longitude) + ' '
                + str(c.latitude) + '\n')
