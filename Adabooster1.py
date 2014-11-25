from random import randrange
import math
HomeDirectory = "/home/panindra/Desktop/Dm/Assignments/Assignment4/dataset/"
training_models = {}

with open(HomeDirectory+ "led.train")as f:
    training_data = f.readlines()

with open(HomeDirectory+ "led.test")as f:
    test_data = f.readlines()

def getMaxLengthOfAttributes(data):
    max_attribute_val = 0
    for line in data:
        words = line.split()
        last_attr_value = int(words[len(words) - 1].split(":")[0])

        if(last_attr_value> max_attribute_val):
            max_attribute_val = last_attr_value
    return max_attribute_val

def fillAttrDict(attr, attr_dict):
    if not attr in attr_dict:
        attr_dict.update({attr: 1})
    else :
        attr_dict.update({attr: int(attr_dict.get(attr)) + 1})


def find_TP_FN_FP_TN(p_of_class_a, p_attr_with_class_a_dict, p_of_class_b, p_attr_with_class_b_dict, dataset):
    max_train_attributes = getMaxLengthOfAttributes(training_data)
    max_test_attributes = getMaxLengthOfAttributes(test_data)

    max_attr = max_test_attributes if (max_test_attributes > max_train_attributes) else max_train_attributes
    range_of_attr = range(1, max_attr + 1)

    data_set = dataset
    missclassification_list_count = 0
    missclassification_list = []

    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    attr_present_in_eachLine_a = []
    attr_present_in_eachLine_b = []


    for line in data_set:
        words = line.split()
        val_a = 1
        val_b = 1

        del attr_present_in_eachLine_a[:]
        del attr_present_in_eachLine_b[:]

        for attr in words[1: len(words)]:
            if attr in p_attr_with_class_a_dict:
                attr_present_in_eachLine_a.append(int(attr.split(":")[0]))
                val_a = val_a * p_attr_with_class_a_dict.get(attr)

            if attr in p_attr_with_class_b_dict:
                attr_present_in_eachLine_b.append(int(attr.split(":")[0]))
                val_b = val_b * p_attr_with_class_b_dict.get(attr)

        missed_ele = list( set(range_of_attr) - set(attr_present_in_eachLine_a) )
        for i in missed_ele:
            ele = "{0}:{1}".format(i,0)
            if ele in p_attr_with_class_a_dict:
                val_a = val_a * p_attr_with_class_a_dict.get(ele)

        missed_ele = list( set(range_of_attr) - set(attr_present_in_eachLine_b) )
        for i in missed_ele:
            ele = "{0}:{1}".format(i,0)
            if ele in p_attr_with_class_b_dict:
                val_b = val_b * p_attr_with_class_b_dict.get(ele)

        val_a = val_a *  p_of_class_a
        val_b = val_b * p_of_class_b
        class_of_this_instance = +1 if (val_a > val_b) else -1

        if(int(words[0]) != class_of_this_instance):
            missclassification_list.append(missclassification_list_count)

        missclassification_list_count = missclassification_list_count + 1

        if class_of_this_instance == +1 and class_of_this_instance == int(words[0]):
            true_positive = true_positive + 1
        elif class_of_this_instance == +1 and class_of_this_instance != int(words[0]):
            false_positive = false_positive + 1
        elif class_of_this_instance == -1 and class_of_this_instance != int(words[0]):
            false_negative = false_negative + 1
        elif class_of_this_instance == -1 and class_of_this_instance == int(words[0]):
            true_negative = true_negative + 1

    print(true_positive, false_negative, false_positive, true_negative )
    return missclassification_list

def computeClassifier(range_of_attr, dataset, currentRound):
    class_labels_dict = {}
    attr_dict_a = {}
    attr_dict_b = {}
    total_set = 0
    class_a = 0
    class_b = 0
    p_attr_with_class_a_dict = {}
    p_attr_with_class_b_dict = {}
    p_of_class_a = 0
    p_of_class_b = 0
    attr_present_in_eachLine = []
    missing_attr_dict = {}
    classLabel = ""
    words = []

    for line in dataset:
        words = line.split()
        del attr_present_in_eachLine[:]
        for attr in words:
            if(attr.find(":") > 0):
                attr_present_in_eachLine.append(int(attr.split(":")[0]))
            if (words[0] == "+1"):
                classLabel = "a"
                fillAttrDict(attr, attr_dict_a)
            else:
                classLabel = "b"
                fillAttrDict(attr, attr_dict_b)

        missed_ele = list( set(range_of_attr) - set(attr_present_in_eachLine) )
        if len(missed_ele):
            if(classLabel == "a"):
                dict = attr_dict_a
            else:
                dict = attr_dict_b

            for i in missed_ele:
                ele = "{0}:{1}".format(i,0)
                if ele not in dict:
                    dict.update({ele : 1})
                else:
                    dict.update({ele : dict.get(ele) + 1})

        total_set = total_set + 1


    class_a = attr_dict_a.get("+1")
    class_b = attr_dict_b.get("-1")

    attr_dict_a.pop("+1")
    attr_dict_b.pop("-1")

    for attr in attr_dict_a:
        p_attr_with_class_a_dict.update({attr: (float(attr_dict_a.get(attr))/float(class_a)) })

    for attr in attr_dict_b:
        p_attr_with_class_b_dict.update({attr: (float(attr_dict_b.get(attr))/float(class_b)) })

    p_of_class_a = float(class_a) / float(total_set)
    p_of_class_b = float(class_b) / float(total_set)

    error_list = find_TP_FN_FP_TN(p_of_class_a, p_attr_with_class_a_dict, p_of_class_b, p_attr_with_class_b_dict, dataset)
    training_models.update({currentRound: [p_of_class_a, p_attr_with_class_a_dict, p_of_class_b, p_attr_with_class_b_dict]})
    return error_list
    #find_TP_FN_FP_TN(p_of_class_a, p_attr_with_class_a_dict, p_of_class_b, p_attr_with_class_b_dict, "test")

def calculateError(weight_of_tuple, error_list):
    sum = 0
    for i in error_list:
        sum = sum + weight_of_tuple[i]
    print(sum)
    return sum

def main():
    random_sample = int(len(training_data) * 0.8)
    weight_of_tuples = []
    random_numbers = []
    k = 4
    currentRound = 0

    max_train_attributes = getMaxLengthOfAttributes(training_data)
    max_test_attributes = getMaxLengthOfAttributes(test_data)

    max_attr = max_test_attributes if (max_test_attributes > max_train_attributes) else max_train_attributes
    range_of_attr = range(1, max_attr + 1)

    currentRound = 0
    error_list = 0
    error_models = []

    m = 0
    while m < random_sample:
        weight_of_tuples.append(1/float(random_sample))
        m = m + 1

    while currentRound < k:
        del random_numbers[:]

        while 1:
            i = 0
            while i < random_sample:
                random_number = randrange(len(training_data))
                if not random_number in random_numbers:
                    random_numbers.append(random_number)
                i = i + 1

            sample = []

            for i in random_numbers:
                sample.append(training_data[i])

            error_list = computeClassifier(range_of_attr, sample, currentRound)
            error_models.append(calculateError(weight_of_tuples, error_list))

            if(error_models[currentRound] < 0.5):
                break;

        i = 0
        while i < random_sample:
            if not i in error_list:
                weight_of_tuples[i] = weight_of_tuples[i] * (error_models[currentRound] / (1 - error_models[currentRound]))
            i = i + 1

        currentRound = currentRound + 1

    no_of_rounds = 0
    weight_of_classifiers = []
    classifiers = []

    while no_of_rounds < k:
        weight_of_classifiers.append(0)
        no_of_rounds = no_of_rounds + 1

    current_classifer = 0
    while current_classifer < k:
        weight_of_classifiers[current_classifer] = math.log((error_models[current_classifer] / (1 - error_models[current_classifer])))
        current_classifer = current_classifer + 1

    index = int(weight_of_classifiers.index(max(weight_of_classifiers)))

    prob_class_a_training_model = training_models.get(index)[0]
    p_attr_with_class_a_dict = training_models.get(index)[1]
    prob_class_b_training_model = training_models.get(index)[2]
    p_attr_with_class_b_dict = training_models.get(index)[3]

    classifiers = find_TP_FN_FP_TN(prob_class_a_training_model, p_attr_with_class_a_dict, prob_class_b_training_model, p_attr_with_class_b_dict, training_data)

if __name__ == "__main__":
    main()
