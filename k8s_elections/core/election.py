# Copyright 2020 Manish Sahani
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author(s):         Manish Sahani <rec.manish.sahani@gmail.com>

from k8s_elections.core import schulze_d, schulze_p, schulze_rank


class Election:
    def __init__(self, candidates, ballots, no_winners):
        self.candidates = candidates
        self.ballots = ballots
        self.no_winners = no_winners
        self.d = {}
        self.p = {}

    def schulze(self):
        self.d = schulze_d(self.candidates, self.ballots)
        self.p = schulze_p(self.candidates, self.d)
        self.ranks = schulze_rank(self.candidates, self.p, self.no_winners)

        return self

    @ staticmethod
    def build(candidates, ballots, no_winners):
        candidates = [c['ID'] for c in candidates]
        pref = {}

        for b in ballots:
            if b.voter not in pref.keys():
                pref[b.voter] = []
            if b.rank == 100000000:
                continue
            pref[b.voter].append((b.candidate, int(b.rank)))

        return Election(candidates, pref, no_winners)

    @ staticmethod
    def from_csv(df, no_winners):
        candidates = list(df.columns)
        ballots = {}

        for v, row in df.iterrows():
            ballots[v] = []
            for c in candidates:
                if row[c] == 'No opinion':
                    continue
                ballots[v].append((c, int(row[c])))

        return Election(candidates, ballots, no_winners)
