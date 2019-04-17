#!/usr/bin/env python3

from sys import exit
from os.path import exists
from config import SECRETFILE, CONSUMERKEY, CONSUMERSEC, ACCESSKEY, ACCESSSEC, OBSERVEE, POSTSDONE, POSTSTODO, POSTER
import random
import pickle
import twitter

COUNT = 200  # API sez, 200 at max

class MemBot:
    
    def __init__(self): 
        self._t = None
        self._done = set()
        self._todo = list()

    def retreive(self):
        print("Retreiving additional tweets by @%s" % OBSERVEE)
        pos = min(self._todo) if (self._todo and random.getrandbits(1)) else 1
        self._todo += [x.id for x in _t.GetUserTimeline(screen_name=OBSERVEE, max_id=pos,
            count=COUNT, include_rts=False, trim_user=True, exclude_replies=True)]
        self._todo = list(set(self._todo))
        with open(POSTSTODO, 'wb') as poststodo:
            pickle.dump(self._todo, poststodo)
        print("Persisted %d statuses." % len(self._todo))

    def pick_status(self):
        print("Picking some random status..")
        status = None
        todo_id = None
        while todo_id not in self._done:
            todo_id = random.choice(self._todo)
            status = self._t.GetStatus(todo_id, trim_user=True)
            self._todo.remove(todo_id)
            self._done.add(todo_id)
            if status.text.startswith("@") or status.text.startswith("RT"):
                continue
            status.text = status.text.replace("@", "#")
            return status

    def post_random(self):
        status = self.pick_status()
        if not status:
            print("Posted nothing.")
            return
        post = self._t.PostUpdate("%s @%s" % (status.text, OBSERVEE))
        if post:
            print("Posted %s" % (post.text))
        else:
            print("Not posted.")

    def reply_random(self):
        print("Looking for replies.")
        for status in self._t.GetMentions(contributor_details=True,
                include_entities=False):
            print("Considering '%s' id %d by %s" % (status.text, status.id,
                status.user.screen_name))
            if status.id in self._done:
                print("Already done.")
                continue
            if status.user.screen_name in [POSTER]: #and not status.user.screen_name in [OBSERVEE, "pschwede"]:
                print("Ignored user.")
                continue
            reply = self.pick_status()
            if not reply:
                print("No reply.")
                continue
            post = self._t.PostUpdate(status=reply.text,
                    in_reply_to_status_id=status.id,
                    auto_populate_reply_metadata=True)
            self._done.add(status.id)
            print("Replied with '%s' id %s" % (reply.text, reply.id))
    
    def __enter__(self):
        print("Connecting..")
        self._t = twitter.Api(consumer_key=CONSUMERKEY,
            consumer_secret=CONSUMERSEC,
            access_token_key=ACCESSKEY,
            access_token_secret=ACCESSSEC,
            sleep_on_rate_limit=True)
        print("Connected.")
        if not self._t.VerifyCredentials():
            print("Could not verify.")
            return 1
        print("Verified.")

        print("Checking already posted statuses")
        if exists(POSTSDONE):
            with open(POSTSDONE, 'rb') as postsdone:
                self._done = pickle.load(postsdone)
            print("Loaded %d already posted statuses" % len(self._done))
        else:
            print("Starting with empty set of already posted statuses.")

        print("Loading statuses by @%s" % OBSERVEE)
        if exists(POSTSTODO):
            with open(POSTSTODO, 'rb') as poststodo:
                self._todo = pickle.load(poststodo)
        print("Loaded %d statuses." % len(self._todo))
        return self

    def __exit__(self, typ, value, traceback):
        with open(POSTSDONE, 'wb') as postsdone:
            pickle.dump(self._done, postsdone)
        with open(POSTSTODO, 'wb') as poststodo:
            pickle.dump(self._todo, poststodo)
        print("Persisted statuses.")


if __name__ == "__main__":
    with MemBot() as m:
        m.post_random()
        m.reply_random()
