import xlrd
import math
from wordcloud import WordCloud
import matplotlib.pyplot as plt

loc_lyrics = (r".\data\song_lyrics_1.xlsx")
wb_lyrics = xlrd.open_workbook(loc_lyrics)
sheet_lyrics = wb_lyrics.sheet_by_index(1)

# Define constants
MINIMUM_OCCURRENCES = 157 #To get rid of Thoia Thoing song
MAXIMUM = 30
TOTAL_WORDS = 1603032

# Define other variables
count = 0
current_decade = 1960
word_count_by_decade = {}
word_count_overall = {}
z_scores_by_decade = {}
lyrics = ""
top_lyrics_by_decade = ""
z_lyrics_by_decade = ""
number_of_words_by_decade = {1960:0, 1970:0, 1980:0, 1990:0, 2000:0, 2010:0}
# Stopwords to not include in word counts
ignore_words = ["you","i","the","a", "and","to","me","it","my","in","on","oh","im",
               "we","yeah","la","NA","is","that","your","be","of","all","dont","so","for","just","do",
               "with","its","but","no","got","get","can","what","when","this","youre","if",
                "up","she","some","much","our","his","her","about","theres","then","da","every","shes",
                "ooh","that","could","had","wont","where","at","ill","isnt","cant","whos","na","put",
                "take","have","they","how","are","youve","was","not","were","there","an","em","uh","id",
                "am","him","from","he","as","ive","ya","by","or"]

def create_wordcloud(text, decade, save):
    wordcloud = WordCloud(width=480, height=480, margin=0, background_color="white", normalize_plurals=True, collocations=False).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.title("Higest z-scoring Lyrics of the %ss" % str(decade))
    if (save):
        plt.savefig("C:/Users/adamg/OneDrive/Documents/aAdam Princeton Freshman/WRI 150 Your Life in Numbers/Unit 3/Word Clouds/Wordcloud_%ss.png" % str(decade), format="png")        
        plt.show()
    else:
        plt.show()

# Used to create word_count_overall to be used in z-score calculations
for i in range(1, sheet_lyrics.nrows):
    lyrics = sheet_lyrics.row_values(i)[4]
    split_lyrics = lyrics.split()
    for word in split_lyrics:
        if word in ignore_words:
            continue     
        if word not in word_count_overall:
            word_count_overall[word] = 1
        else:
            word_count_overall[word] += 1

for i in range(1, sheet_lyrics.nrows):
    rank = sheet_lyrics.row_values(i)[0]
    song = sheet_lyrics.row_values(i)[1]
    artist = sheet_lyrics.row_values(i)[2]
    year = sheet_lyrics.row_values(i)[3]
    decade = math.floor(year/10)*10
    lyrics = sheet_lyrics.row_values(i)[4]
    split_lyrics = lyrics.split()
    
    for word in split_lyrics:
        number_of_words_by_decade[current_decade] += 1
        if word in ignore_words:
            continue
        if word not in word_count_by_decade:
            word_count_by_decade[word] = 1
        else:
            word_count_by_decade[word] += 1        

    if decade != current_decade or (year == 2015 and rank == 100):
        #print("Top", str(MAXIMUM), "Lyrics of the", str(current_decade) + "s")
        for key, value in sorted(word_count_by_decade.items(), key=lambda item:item[1], reverse=True):
            if count < MAXIMUM:
                #print("%s: %s" % (key, value))
                top_lyrics_by_decade += (key + " ")*value
                count += 1
            else:
                #create_wordcloud(top_lyrics_by_decade, current_decade, False)
                top_lyrics_by_decade = ""
                count = 0
                break
       
        # Calculate z-scores by finding how the actual # differs from the expected
        z_scores_by_decade = word_count_by_decade
        for key in z_scores_by_decade.keys():
            value = z_scores_by_decade[key]
            if value < MINIMUM_OCCURRENCES:
                value = 0
            z_scores_by_decade[key] = (value/word_count_overall[key]) / (number_of_words_by_decade[current_decade]/TOTAL_WORDS)
        for key, value in sorted(z_scores_by_decade.items(), key=lambda item:item[1], reverse=True):
            if count < MAXIMUM:
                print("%s: %s" % (key, value))
                z_lyrics_by_decade += (key + " ")*math.floor(value*10)
                count += 1
            else:
                create_wordcloud(z_lyrics_by_decade, current_decade, False)
                z_lyrics_by_decade = ""
                count = 0
                break        
        
        word_count_by_decade = {}
        if current_decade != 2010:
            current_decade += 10

#print("Top Lyrics Overall")
for key, value in sorted(word_count_overall.items(), key=lambda item:item[1], reverse=True):
            if value > 100:
                #print("%s: %s" % (key, value))
                top_lyrics_by_decade += (key + " ")*value
            else:
                #create_wordcloud(top_lyrics_by_decade, "Overall", False)
                break
