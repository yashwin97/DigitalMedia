import nltk
nltk.download('vader_lexicon')
nltk.download('words')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
import itertools

#cleaning dataset by removing repetitive words and only taking in english dictionary words
clean_words = set(nltk.corpus.words.words())
def read_clean(file_name):
    hashtag1 = set()
    hashtag2 = set()

    with open(file_name, "r", encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for lines in csv_reader:
            w = lines['hashtag1'].lower()
            if w in clean_words:     # "or w.isalpha()" can be added for all the words
                hashtag1.add(w)

            w = lines['hashtag2'].lower()
            if w in clean_words:
                hashtag2.add(w)

    return list(hashtag1), list(hashtag2)

#dataset = 'sochiAD.csv'
#dataset = 'sochiBL.csv'
dataset = 'sochiEX.csv'

set1, set2 = read_clean(dataset)
total_words1 = len(set1)
total_words2 = len(set2)
print(total_words1, total_words2)
print("\n")

#saving filtered dataset as csv file
def write_csv(data1,data2,title):
    out = [['hashtag1', 'hashtag2']]
    for x in itertools.zip_longest(data1,data2):
        out.append(x)

    with open('Filtered_'+ title,'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(out)

write_csv(set1,set2,dataset)

# sentiment analysis of column(hashtag) in dataset
sia = SentimentIntensityAnalyzer()
def get_overall_sentiment(input,words, title):
    sentiment_score = 0
    word_count = 0
    dict1 = {}
    for word in input:
        word_count += 1
        ss = sia.polarity_scores(word)
        sentiment_score += ss['compound']
        #print(ss)
        if  ss['compound'] > 0.6:
            #print("greatest")
            if "great" in dict1.keys():
                dict1["great"] += 1
            else:
                dict1["great"] = 1
        elif ss['compound'] > 0.2 and ss['compound'] <= 0.6:
            #print('good')
            if "good" in dict1.keys():
                dict1["good"] += 1
            else:
                dict1["good"] = 1
        elif ss['compound'] > -0.2 and ss['compound'] <= 0.2:
            #print('average')
            if "average" in dict1.keys():
                dict1["average"] += 1
            else:
                dict1["average"] = 1
        elif ss['compound'] > -0.6 and ss['compound'] <= -0.2:
            #print('bad')
            if "bad" in dict1.keys():
                dict1["bad"] += 1
            else:
                dict1["bad"] = 1
        else:
            #print("very bad")
            if "very bad" in dict1.keys():
                dict1["very bad"] += 1
            else:
                dict1["very bad"] = 1
    #print(sentiment_score, word_count)

    print('Total word count in ' + title + ': ' + str(word_count))
    print('Total compound value: ' + str(sentiment_score))
    print('overall sentiment score : ' + str(sentiment_score/words))
    print(dict1)
    # return sentiment_score / len(get_all_sents())

get_overall_sentiment(set1, total_words1, 'cluster1')
print("\n")
get_overall_sentiment(set2, total_words2, 'cluster2')

