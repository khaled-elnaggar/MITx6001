# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory(object):
    def __init__(self, guid='', title='', description='', link='', pubdate=datetime.now()):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

def compare_lists(phrase, text):
    check = False
    for i in range(len(text) - len(phrase) + 1):
        if phrase[0] == text[i]:
            check = True
            for j in range(1, len(phrase)):
                if phrase[j] != text[j + i]:
                    check = False
                    break

    return check


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        phrase = phrase.lower().strip()
        phrase = phrase.split()
        self.phrase = phrase

    def is_phrase_in(self, text):
        text = text.lower()
        temp = ''
        for i in text:
            if i in string.ascii_lowercase:
                temp += i
            else:
                temp += ' '
        text = temp.split()
        return compare_lists(self.phrase, text)


# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time_str):
        time_str = time_str.strip()
        time = datetime.strptime(time_str, '%d %b %Y %H:%M:%S')


        self.time = time


# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_str):
        TimeTrigger.__init__(self, time_str)

    def evaluate(self, story):
        # use pytz to define a timezone, then allocate it to time
        if story.get_pubdate().strftime('%Z') == 'EST':
            self.time = (self.time).replace(tzinfo=pytz.timezone('EST'))
        return self.time > story.get_pubdate()


class AfterTrigger(TimeTrigger):
    def __init__(self, time_str):
        TimeTrigger.__init__(self, time_str)

    def evaluate(self, story):
        # use pytz to define a timezone, then allocate it to time
        if story.get_pubdate().strftime('%Z') == 'EST':
            self.time = (self.time).replace(tzinfo=pytz.timezone('EST'))
        return self.time < story.get_pubdate()

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, t):
        self.t = t
    def evaluate(self, story):
        return not self.t.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered_stories = []
    print(len(triggerlist))

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
                break

    return triggered_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!

    triggers_list = []
    triggers_dict = {}
    parser = {'TITLE': TitleTrigger, 'DESCRIPTION': DescriptionTrigger, 'AFTER': AfterTrigger, 'BEFORE': BeforeTrigger,
              'NOT': NotTrigger, 'AND': AndTrigger, 'OR': OrTrigger}
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line.split(','))
    for trigger_line in lines:
        if trigger_line[0] != 'ADD':
            trigger_val = parser[trigger_line[1]]

            if len(trigger_line) == 3:
                triggers_dict[trigger_line[0]] = trigger_val(trigger_line[2])
            else:
                triggers_dict[trigger_line[0]] = trigger_val(trigger_line[2], trigger_line[3])
        else:
            for tito in trigger_line[1:]:
                triggers_list.append(triggers_dict[tito])
    return triggers_list

SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("syria")
        # t2 = DescriptionTrigger("apple")
        # t3 = DescriptionTrigger("million")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
