import os
import re
import socket
from collections import Counter

# paths to the files inside the container
file1 = "/home/data/IF.txt"
file2 = "/home/data/AlwaysRememberUsThisWay.txt"

# where we want to save the output
out_dir = "/home/data/output"
out_file = out_dir + "/result.txt"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)


def count_words(filepath):
    f = open(filepath, "r")
    content = f.read()
    f.close()
    # normalize curly apostrophes and em-dashes first
    content = content.replace("\u2019", "'")   # curly ' -> straight '
    content = content.replace("\u2014", " ")   # em-dash -> space
    content = content.replace("\u2018", "'")   # curly ' -> straight '
    words = content.split()
    cleaned = []
    for w in words:
        w2 = w.strip('.,!?;:\"\':()[]{}').lower()
        if w2:
            cleaned.append(w2)
    return len(cleaned)


def get_words(filepath):
    f = open(filepath, "r")
    content = f.read()
    f.close()
    # normalize curly apostrophes and em-dashes
    content = content.replace("\u2019", "'")
    content = content.replace("\u2014", " ")
    content = content.replace("\u2018", "'")
    words = content.split()
    cleaned = []
    for w in words:
        w2 = w.strip('.,!?;:\"\':()[]{}').lower()
        if w2:
            cleaned.append(w2)
    return cleaned


def get_words_expand_contractions(filepath):
    f = open(filepath, "r")
    raw = f.read()
    f.close()

    # normalize curly apostrophes first
    raw = raw.replace("\u2019", "'")
    raw = raw.replace("\u2014", " ")
    raw = raw.replace("\u2018", "'")
    raw = raw.lower()

    # expand contractions
    raw = raw.replace("i'm", "i am")
    raw = raw.replace("i've", "i have")
    raw = raw.replace("i'll", "i will")
    raw = raw.replace("i'd", "i would")
    raw = raw.replace("you're", "you are")
    raw = raw.replace("you've", "you have")
    raw = raw.replace("you'll", "you will")
    raw = raw.replace("you'd", "you would")
    raw = raw.replace("he's", "he is")
    raw = raw.replace("she's", "she is")
    raw = raw.replace("it's", "it is")
    raw = raw.replace("we're", "we are")
    raw = raw.replace("we've", "we have")
    raw = raw.replace("we'll", "we will")
    raw = raw.replace("they're", "they are")
    raw = raw.replace("they've", "they have")
    raw = raw.replace("they'll", "they will")
    raw = raw.replace("that's", "that is")
    raw = raw.replace("there's", "there is")
    raw = raw.replace("can't", "cannot")
    raw = raw.replace("won't", "will not")
    raw = raw.replace("don't", "do not")
    raw = raw.replace("doesn't", "does not")
    raw = raw.replace("didn't", "did not")
    raw = raw.replace("isn't", "is not")
    raw = raw.replace("aren't", "are not")
    raw = raw.replace("wasn't", "was not")
    raw = raw.replace("weren't", "were not")
    raw = raw.replace("hasn't", "has not")
    raw = raw.replace("haven't", "have not")
    raw = raw.replace("hadn't", "had not")
    raw = raw.replace("wouldn't", "would not")
    raw = raw.replace("couldn't", "could not")
    raw = raw.replace("shouldn't", "should not")
    raw = raw.replace("let's", "let us")

    words = raw.split()
    cleaned = []
    for w in words:
        w2 = w.strip('.,!?;:\"\':()[]{}').lower()
        if w2:
            cleaned.append(w2)
    return cleaned


# word counts
count_if = count_words(file1)
count_gaga = count_words(file2)
total_words = count_if + count_gaga

# top 3 for IF.txt
words_if = get_words(file1)
freq_if = Counter(words_if)
top3_if = freq_if.most_common(3)

# top 3 for song
words_gaga = get_words_expand_contractions(file2)
freq_gaga = Counter(words_gaga)
top3_gaga = freq_gaga.most_common(3)

# ip address
try:
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.connect(("8.8.8.8", 80))
    ip_addr = temp_sock.getsockname()[0]
    temp_sock.close()
except Exception:
    ip_addr = socket.gethostbyname(socket.gethostname())

# build result
result = ""
result += "Word Count Results\n"
result += "Total words in IF.txt: " + str(count_if) + "\n"
result += "Total words in AlwaysRememberUsThisWay.txt: " + str(count_gaga) + "\n"
result += "Grand total (both files): " + str(total_words) + "\n\n"

result += "Top 3 words in IF.txt:\n"
for i in range(len(top3_if)):
    word = top3_if[i][0]
    cnt = top3_if[i][1]
    result += "  " + str(i+1) + ". " + word + " : " + str(cnt) + " times\n"

result += "\nTop 3 words in AlwaysRememberUsThisWay.txt (contractions expanded):\n"
for i in range(len(top3_gaga)):
    word = top3_gaga[i][0]
    cnt = top3_gaga[i][1]
    result += "  " + str(i+1) + ". " + word + " : " + str(cnt) + " times\n"

result += "\nIP Address of container: " + ip_addr + "\n"
output = open(out_file, "w")
output.write(result)
output.close()

print(result)
print("Output saved to", out_file)