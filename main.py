# inspired by HellSec : https://github.com/rpie/MCInfo
# recreated and turned into a library by vvs [#SpookySquad]

import requests, sys, json 
from colorama import Fore

g = Fore.GREEN
w = Fore.WHITE
information = []
usernames = []
available = []

class MCInfo:
    def __init__(self, username):
        self.username = username

    def getAccountUID(account: str):
        JSONUID = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{account}')
        return JSONUID.json()['id']

    def getPastUsers(UID: str):
        json = requests.get(f'https://api.mojang.com/user/profiles/{UID}/names')
        array = []
        for x in range(len(json.json())):
            array.append(json.json()[x]['name'])
        return array

    def getMigrated(UID: str):
        r = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{UID}')
        if r.status_code == 200:
            return True
        else:
            return False

    def SearchUser(username):
        uid = MCInfo.getAccountUID(username)
        PastNames = MCInfo.getPastUsers(uid)
        migrated = MCInfo.getMigrated(uid)
        information.append(("PastNames", PastNames))
        for user in information[0][1]:
            r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{user}')
            if r.status_code == 204: available.append(user)
            if user in usernames: continue
            usernames.append(user)
        if len(available) <= 0:
            available.append("None")

        print(f'''
{g}
      _   ___      _
|\/| /     |  ._ _|_ _ {w} Created by vvs{g}
|  | \_   _|_ | | | (_){w}.py


Username    :   {username}
UID         :   {uid}
Migrated    :   {migrated}
Past Names  :   {", ".join(usernames)}
Available   :   {", ".join(available)}
        ''')
username = sys.argv[1]
MCInfo.SearchUser(username)
