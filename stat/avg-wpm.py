import sys 
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime


def main():
    """Usage: avg-wpm.py filename.json

Print average number of words user by each user and average num of characters

Assumes filename.json is a JSON GroupMe transcript.
    """
    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    names = {}
    messcounts = {}
    charcounts = {}
    wordcounts = {}
    likesreceived = {}
    likesgiven = {}

    for message in transcript:
        name = message[u'name']
        id = message[u'user_id']
        
        numwords = 0
        if (message[u'text'] is not None):
            numwords = len(message[u'text'].split())

            names[id] = name
            if id not in messcounts:
                messcounts[id] = 0
            else:
                messcounts[id] = messcounts[id] + 1

            if id not in charcounts:
                charcounts[id] = 0
            else:
                charcounts[id] = charcounts[id] + len(message[u'text'])

            if id not in wordcounts:
                wordcounts[id] = 0
            else:
                wordcounts[id] = wordcounts[id] + numwords
        if (message[u'favorited_by'] is not None):
            likers = list(message[u'favorited_by'])
            for liker_id in likers:
                if liker_id not in likesgiven:
                    likesgiven[liker_id] = 0
                else:
                    likesgiven[liker_id] += 1
                if message[u'sender_id'] not in likesreceived:
                    likesreceived[message[u'sender_id']] = 0
                else:
                    likesreceived[message[u'sender_id']] += 1

    for id, count in messcounts.items():
        name = names[id]
        totalwords = wordcounts[id]
        avgwords = totalwords/count
        totalchars = charcounts[id]
        avgchars = totalchars/count
        total_likes_given = likesgiven.get(id, 0)
        total_likes_received = likesreceived.get(id, 0)
        print name
        print "\tTotal messages = " + str(count)
        print "\tTotal words = " + str(totalwords)
        print "\tAverage words = " + str(avgwords)
        print "\tTotal characters typed = " + str(totalchars)
        print "\tAverage characters used = " + str(avgchars)
        print "\tTotal likes given = " + str(total_likes_given)
        print "\tTotal likes received = " + str(total_likes_received)



if __name__ == '__main__':
    main()
    sys.exit(0)

