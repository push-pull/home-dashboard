import discord
import asyncio

import json

API_TOKEN = json.loads(open('config.json').read())['API_TOKEN']

class Chore:
    def __init__(self, name, people=None):
        self.name = name
        self.people = people
        self.owner = None
        self.completed = False

    def assign_random_user(self):
        from random import choice
        self.owner = choice(self.people)
        return self.owner

    def complete(self):
        self.complete = True


class Person:
    def __init__(self, username):
        self.username = username


client = discord.Client()
assigned_chores = []

def get_chore(owner):
    for chore in assigned_chores:
        if chore.owner.user == owner:
            return chore

def get_thanks():
    return "You're the best!"

@client.event
async def on_ready():
    print('%s is online.' % client.user.name)
    channel = client.get_channel('192684591432073218')
    await announce_chore_assignments()

@client.event
async def on_message(message):
    if message.content.startswith('!complete'):
        chore = get_chore(message.author)

        if chore:
            assigned_chores.remove(chore)
            msg = "Marking \"{chore}\" as complete. {thanks}".format(chore=chore.name, thanks=get_thanks())
        else:
            msg = "You don't have any chores assigned to you, {user}.".format(user=message.author.mention)

        await client.send_message(message.channel, msg)

async def announce_chore_assignments():
    people = [Person('deus-x'), Person('thetwam')]
    channel = client.get_channel('192684591432073218')

    for person in people:
        user = channel.server.get_member_named(person.username)

        if user:
            person.user = user
        else:
            people.remove(person)

    chores = [Chore('Take out the trash', people=people)]

    for chore in chores:
        assigned_to = chore.assign_random_user()

        message = "Chore time! Sorry, {user}, it's your turn to: {chore}".format(
            user=assigned_to.user.mention,
            chore=chore.name
        )

        assigned_chores.append(chore)

        await client.send_message(channel, message)


client.run(API_TOKEN)
