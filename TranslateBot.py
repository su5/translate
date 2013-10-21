'''
Created on Sep 4, 2013

@author: vostro
'''
import time  #tracking purposed
import re    #prolly gonna be useful
import praw  # for reddit
import goslate
count = 0
trigger = '-translatethis'
runTestMessage = True

r = praw.Reddit(user_agent='multifunctionbot')
print("logging in")
r.login()
print("logged in")

lastTime = 0
languages = goslate.Goslate().get_languages()
tl = goslate.Goslate()
checked = []
parsed=0
getreddits = r.get_my_subreddits(limit=None)
allowedSubs = None


replied = 0
all_comments = r.get_comments('all',limit=None)
done = []
while True:
    try:
        print("starting loop %d, we have parsed %d comments, and have translated %d items"%(count,parsed,replied))
        count+=1
        for com in all_comments:
            parsed+=1
            if str(com.author).lower() != 'multifunctionbot' and com.id not in done:
                if (trigger in com.body.lower() or '/u/multifunctionbot' in com.body.lower()) and not com.is_root:
                    print("found one!")
                    done.append(com.id)
                    nls = re.findall('[+][a-z][a-z]',com.body)
                    newText =  r.get_info(thing_id=com.parent_id).body
                    prevAuth = r.get_info(thing_id=com.parent_id).author
                    if str(prevAuth).lower() == 'multifunctionbot':
                        newText = newText[:newText.find('---')]
                    print(len(nls))
                    bad = True
                    oldLang = tl.detect(newText)
                    source = oldLang
                    job = languages[oldLang]
                    for nl in nls:
                        key = nl[1:]
                        if key in languages:
                            lang = languages[key]
                            job+=' to %s'%lang
                            newLang = languages[key]
                            newText = tl.translate(newText, nl[1:])
                            print('did it')
                            bad = False
                    
                    outStr="""%s

    
-------------------
    
      

That was the result of %d translations

    
    
[Languages and keys.](http://www.reddit.com/r/test/comments/1lze9y/supported_languages/) 
    
    
The translation provided by the Googles
"""%(newText,len(nls))
                    if bad == False:
                        com.reply(outStr)
                        replied+=1
        
        all_comments = r.get_comments('all',limit=None)
    except:
        print('oops')
            
    
    
    
print('all done')
