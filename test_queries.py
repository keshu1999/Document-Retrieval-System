import math
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker
from nltk.tag import pos_tag

######################################################################

def Log(a):
    if a == 0:
        return 0
    else:
        return math.log10(a)

######################################################################
        
def Normalize(Matrix):
    if type(Matrix[0]) == float:
        Mat = [Matrix[:]]
    else:
        Mat = [row[:] for row in Matrix]
    for i in range(len(Mat)):
        sqrSum = 0.0
        for j in range(len(Mat[i])):
            sqrSum += Mat[i][j]**2
        docLen = math.sqrt(sqrSum)
        if docLen == 0:
            continue
        for j in range(len(Mat[i])):
            Mat[i][j] /= docLen
    if type(Matrix[0]) == float:
        return Mat[0]
    return Mat

######################################################################

def Similarity(A, B):
    prodsum = 0
    for i in range(len(A)):
        prodsum += A[i]*B[i]
    return prodsum

######################################################################

def computeScore(Query_Tokens, Posting_List):
    Query_Toks = list(dict.fromkeys(Query_Tokens))
    Query_Toks.sort()
    Querylen = len(Query_Toks)
    QueryScore = [0.0 for i in range(Querylen)]
    DocScore = [[0.0 for i in range(Querylen)] for j in range(N)]
    Scores = [0.0 for i in range(N)]
    
    #Doc and Query Vectors
    index = 0
    for queryWord in Query_Toks:
        if Posting_List.get(queryWord) is None:
            index += 1
            continue
        else:
            postList = Posting_List[queryWord]
            idf = Log(N/len(postList))
            for key in postList:
                DocScore[key][index] = 1 + Log(postList[key])
                QueryScore[index] = (1 + Log(Query_Tokens.count(queryWord)))*idf
        index += 1
    del index, queryWord

    NormDocScore = Normalize(DocScore)
    NormQueryScore = Normalize(QueryScore)

    for i in range(N):
        Scores[i] = Similarity(NormQueryScore, NormDocScore[i])
    SortedScores = dict()
    for i in range(len(Scores)):
        SortedScores[i] = Scores[i]
    del i
    SortedScores = dict(sorted(SortedScores.items(), key=lambda x:x[1], reverse=True))
    
    return SortedScores

######################################################################
    
def printDocs(Query_Tokens, Posting_List, Doc_ids, Doc_titles, rank):
    global Retrieved_Docs
    Scores = computeScore(Query_Tokens, Posting_List)
    for score in Scores:
        if score == 0.0:
            break
        if Doc_ids[score] in Retrieved_Docs:
            continue
        rank+=1
        Retrieved_Docs.add(Doc_ids[score])
        print('Rank ' + str(rank) + ': Doc ID: ' + str(Doc_ids[score]), end=' ')
        print('     Title: ' + str(Doc_titles[score]) + "\nScore: " + str(Scores[score]) + '\n')
        if rank == 10:
            break
    return rank

#####################################################################
    
with open('Posting_List.pik', 'rb') as f:
    Posting_List, Doc_ids, Doc_titles, N = pickle.load(f)

with open('Posting_List_Lem.pik', 'rb') as f:
    Posting_List_Lem, Doc_ids_Lem, Doc_titles_Lem, N = pickle.load(f)
    
punctuation = ['.', ',', '(', ')', '"', '!', ':', '-']
le = WordNetLemmatizer()
#Take input from User
User_Query = input('Please Enter Your Query: ')
query_tok = word_tokenize(User_Query)
Query_Tokens_Raw = []
Query_Tokens = []
Query_Tokens_Lem = []
for quer in query_tok:
    if quer not in punctuation:
        Query_Tokens_Raw.append(quer)
        Query_Tokens.append(quer.lower())
        Query_Tokens_Lem.append(le.lemmatize(quer.lower()))
        
del query_tok, quer

Retrieved_Docs = set()
print("Enter 1 for lnc.ltc parsing")
print("Enter 2 for lnc.ltc parsing with Lemmatization and Spell-Check")
option = int(input("Option: "))
while option > 2:
    option = int(input("Enter a valid Option: "))
    
print("\n--------------THE TOP 10 DOCUMENTS RETRIEVED ARE--------------\n")
count = printDocs(Query_Tokens, Posting_List, Doc_ids, Doc_titles, 0)
if option == 2:
    if count < 10:
        count = printDocs(Query_Tokens_Lem, Posting_List_Lem, Doc_ids, Doc_titles_Lem, count)
    
    if count < 10:
        #spellcheck
        spell = SpellChecker()
        Query_Tokens_Corrected = list()
        
        for word in Query_Tokens_Raw:
            if pos_tag([word])[0][1] == 'NNP':
                Query_Tokens_Corrected.append(word.lower())
                continue
            corrected = spell.correction(word)
            Query_Tokens_Corrected.append(corrected.lower())
            
        printDocs(Query_Tokens_Corrected, Posting_List, Doc_ids, Doc_titles, count)
        del word
    del count
#####################################################################