# Naive bayes classifier for English language identification

# 1. Separate words into two groups -- English (0) and not-English (1).
# 2. Count within each group.
# 3. Adjust the counts by applying add-one smoothing. Add the UNKNOWN bigram.
# 4. Change the adjusted counts to probabilities.
# 5. Write a function that uses the probabilities to classify a word. To avoid underflow errors, add log-probabilities rather than multiplying the probabilities.
# 6. Apply the function to the test data.
# 7. Calculate precision and recall:
# - precision = number of machine said English and data said English
#              -------------------------------------------
#               number of machine said English
# - recall = number of machine said English and data said English
#            -------------------------------------------
#            number of data said English

import re

english_bigrams = {} # e.g. english_bigrams['th'] = 10 <-- 'th' is found 10 times in the English words
notenglish_bigrams = {}
english_count = 0 # start the counts at 0 (these counts are for the number of English and not-English words)
notenglish_count = 0

# 1. Separate words into two groups.

for line in open('words.train'):
	#splitted = line.split() # split line by white-space
	label = line[0] # the first element is the label (0 for English and 1 for not-English)
	letters = line[2:].strip() # the rest are letters (the letters in each word)
	letters = letters, '###'
	letters = ''.join(letters)
	moreletters = '#', letters
	moreletters = ''.join(moreletters)
	moremoreletters = '##', letters
	moremoreletters = ''.join(moremoreletters)
	moremoremoreletters = '###', letters
	moremoremoreletters = ''.join(moremoremoreletters)

	if label == '0':
		english_count += 1 # if the label is 0, increment the frequency for English words
	else:
		notenglish_count += 1

# 2. Identify and count bigrams within each group.

	pattern = '....'
	bigrams = re.findall(pattern, letters)
	morebigrams = re.findall(pattern, moreletters)
	moremorebigrams = re.findall(pattern, moremoreletters)
	moremoremorebigrams = re.findall(pattern, moremoremoreletters)
	allbigrams = bigrams + morebigrams + moremorebigrams + moremoremorebigrams

	for bigram in allbigrams:
		if label == '0':
		# increment frequency in english_bigrams
			if bigram in english_bigrams:
				english_bigrams[bigram] += 1 # if the bigram is already in the dictionary
			else: 
				english_bigrams[bigram] = 1 # if the bigram isn't in the dictionary, add it and assign the count to 1
		else:
		# increment frequency in notenglish_bigrams
			if bigram in notenglish_bigrams:
				notenglish_bigrams[bigram] += 1
			else:
				notenglish_bigrams[bigram] = 1

# 3. Smooth.

english_bigrams['<<>>'] = 0 # add a dummy bigram called '<>'
for bigram in english_bigrams:
	english_bigrams[bigram] += 1 # apply smoothing by adding 1 to each frequency
notenglish_bigrams['<<>>'] = 0
for bigram in notenglish_bigrams:
	notenglish_bigrams[bigram] += 1

# 4. To probabilities.
english_total = float(sum(english_bigrams.values())) # total number of bigrams in the English words, after application of smoothing and addition of dummy bigram
for bigram in english_bigrams:
	english_bigrams[bigram] /= english_total # P(bigram|English)

notenglish_total = float(sum(notenglish_bigrams.values()))
for bigram in notenglish_bigrams:
	notenglish_bigrams[bigram] /= notenglish_total # P(bigram|not-English)

english_prior = english_count / float(english_count+notenglish_count) # P(English) # probability that a word is English
notenglish_prior = notenglish_count / float(english_count+notenglish_count) # P(not English) # probability that a word is not English

# 5. The classifier function
def classify(input_bigrams, english_prior, notenglish_prior, english_bigrams, notenglish_bigrams):
	import math
	# 1. Calculate the English score.
	english_score = math.log(english_prior)
	for bigram in input_bigrams:
		english_score += math.log(english_bigrams.get(bigram, english_bigrams['<<>>'])) # look up the word's bigrams and calculate the English score (probability)
	# 2. Calculate the not-English score.
	notenglish_score = math.log(notenglish_prior)
	for bigram in input_bigrams:
		notenglish_score += math.log(notenglish_bigrams.get(bigram, notenglish_bigrams['<<>>']))
	# 3. Compare the two scores to classify.
	if english_score >= notenglish_score: # this is how the program decides whether an input word should be classified as English (0) or not-English (1)
		return '0'
	else:
		return '1'

#both_said_english = 0
#we_said_english = 0
#data_said_english = 0
tp = 0
fn = 0
fp = 0
tn = 0
test_file = open('words2.test')
for line in test_file:
	#ll = line.split()
	answer = line[0]
	input_letters = line[2:].strip()
	input_letters = input_letters, '###'
	input_letters = ''.join(input_letters)
	more_input_letters = '#', input_letters
	more_input_letters = ''.join(more_input_letters)
	more_more_input_letters = '##', input_letters
	more_more_input_letters = ''.join(more_more_input_letters)
	more_more_more_input_letters = '###', input_letters
	more_more_more_input_letters = ''.join(more_more_more_input_letters)

	pattern = '....'
	input_bigrams = re.findall(pattern, input_letters)
	more_input_bigrams = re.findall(pattern, more_input_letters)
	more_more_input_bigrams = re.findall(pattern, more_more_input_letters)
	more_more_more_input_bigrams = re.findall(pattern, more_more_more_input_letters)
	all_input_bigrams = input_bigrams + more_input_bigrams + more_more_input_bigrams + more_more_more_input_bigrams
	
	prediction = classify(all_input_bigrams, english_prior, notenglish_prior, english_bigrams, notenglish_bigrams)
#	print '# data: ', line.strip() # what the data said
#	print '# prediction: ', prediction # what the program predicts
	#if answer == '0': data_said_english += 1 # increment the counts
	#if prediction == '0': we_said_english += 1
	#if answer == '0' and prediction == '0': both_said_english += 1
	if answer == '0' and prediction =='0' : tp += 1
	if answer == '1' and prediction == '0': fp += 1 
	if answer == '0' and prediction =='1' : fn += 1
	if answer == '1' and prediction == '1' : tn += 1
test_file.close()

'''print 'data', data_said_english
print 'we', we_said_english
print 'both', both_said_english

precision = float(both_said_english) / we_said_english
recall = float(both_said_english) / data_said_english'''

accuracy = float(tp + tn) / (tp + fp + tn +fn)
precision = float(tp)/(tp + fp)
recall = float(tp)/ (tp + fn)
fscore = float(precision*recall)/(precision + recall)

print 'accuracy = ', accuracy
print 'precision = ', precision
print 'recall = ', recall
print 'f-score = ',fscore
