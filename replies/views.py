import wikipedia
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse


@csrf_exempt
def index(request):
    return HttpResponse('Hello Monay')


def which_engine(msg):
    if msg[:5] == 'wiki ':
        print(f'Wikipedia search {msg[5:]}')
        content = wiki_search({msg[5:]})
    elif msg[:4] == 'book ':
        print(f'book search {msg[4:]}')
    elif msg[:4] ==   'dict' :
        print(f'dictionary search {msg[4:]}')
    elif msg[:5] == 'movie ':
        print(f'Imdb search {msg[5:]}')
    elif msg[:5] == 'imdb ':
        print(f'IMDB search {msg[4:]}')
    else :
        print(f'searching {msg}')
    return content  

def wordsplitter(msg):
    msg_split = []
    message_no = int(len(msg)/1600)
    i=0
    j=1599
    k=0
   
    
    while k <= message_no:
        msg_split.append(msg[i:j])
        k+=1
        i+=1599
        j+=1599

    return msg_split

def url_maker(lista):
    urls =[]
    for word in lista:
        bird = word.replace(' ', '_')
        urls.append(bird)
    return urls 

#summary = wikipedia.summary('Android')
def wiki_search(q_word):
   # query = input('enter your search query \n')
    result_list = wikipedia.search(q_word)
    i = 0
    for word in result_list:
    
        print(f'{i}. {word}')
        i += 1
    #using an id from search list to generate a pa
    #print(wikipedia.summary('Ed Balls'))
    result_list = url_maker(result_list)
    #choice = int    (input('choose suitable option\n'))
    #print(result_list[choice])
    juice = wikipedia.page(f'{result_list[0]}').summary
    #juice = wikipedia.page(f'{result_list[choice]}').content
    word_list = wordsplitter(juice)
    return  word_list







@csrf_exempt
def sms_response(request):
    
    resp = MessagingResponse()
    body = request.POST.get('Body', None)
    
    
    # Start our TwiML response
    new_messages = which_engine(body)
    for items in new_messages:
        msg = resp.message(str(items))

    return HttpResponse(str(resp))