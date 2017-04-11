from nltk import word_tokenize
from nltk.corpus import stopwords


stopwords = set(stopwords.words('english'))
stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation
str1 = "Mariel Zagunis is notable for winning what?"
# str2 = "A notable alumnus of the College of Science is Medicine Nobel Prize winner Eric F. Wieschaus."
str2 = "With the university having high profile sports teams itself, a number of alumni went on to become involved in athletics outside the university, including professional baseball, basketball, football, and ice hockey players, such as Joe Theismann, Joe Montana, Tim Brown, Ross Browner, Rocket Ismail, Ruth Riley, Jeff Samardzija, Jerome Bettis, Brett Lebda, Olympic gold medalist Mariel Zagunis, professional boxer Mike Lee, former football coaches such as Charlie Weis, Frank Leahy and Knute Rockne, and Basketball Hall of Famers Austin Carr and Adrian Dantley."
str1_set, str2_set = set(word_tokenize(str1.lower())), set(word_tokenize(str2.lower()))
str1_set, str2_set = str1_set - stopwords, str2_set - stopwords
print str1_set, str2_set
intersection_set = str1_set.intersection(str2_set)
print float(len(intersection_set))