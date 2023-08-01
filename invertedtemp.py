
import json
def document_tokenization(doc, delimiters, after_delimiters, stop_words, docId):
    for i in delimiters:
        doc = str(doc).replace(i, ' ')

    for i in stop_words:
        doc = str(doc).replace(" "+i+" ", ' ')

    for i in after_delimiters:
        doc = str(doc).replace(i, ' ')


    split_terms = str(doc).split(' ')
    tokenized_terms = []

    for i in split_terms:
        if(i.lower() not in stop_words and i != ''):
            tokenized_terms.append({'term': i.lower(), 'docId': docId})
    return tokenized_terms 

def create_invertedindex(dictionary):
    term_postings = {} 

    for i in dictionary: 

        if term_postings.get(i['term']) == None: 
            term_postings[i['term']] = {'frequency': 0, 'posting_list': {}} 

        if i['docId'] not in term_postings[i['term']]['posting_list'].keys(): 
            term_postings[i['term']]['posting_list'][i['docId']] = 1 
        else:
            term_postings[i['term']]['posting_list'][i['docId']] += 1
        term_postings[i['term']]['frequency'] = term_postings[i['term']]['frequency'] + 1 

    return term_postings 

if __name__ == '__main__':
    stop_words_file = open('./stop_words.txt', 'r+', encoding='utf8')


    delimiters = ['.', ',', '“', '”', '-', "’s","'s", "\n", "\t", '—', '/', 
                  '(', ')', "!", "&", "~", "@", "#", "$", "%", "^", "*", "_", "₹", '\\',
                  "+", "=", "`", "<", ">", "?", "|", "[", "]", "{", "}", ":", ";", "\xa0", "'", '"',"'", "’", "‘"]

    after_delimiters = ["'", "’", "‘"]

    stop_words = stop_words_file.read().split('\n') 
    dictionary = []  

    for number in range(0, 990):
        number = number+1
        print('indexing document {num}'.format(num=number))
        try:
         document = open('./News_Dataset/{}.txt.txt'.format(str(number).zfill(4)), 'r+', encoding='utf8')
         words_after_filtering = document_tokenization(document.read().lower(), delimiters, after_delimiters, stop_words, number) 
         dictionary = dictionary + words_after_filtering 
         document.close() 
        except:
             print("page not in correct form")
    stop_words_file.close()

     

    dictionary = sorted(dictionary, key=lambda k: k['term'])  
    
    

    term_postings = create_invertedindex(dictionary) 

    
    json_dta = {}
    for i in term_postings:
        json_dta[i] = {"postings":[{"doc":str(x), "freq":str(term_postings[i]['posting_list'][x])} for x in term_postings[i]['posting_list'].keys()]}
    with open('newInverted1.json', 'w') as f:
     json.dump(json_dta, f, indent=4)
    f.close()

