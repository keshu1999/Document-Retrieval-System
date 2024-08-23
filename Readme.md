## Bag of Words Document Retrieval System

This Assignment is made by :
* Keshav Sharma		ID : 2017A7PS0140P
* Burhan Boxwalla		ID : 2017A7PS0097P
* Pranav Panchumarthi	ID : 2017A7PS0153P

The Assignment is am implementation of the working Information Retrieval Systems. To run the Vector-Space based Information Retrieval System

1. Extract the files index_creation, test_queries.py and wiki_69.txt (or any other corpus) onto the same directory

2. If you want to use a different file as a corpus, change the name of the file in the 8th line of the index_creation.py file. The default corpus is wiki_69.txt.

3. Run the file index_creation.py to create 2 pickle files containing Indexes and Posting lists.

4. Run the file test_queries.py and enter a sample query. Select option 1 for parsing the query without lemmatization and spell check and option 2 for parsing the query using these.

The Top 10 Retrieved documents are displayed on the console.  

Make sure you have NLTK and pyspellchecker libraries installed on your system before running.
Downloading nltk : 
	Ubuntu : sudo apt install python3-nltk
	Windows : Visit http://pypi.python.org/pypi/nltk and download nltk. Once downloaded, import nltk and type nltk.download('all') in the console
	
Downloading pyspellchecker :
	The easiest method to install is using pip:		
		pip install pyspellchecker
	If you are using virtual environments :
		pipenv install pyspellchecker
	To install from source:
		git clone https://github.com/barrust/pyspellchecker.git
		cd pyspellchecker
		python3 setup.py install
