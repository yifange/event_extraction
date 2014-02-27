Event and Task Extraction from Email
====================================

Group Member
------------
Jiaqi Gao   jiaqigao@jhu.edu
Yifan Ge    gyifan1@jhu.edu

Goals of the Project
-------------------
We notice our daily emails usually contain information about events and tasks, which is hard to organize. Life would be much easier if the event and task information can be extracted automatically from the emails we receive and added to our favorite calendar apps. The goals of our project are:

1. Classify the emails into different categories
Here we set three categories for the emails: EVENT, TODO, and OTHER. An EVENT email contains explicit date, time and location information (e.g. seminar announcements). A TODO email contains events with less information, or more personal. Something like a homework deadline notice can be classified into this category. For all the rest emails contain no such information, we put them into the OTHER category. This is the baseline of our project. 

2. Extract event and task information from the emails
Since we have put the emails into different categories, we also want to get the information we most interested in from the emails. For the EVENT emails, we want to get the time, the date, the locations, and the title of the events out of the emails. For the TODO emails, we want to know *WHAT* we need to do, and *WHO* is the person that gives us the tasks. We also want to organize the information well to make them easy to read. 

3. Context-aware information
We also want smarter information extracted. If we get an announcement about a tomorrow's meeting, we'd like our system get the current date from the email header and add 1 to get the actual date of the meeting. We also like to extract the names from the mail to imply who is inviting me to his party and the other participants. 

Approaches
----------
We first consider using a similar approach used in homework 3. Tokenize the emails and compute the similarity between the test email and the centroid of the emails have been classified. But this turns out to be inaccurate because information about date, time and location are most important in the classification, while they cannot simply match each other if we just tokenize the corpus word by word. 

So we use Named Entity Recognition to tag the tokens, and add the tags instead of the original words into the vectors. 

After we can get the class of the email, we can extract the needed information from the text. Instead of using approaches like [Hidden Markov Model][1], I use [pattern matching][2] to identify the information.

As time limits, we did the first the second goals we set and our system is able to extract the event and task information (more or less).

Implementation
--------------
The project is written in Python 2.7. We use the Stanford Named Entity Recognizer to tag the text. The learning set is selected from the [Enron Email Dataset](http://www.cs.cmu.edu/~enron/).

We use `manualclass.py` to classify and tag the emails manually, the results are passed to Stanford NER to generate our custom classifier. The classifier models generated are `model/event.ser.gz` and `model/todo.ser.gz`.

As Stanford NER is written in Java, we use its [Python interface](https://github.com/dat/pyner). `tagger.py` is a simple wrapper of it, using it we can start a NER server and tag the text we pass in.

[A Python implementation of Porter stemmer](https://pypi.python.org/pypi/stemming/1.0) is used in `porter2.py`.

`tokenizer.py` tokenize the text and compute the frequency vectors for each email. `folderfreq.py` computes the normalized frequency vectors for each category. `extractor.py` extracts the event and task information from the emails using pattern matching.

As we do not have enough time to create a sufficiently large learning set, the results shown by our system are not quite satisfying.

[1]: Almgren, Magnus, and Jenny Berglund. "Information extraction of Seminar information." CS224N: Final Project (2000): 1-12.
[2]: Black, Julie A., and Nisheeth Ranjan. "Automated event extraction from email." Final Report of CS224N/Ling237 Course in Stanford: http://nlp. stanford. edu/courses/cs224n/2004/, Spring (2004).
