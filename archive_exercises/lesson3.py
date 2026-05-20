
import nltk

# Download the new tokenizer models
# nltk.download('punkt_tab')

# from nltk.tokenize import word_tokenize


# from nltk.tokenize import word_tokenize
# from collections import Counter
# import nltk
# nltk.download('punkt', quiet=True)


# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import nltk
# nltk.download('punkt', quiet=True)
# nltk.download('stopwords', quiet=True)

# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt', quiet=True)

# positive = {"good", "great", "happy", "fun", "love", "powerful"}
# negative = {"bad", "sad", "hate", "terrible", "hard"}

# def sentiment(text):
#     tokens = [t.lower() for t in word_tokenize(text)]
#     pos = sum(1 for t in tokens if t in positive)
#     neg = sum(1 for t in tokens if t in negative)
#     if pos > neg:
#         return "Positive"
#     elif neg > pos:
#         return "Negative"
#     else:
#         return "Neutral"

# print(sentiment("I love"))
# print(sentiment("This is a terrible example, I hate bugs."))

# import nltk
# from nltk.stem import PorterStemmer, WordNetLemmatizer
# from nltk import word_tokenize, pos_tag
# from nltk.corpus import wordnet

# # Downloads (run once)
# nltk.download('punkt', quiet=True)
# nltk.download('wordnet', quiet=True)
# nltk.download('omw-1.4', quiet=True)
# nltk.download('averaged_perceptron_tagger_eng', quiet=True)

# # Helpers to map NLTK POS tags to WordNet's format
# def get_wordnet_pos(treebank_tag):
#     if treebank_tag.startswith('J'):
#         return wordnet.ADJ
#     if treebank_tag.startswith('V'):
#         return wordnet.VERB
#     if treebank_tag.startswith('N'):
#         return wordnet.NOUN
#     if treebank_tag.startswith('R'):
#         return wordnet.ADV
#     return wordnet.NOUN  # fallback

# text = "The striped bats are hanging on their feet and they are better than before."

# tokens = word_tokenize(text)
# print("Tokens:", tokens)
# pos_tags = pos_tag(tokens)
# print("Pos Tags:", pos_tags)

# stemmer = PorterStemmer()
# lemmatizer = WordNetLemmatizer()

# print("Token | Stemmed | Lemmatized")
# for token, pos in pos_tags:
#     stem = stemmer.stem(token)
#     lemma = lemmatizer.lemmatize(token, get_wordnet_pos(pos))
#     print(f"{token:6} | {stem:7} | {lemma}")



# from nltk.tokenize import RegexpTokenizer

# text1 = "Learning Python is very useful!"
# text2 = "Learning Python = very usef."

# tokenizer = RegexpTokenizer(r'\w+')

# token1 = [word.lower() for word in tokenizer.tokenize(text1)]
# token2 = [word.lower() for word in tokenizer.tokenize(text2)]

# print(text1, token1)
# print(text2, token2)


# import gensim.downloader as api

# # this is a one‑time download + cache
# model = api.load("glove-wiki-gigaword-50")

# print("king ~ queen:", model.similarity("king", "queen"))
# print("paris + germany - france →",
#       [w for w,_ in model.most_similar(
#           positive=["paris","germany"],
#           negative=["france"],
#           topn=10)])


from google import genai

client = genai.Client(api_key="AIzaSyB__xH7W3X2UqnkEebPNm9kWhGQQzx-cgM")

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="what is the time right now tlv?",
)

print(response.text)





# text = "This is an example showing how tokenization and stopword removal work."
# tokens = [t.lower() for t in word_tokenize(text)]
# filtered = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]

# print("Original tokens:", tokens)
# print("Filtered tokens:", filtered)


















# text = "Python is great. Python is simple. NLP with Python is powerful!"
# tokens = [t.lower() for t in word_tokenize(text)]
# freq = Counter(tokens)

# print("Tokens:", tokens)
# print("Frequencies:", freq)










# text = "Natural Language Processing with Python is fun!"
# tokens = word_tokenize(text)
# print(tokens)

# from nltk.tokenize import word_tokenize
# import nltk
# nltk.download('punkt', quiet=True)

# text = "Don't stop believing! It's amazing."

# print("split():", text.split())
# print("word_tokenize():", word_tokenize(text))