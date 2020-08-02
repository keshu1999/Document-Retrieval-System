from bs4 import BeautifulSoup as bs
from nltk.tokenize import word_tokenize
import pickle 
from nltk.stem import WordNetLemmatizer

######################################################################

#open file and store data in raw_text
f = open("wiki_69.txt", "r", encoding='utf-8')
raw_text = f.read(-1)
f.close()
le = WordNetLemmatizer()

#create 
Doc_list = bs(raw_text, 'html.parser').find_all('doc')
Documents_List = []
Document_Tokens = []
Doc_ids = []
Posting_List = dict()
Posting_List_Lem = dict();
N = len(Doc_list)
Doc_titles = []


for i in range(N):
    Documents_List.append(bs(str(Doc_list[i]), 'html.parser').get_text())
    docid = int(bs(str(Doc_list[i]), 'html.parser').find('doc').attrs.get('id'))
    Doc_ids.append(docid)
    title = str(bs(str(Doc_list[i]), 'html.parser').find('doc').attrs.get('title'))
    Doc_titles.append(title)
    
punctuation = ['.', ',', '(', ')', '"', '!', ':', '-']

#Create Posting List
for i in range(N):
    word_token = word_tokenize(Documents_List[i])
    word_tokens = []
    word_tokens_lem=[]
    for word in word_token:
        if word not in punctuation:
            word_tokens.append(word)
            word_tokens_lem.append(word)
            wrd = word.lower()
            wrd_lem = le.lemmatize(wrd) 
            
            if wrd not in Posting_List.keys():
                Posting_List[wrd] = dict()
                Posting_List[wrd][i] = 1
            else:
                if Posting_List[wrd].get(i) is None:
                    Posting_List[wrd][i] = 1
                else:
                    Posting_List[wrd][i] = Posting_List[wrd][i] + 1
            
            if wrd_lem not in Posting_List_Lem.keys():
                Posting_List_Lem[wrd_lem] = dict()
                Posting_List_Lem[wrd_lem][i] = 1
            else:
                if Posting_List_Lem[wrd_lem].get(i) is None:
                    Posting_List_Lem[wrd_lem][i] = 1
                else:
                    Posting_List_Lem[wrd_lem][i] = Posting_List_Lem[wrd_lem][i] + 1
    Document_Tokens.append(word_tokens)
    
#Store Posting Lists in file Posting_List.pik
with open('Posting_List.pik', 'wb') as f:
  pickle.dump([Posting_List,Doc_ids, Doc_titles, N], f, -1)
#Store Lemmatized Posting Lists in file Posting_List_Lem.pik
with open('Posting_List_Lem.pik', 'wb') as f2:
  pickle.dump([Posting_List_Lem,Doc_ids, Doc_titles, N], f2, -1)
#Delete unwanted variables
del docid, wrd, word_token, word_tokens, i, word, wrd_lem, word_tokens_lem, title

######################################################################