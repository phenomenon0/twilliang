import wikipedia
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json


#wekker




@csrf_exempt
def index(request):
    return HttpResponse('Hello Monay')


def which_engine(msg):
    if msg[:5] == 'wiki ':
        print(f'Wikipedia search {msg[5:]}')
        content = wiki_search(msg[5:])
    elif msg[:5] == 'wolf ':
        content = wolframalpha(msg[5:])
    elif msg[:5] ==   'dict ' :
        google_dic(msg[5:])
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

def wolframalpha(msge):
    APPID = 'LR36L2-JWRKPRLR5L'
    your_query = msge
    your_query = your_query.replace(' ', '+')
    url = f'https://api.wolframalpha.com/v1/result?i={your_query}&appid={APPID}'
    response = requests.request("GET", url)
    answer  = response.text
    answer = wordsplitter(answer)
    print(answer)
    return answer


def google_dic(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/'
    url = url + f'/{word}'
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    #print('audio: ' + json_data[0]['phonetics'][0]['audio'])
    #counter = len(json_data[0]['meanings'][0])
    i=1
    things = []
    r=0
    
    things.append(json_data[0]['word'] + ' ' + json_data[0]['phonetics'][0]['text'] )
    
    for item in json_data[0]['meanings']:
       
        things.append(f'{i}.')
        things.append(json_data[0]['meanings'][i-1]['partOfSpeech']) #try
        things.append('Definition: ' + json_data[0]['meanings'][0]['definitions'][r]['definition'])
       
        if len(json_data[0]['meanings'][0]['definitions'])>1:
            things.append('Example: ' + json_data[0]['meanings'][0]['definitions'][r]['example']) 
            i+=1
           
            r=+1
        else :
             #phonetics
            i+=1
              
            r=+1  

    bang = '\n'.join(things)
    print(bang)
    print(type()(bang))
    bang = wordsplitter(bang)
    print(bang = wordsplitter(bang))
    return bang




@csrf_exempt
def sms_response(request):
    
    resp = MessagingResponse()
    body = request.POST.get('Body', None)
    
    
    # Start our TwiML response
    new_messages = which_engine(body)
    
    for items in new_messages:
        msg = resp.message(items)

    return HttpResponse(str(resp))

   