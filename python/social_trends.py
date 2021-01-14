import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
    
count_subgroup = 0
current_year = 1965
year = 1965
number_of_words_by_year = {}

subgroup_financial = ["money", "dollar", "cash", "bill", "bills", "ballin"]
subgroup_violence = ["shit", "high", "fuck", "ass", "club", "bitch", "fight", "drink", "bang", "gun", "fuckin", "drunk", "kill", "shoot", "hell"]
subgroup_positive = ["love", "heart", "good", "dance", "sweet", "light", "together", "best", "dream", "friends", "party", "soul", "dreams", "sing", "smile", "kind"]
subgroup_negative = ["gone", "leave", "bad", "hard", "alone", "cry", "break", "rain", "lonely", "miss", "lose", "lost", "end", "hurt", "cold", "die", "tears"]

subgroup_list = []
year_list = np.linspace(1965,2015,51)

def count_words (subgroup, line_color):
    global current_year, count_subgroup, subgroup_list, number_of_words_by_year
    
    for i in range(1, sheet_lyrics.nrows):
        year = sheet_lyrics.row_values(i)[3]
        lyrics = sheet_lyrics.row_values(i)[4]
        split_lyrics = lyrics.split()
        if year != current_year:
            #print(current_year, ":", count_subgroup) 
            subgroup_list.append(count_subgroup)
            
            count_subgroup = 0
            current_year = year
            #print(year)
        
        for word in split_lyrics:
            if current_year in number_of_words_by_year:
                number_of_words_by_year[current_year] += 1
            else:
                number_of_words_by_year[current_year] = 1
            if word in subgroup:
                count_subgroup += 1 
            
    subgroup_list.append(count_subgroup)
    
    # Adjust for differing numbers of total lyrics each year
    print(number_of_words_by_year)
    for i, num in enumerate(subgroup_list):
        subgroup_list[i] = num/number_of_words_by_year[year_list[i]]*100
        print(year_list[i], ":", subgroup_list[i])
    
    plt.plot(year_list, subgroup_list, color=line_color)
    
    # Reset variables
    subgroup_list = []
    count_subgroup = 0
    year = 1965
    current_year = 1965
    number_of_words_by_year = {}

# Run function
count_words(subgroup_positive, "b")
count_words(subgroup_negative,"black")
count_words(subgroup_financial, "g")
count_words(subgroup_violence, "r")

# Format graph
plt.legend(["Positive", "Negative", "Financial", "Violent"], loc="upper right")
plt.xlim(1965,2015)
plt.ylim(0,4)
plt.xlabel("Year")
plt.ylabel("% of Occurrences per Year")
plt.title("Lyric Subgroup % Frequencies by Year")
#plt.savefig("C:/Users/adamg/OneDrive/Documents/aAdam Princeton Freshman/WRI 150 Your Life in Numbers/Unit 3/lyric_subgroups", format="pdf")
plt.show()
