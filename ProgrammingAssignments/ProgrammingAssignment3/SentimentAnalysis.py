import sys
import re

training_file = ''
test_file = ''


# using inputfile to build a vocabulary list
# return vocabulary list which is sorted without upper case letters, and every word is unique
def Form_Vocabulary_List(inputfile):
    fp = open(inputfile, 'r') # open a file for reading with read only mode
    lines = fp.readlines()  # read the whole file and saved in varaible 'line' line by line
    fp.close() # finish reading
    vocabulary_list = [] 
    count = 0
    for line in lines:
        line = line.strip() # Get rid of the newline character
        line = re.sub(r'[^\w\s]', '', line) # Get rid of the punctuations
        line = line.lower() # convert everything to lower case
        line = line[:-1] # remove class lable from strings
        words_list = line.split()
        for word in words_list: # for every word in the words list
            if word not in vocabulary_list and not word.isnumeric(): # if that word is unique, add it into the vocabulary list
                vocabulary_list.append(word)
            else:
                pass # if word already in the vocabulary list, ignore it 
    vocabulary_list.sort() # sort the vocabulary alphabetically
    return vocabulary_list


def Pre_Process_Data(inputfile, vocabulary):
    fp = open(inputfile, 'r') # open a file for reading with read only mode
    lines = fp.readlines()  # read the whole file and saved in varaible 'line' line by line
    fp.close()
    training_data = []
    for line in lines:
        line = line.strip() # Get rid of the newline character
        line = re.sub(r'[^\w\s]', '', line) # Get rid of the punctuations
        line = line.lower() # convert everything to lower case
        classlabel = line[-1]
        line = line[:-1] # remove class lable from strings
        words_list = line.split()
        temp_list = []
        for v in vocabulary:
            if v in words_list:
                temp_list.append(1)
            else:
                temp_list.append(0)
        temp_list.append(int(classlabel))
        # add temp_list into training_data
        training_data.append(temp_list)
    return training_data
        

def Output_Pre_Processed_Data(train_d, test_d, vocabulary):
    train_fp = open("preprocessed_train.txt", 'w')
    test_fp = open("preprocessed_test.txt", 'w')
    # writing first line to both files
    for i in vocabulary:
        train_fp.write(i + ', ')
        test_fp.write(i + ', ')
    train_fp.write('classlabel\n')
    test_fp.write('classlabel\n')

    # writing preprocessed data into two files
    for i in range(len(train_d)):
        for k in range(len(train_d[i])):
            if k != len(train_d[i]) - 1:
                train_fp.write(str(train_d[i][k]) + ', ')
            else:
                train_fp.write(str(train_d[i][k]))
        train_fp.write('\n')
    
    for i in range(len(test_d)):
        for k in range(len(test_d[i])):
            if k != len(test_d[i]) - 1:
                test_fp.write(str(test_d[i][k]) + ', ')
            else:
                test_fp.write(str(test_d[i][k]))
        test_fp.write('\n')


    train_fp.close()
    test_fp.close()


def Get_Num_Classlabel_1(preprocessed_data):
    count = 0
    for i in range(len(preprocessed_data)):
        if preprocessed_data[i][-1] == 1:
            count += 1
    return count


def Differentiate_Reviews_From_Training_Data(training_data):
    positive_reviews = []
    negative_reviews = []
    for i in range(len(training_data)):
        if training_data[i][-1] == 1:
            positive_reviews.append(training_data[i])
        else:
            negative_reviews.append(training_data[i])
    return positive_reviews, negative_reviews


def Get_prob_vocabulary_give_positive(vocabulary, positive_reviews):
    num_positive_reviews = len(positive_reviews)
    prob_vocabulary_given_positive = []
    for i in range(len(vocabulary)):
        count = 0
        for singleReview in positive_reviews:
            if singleReview[i] == 1:
                count += 1
        # at this point, count presents how many positive reviews have the word vocabulary[i]
        prob_vocabulary_given_positive.append((count+1)/(num_positive_reviews+2))
    return prob_vocabulary_given_positive


def Get_prob_vocabulary_give_negative(vocabulary, negative_reviews):
    num_negative_reviews = len(negative_reviews)
    prob_vocabulary_given_negative = []
    for i in range(len(vocabulary)):
        count = 0
        for singleReview in negative_reviews:
            if singleReview[i] == 1:
                count += 1
        # at this point, count presents how many positive reviews have the word vocabulary[i]
        prob_vocabulary_given_negative.append((count+1)/(num_negative_reviews+2))
    return prob_vocabulary_given_negative


def Naive_Bayes_Classifer(vocabulary,test_data, prob_of_positive, prob_of_negative, prob_vocabulary_given_positive, prob_vocabulary_given_negative):
    count_of_correct_estimation = 0
    total = len(test_data)
    for singleReview in test_data:
        flag = -1
        prob_posit = prob_of_positive
        prob_negat = prob_of_negative
        for i in range(len(singleReview)-1):
            if singleReview[i] == 1:
                prob_posit *= prob_vocabulary_given_positive[i]
                prob_negat *= prob_vocabulary_given_negative[i]
        if prob_posit > prob_negat:
            flag = 1
        else:
            flag = 0
        if flag == singleReview[-1]:
            count_of_correct_estimation += 1
    correctness = count_of_correct_estimation/total
    return correctness


def SentimentAnalysis():
    outFp = open('results.txt', 'w')
    # get vocabulary list from training dataset
    vocabulary_list = Form_Vocabulary_List(training_file)
    training_data = Pre_Process_Data(training_file, vocabulary_list)
    test_data = Pre_Process_Data(test_file, vocabulary_list)
    Output_Pre_Processed_Data(training_data,test_data, vocabulary_list)
    num_positive_reviews_in_training_data = Get_Num_Classlabel_1(training_data)
    num_negative_reviews_in_training_data = len(training_data) - num_positive_reviews_in_training_data
    # calculating the P(1) which is prior prob
    prob_of_positive = num_positive_reviews_in_training_data/len(training_data)
    # calculating the P(0) which is prior prob
    prob_of_negative = 1 - prob_of_positive
    # differentiate positive and negative reviews from training data
    positive_reviews, negative_reviews = Differentiate_Reviews_From_Training_Data(training_data)
    # calculate Probability of all Vocabulary given it is positive
    prob_vocabulary_given_positive = Get_prob_vocabulary_give_positive(vocabulary_list,positive_reviews)
    # calculate probablity of all vocabulary given it is negative
    prob_vocabulary_given_negative = Get_prob_vocabulary_give_negative(vocabulary_list,negative_reviews)
    
    correctness1 = Naive_Bayes_Classifer(vocabulary_list, training_data, prob_of_positive, prob_of_negative, prob_vocabulary_given_positive, prob_vocabulary_given_negative)
    correctness2 = Naive_Bayes_Classifer(vocabulary_list, test_data, prob_of_positive, prob_of_negative, prob_vocabulary_given_positive, prob_vocabulary_given_negative)
    outFp.write("Training dataset filename: " + training_file + "\nTest dataset filename: " + training_file + "\n\tAccuracy: %" + str(correctness1*100) + "\n")
    outFp.write("Training dataset filename: " + training_file + "\nTest dataset filename: " + test_file + "\n\tAccuracy: %" + str(correctness2*100) + "\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Not enough commandline arguments!")
        print("Usage: python3 SentimentAnalysis.py trainingSet.text testSet.txt")
    else:
        training_file = sys.argv[1]
        test_file = sys.argv[2]
        SentimentAnalysis()
    '''
    for i in range(len(vocabulary_list)):
        if training_data[1][i] == 1:
            print(vocabulary_list[i])'''