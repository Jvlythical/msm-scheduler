import pdb
from typing import List

from ..types import PlayerAvailability, PlayerExperience, PlayerInterest, PlayerStats
from ..models import Player


class PlayersBuilder():
    def __init__(self):
        self.availabilities = []
        self.experiences = []
        self.interests = []
        self.stats = []

    def with_availabilities(self, availabilites: List[PlayerAvailability]):
        self.availabilities = availabilites
        return self

    def with_experiences(self, experiences: List[PlayerExperience]):
        self.experiences = experiences
        return self

    def with_interests(self, interests: List[PlayerInterest]):
        self.interests = interests
        return self

    def with_stats(self, stats: List[PlayerStats]):
        self.stats = stats
        return self

    def build_availabilities_index(self):
        availabilities_index = {}
        # Ensure that players with the same identity have the same availability reference
        for availability in self.availabilities:
            times = []
            for day in availability:
                if day == 'Identity':
                    continue
                # Add these try/except blocks to let the old test.py run
                try:
                    hours = availability[day].replace(' ', '').split(',')
                except AttributeError:
                    hours = availability[day]

                if hours == ['']:
                    continue

                times += list(map(lambda hour: f"{day}.{hour}", hours))
            try:
                availabilities_index[availability['Identity']] = times
            except KeyError:
                availabilities_index[availability['identity']] = times
        return availabilities_index

    def build_experiences_index(self):
        experiences_index = {}
        for experience in self.experiences:
            clone = {**experience}
            del clone['name']
            experiences_index[experience['name']] = clone
        return experiences_index

    def build_interests_index(self):
        interests_index = {}
        for interest in self.interests:
            clone = {**interest}
            del clone['name']
            interests_index[interest['name']] = clone
        return interests_index

    def build(self):
        availabilities_index = self.build_availabilities_index()
        experiences_index = self.build_experiences_index()
        interests_index = self.build_interests_index()

        players = []
        for stat in self.stats:
            player = Player(
                **stat,
                availability=availabilities_index[stat['identity']],
                experience=experiences_index.get(stat['name']) or {},
                interests=interests_index.get(stat['name']) or {}
            )
            players.append(player)

        return players
