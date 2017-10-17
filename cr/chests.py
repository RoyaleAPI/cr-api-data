"""
Generate chest cycle
"""
import csv
import json
import os
import re

class Chests:

    def __init__(self, config):
        self.config = config

    def run(self):
        """Generate chests.json"""
        csv_path = os.path.join(self.config.csv.base, self.config.csv.path.chest_order)

        chests = {}

        with open(csv_path) as f:
            reader = csv.DictReader(f)

            current_name = ''
            for i, row in enumerate(reader):
                if i > 0:
                    name = row["Name"]
                    if len(name):
                        chests[name] = []
                        current_name = name

                    if current_name == 'MainCycle':
                        chests[current_name].append(row["Chest"])
                    else:
                        chests[current_name].append({
                            "chest": row["Chest"],
                            "quest_threshold": int(row["QuestThreshold"]),
                            "arena_threshold": row["ArenaThreshold"],
                            "one_time": bool(row["OneTime"])
                        })

        json_path = os.path.join(self.config.json.base, self.config.json.chest_order)
        with open(json_path, 'w') as f:
            json.dump(chests, f, indent=4)

        print(json_path)
