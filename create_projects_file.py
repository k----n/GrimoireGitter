#!/usr/bin/env python3

# specify the projects separated by line below
gitter_rooms = """PerfectlySoft/Perfect
                mailboxer/mailboxer
                patchthecode/JTAppleCalendar
                aws/aws-sdk-go
                amberframework/amber
                shuup/shuup
                kriasoft/react-starter-kit
                """.split('\n')

import json

projects = {}

for room in gitter_rooms:
    if room != '':
        projects[room] = {
            "git": ["https://github.com/" + room],
            "github:issue": ["https://github.com/" + room],
            "github:pull": ["https://github.com/" + room],
            "github2:issue": ["https://github.com/" + room],
            "github2:pull": ["https://github.com/" + room],
            "gitter": [ "https://gitter.im/" + room],
        }

with open(' grimoirelab-settings/projects.json', 'w') as f:
    json.dump(projects, f, indent=4)