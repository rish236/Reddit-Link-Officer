import config
import praw
from bs4 import BeautifulSoup
import string
import requests

url = ''




def client():
    
    print("Logging in...")
    reddit = praw.Reddit(user_agent = 'LinkOfficer (by /u/?????)', client_id = config.client_id, client_secret = config.client_secret, 
    username = config.username, password = config.password)

    print ("Logged in as:",config.username)

    activation = '!linkofficer'
    subreddits = reddit.subreddit('TEST')


    
    for comment in subreddits.stream.comments():

        if activation in comment.body.lower():
             cmnt = comment.body.split()
             link = cmnt[1]

             if link_check(link):
                 url = link 
                 print (url)
                 msg = soup(url)
                 comment.reply(msg)

                 

             else:
                 comment.reply("Please enter a valid link.")


         

def link_check(url):

    approved = ['.com', '.org', '.net', '.io', '.edu', '.co', '.us', '.gov' ]

    if (url[-4:]) in approved or url[-3:] in approved:
        return True

    else:
        return False


def soup(url):
    main = 'https://safeweb.norton.com/report/show?url=' + url 

    page = requests.get(main)

    soup = BeautifulSoup(page.content, 'html.parser')

    #add check to wait for page to load 

    community_rating_tbl = soup.find_all(class_= 'community-text')[0].get_text().strip().split()

    safe_tbl = soup.find_all(class_= 'paddingTop30 tAlignCr')[0].get_text().strip().split()

    threats_tbl = soup.find_all(class_= 'span10')[0].get_text().strip().split()



    computer_threats = threats_tbl[2]
    identity_threats = threats_tbl[5]
    annoyance_factors = threats_tbl[8]
    total_threats = threats_tbl[14]

    community_rating = community_rating_tbl[0]
    users = community_rating_tbl[3]

    safe = safe_tbl[0].lower()

#reddit msg formatting 
    if safe == 'warning':

        msg = f'WEEEEOOOOOEEEEOOO LinkOfficer here! Watch out! This link is not safe! :(\n A total of {computer_threats} computer threats were found.\n A total of {identity_threats} identity threats were found.\n A total of {annoyance_factors} annoyance factors were found.\n A total of {total_threats} threats are present.\n This link received a rating of {community_rating} by {users} users.\n This link was tested using Norton SafeWeb'


    if safe == 'safe': 

        msg = f'WEEEEOOOOOEEEEOOO LinkOfficer here! No need to worry! This link is {safe}! :)\n A total of {computer_threats} computer threats were found.\n A total of {identity_threats} identity threats were found.\n A total of {annoyance_factors} annoyance factors were found.\n A total of {total_threats} threats are present.\n This link received a rating of {community_rating} by {users} users.\n This link was tested using Norton SafeWeb'



    else:
        msg = f'WEEEEOOOOOEEEEOOO LinkOfficer here! This link is {safe}!\n A total of {computer_threats} computer threats were found.\n A total of {identity_threats} identity threats were found.\n A total of {annoyance_factors} annoyance factors were found.\n A total of {total_threats} threats are present.\n This link received a rating of {community_rating} by {users} users.\n This link was tested using Norton SafeWeb'



    return msg



if __name__ == "__main__":
    client()
