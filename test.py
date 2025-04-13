"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""
from datetime import datetime
from collections import defaultdict
import unittest
from main import ItineraryBuilder
from concerts_data import get_all_concerts

class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""

    def setUp(self):
        """Set up for the tests."""
        self.builder = ItineraryBuilder()

        self.all_concerts = get_all_concerts()

    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here.

    def test_manual_1(self):
        """First manually written test case."""

        self.setUp()
        concerts = self.builder.build_itinerary(self.all_concerts)

        valid_list = True
        # Check if all artists are found exactly once including those without a concert
        # Then check that artists missing concert have the correct values
        for a in self.all_concerts:

            found = False
            for c in concerts:

                #Check valid entry for missing artist
                if c.location == "No concert":
                    if not (c.date is None and c.longitude is None and c.latitude is None):
                        valid_list = False

                if c.artist == a.artist:
                    found = True
                    break

            if not found:
                valid_list = False

        self.assertTrue(valid_list and concerts)

    def test_manual_2(self):
        """Second manually written test case."""
        self.setUp()
        concerts = self.builder.build_itinerary(self.all_concerts)

        valid_order = True

        #Using todays date as lowest possible value
        first = datetime.strptime('2025-04-13', '%Y-%m-%d')

        for c in concerts:

            if c.date is None:
                continue

            second = datetime.strptime(c.date, '%Y-%m-%d')

            #Check if all concerts occur after each other in the itinerary
            if first > second:
                valid_order = False
                break

            first = second

        self.assertTrue(valid_order and concerts)

    def test_manual_3(self):
        """Third manually written test case."""
        self.setUp()
        concerts = self.builder.build_itinerary(self.all_concerts)

        #Check for duplicate concerts
        unique_entries = True
        for a in self.all_concerts:
            artist_found = False
            for c in concerts:
                if a.artist == c.artist:
                    if artist_found:
                        unique_entries = False
                        break

                    artist_found = True

        #check that concerts are earliest possible ones
        earliest_planned = True
        for c in concerts:
            earliest = datetime.strptime('2100-01-01', '%Y-%m-%d')
            if c.date is None:
                continue

            for a in self.all_concerts:

                if c.artist == a.artist:
                    if datetime.strptime(a.date, '%Y-%m-%d') < earliest:
                        earliest = datetime.strptime(a.date, '%Y-%m-%d')

            if datetime.strptime(c.date, '%Y-%m-%d') != earliest:
                earliest_planned = False

        self.assertTrue(unique_entries and earliest_planned and concerts)

    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.

    def test_assisted_1(self):
        '''First assisted test case'''
        self.setUp()
        concerts = self.builder.build_itinerary(self.all_concerts)
        valid_contents = True

        for i, current in enumerate(concerts):
            seen_dates = set()

            # Check for duplicate dates
            if current.date in seen_dates:
                valid_contents = False

            seen_dates.add(current.date)

            # Skip first concert
            # (no previous concert to compare with or if entry represents a missing artist)
            if i == 0 or current.date is None:
                continue

            prev = concerts[i - 1]

            # Get all concerts that occurr on the same dates
            same_day_options = [c for c in self.all_concerts if c.date == current.date]

            # If no other options exist, skip
            if not same_day_options:
                continue

            # Calculate distance from previous concert to each option
            distances = {
            c: self.builder.globe_distance(prev.latitude, prev.longitude, c.latitude, c.longitude)
            for c in same_day_options
            }

            # Find the concert with the closest distance
            closest = min(distances, key=distances.get)

            if current != closest:
                valid_contents = False

        self.assertTrue(valid_contents)

    def test_assisted_2(self):
        '''Second assisted test case'''
        self.setUp()
        concerts = self.builder.build_itinerary(self.all_concerts)

        valid_contents = True

        # Check if the objects contain the correct attributes
        for _, concert in enumerate(concerts):
            if not hasattr(concert, 'artist'):
                valid_contents = False
            if not hasattr(concert, 'date'):
                valid_contents = False
            if not hasattr(concert, 'location'):
                valid_contents = False

        self.assertTrue(valid_contents)

    def test_assisted_3(self):
        '''Thirds assisted test case'''
        self.setUp()
        itinerary = self.builder.build_itinerary(self.all_concerts)

        valid_contents = True

        # Count how many concerts each artist has in total
        artist_counts = defaultdict(int)
        for concert in self.all_concerts:
            artist_counts[concert.artist] += 1

        # Index concerts by date
        concerts_by_date = defaultdict(list)
        for concert in self.all_concerts:
            concerts_by_date[concert.date].append(concert)

        # Index itinerary by date
        itinerary_by_date = {concert.date: concert for concert in itinerary}

        for date, concerts_on_date in concerts_by_date.items():
            solo_concerts = [c for c in concerts_on_date if artist_counts[c.artist] == 1]

            # If there are solo artist concerts on the date
            if solo_concerts:
                # Concert in the itinerary for that date must be from one of them
                concert_in_itinerary = itinerary_by_date.get(date)
                if not concert_in_itinerary:
                    valid_contents = False
                if concert_in_itinerary.artist not in {c.artist for c in solo_concerts}:
                    valid_contents = False

        self.assertTrue(valid_contents)

if __name__ == "__main__":
    unittest.main()
