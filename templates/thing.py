import random
from collections import defaultdict

'''
Team BigOwl: Adam Abbas, Daria Shifrina
SoftDev pd7
HW#03: StI/O: Divine your Destiny!
2017-09-15
'''

cool_file = open("occupations.csv", "r")
cool_list = cool_file.readlines()
#print coolList
cool_dic = {}
i = 1

while (i<len(cool_list)):
     comma = cool_list[i].rfind(",", 0, len(cool_list[i]))
     cool_dic[cool_list[i][:comma]] = cool_list[i][comma + 1:len(cool_list[i]) - 1]
     i += 1

#print(cool_dic)

#explanation: we used cumulative probability, since random does not account for weighted probabilities as all of the values in its range have an equal probability of being picked. first, we generated a random float that stood for a random percentage(0-100%). then we summed up the dictionary probabilities in the cumulative_probability. the moment the cumulative probability exceeded the random percentage, we returned that value. this method is efficient because dictionary keys are picked in random order so there's no order ruining the randonmness(a parallel would be a bag with different amounts of colorful balls and randomly taking out one!) 
def random_occupation():
    c = 0 #counter for while loop
    random_float = random.uniform(0.0, 100.0) #float within range
    #print random_float
    cumulative_probability = 0.0
    while (c < len(cool_dic)):
        cumulative_probability += float(cool_dic.values()[c])
        if (cumulative_probability>random_float):
            return cool_dic.keys()[c]
        c += 1

#below we are testing the accuracy of using cumulative frequency. we are running 1000 test trials to see if each occupation shows up the percentage that it is supposed to. as you can tell, it is pretty close every single time.
counter = 0
frequency_words = ""
while(counter < 1000):
    frequency_words += random_occupation() + "$"
    counter +=1

d = defaultdict(int)
for word in frequency_words.split("$"):
    d[word] += 1

print('Occupation Frequency')
for occupation, frequency in d.items():
    print('{} {}'.format(occupation, frequency))