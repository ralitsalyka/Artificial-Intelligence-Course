import pandas as pd
from numpy import log
from magic_str import *
from time import sleep
from statistics import mean


class NaiveBayesClassifier:
    def __init__(self):
        self.data = self.read_data()

    def create_column(self):
        columns = []
        columns.append(CLASS)
        for i in range(1, 17):
            columns.append(C + str(i))
        return columns

    def read_data(self):
        columns = self.create_column()
        data = pd.read_csv(dataname, names=columns)
        return data

    def find_democrats_count(self, data, dem_count, len_of_data):
        return dem_count / len_of_data

    def find_republicans_count(self, data, rep_count, len_of_data):
        return rep_count / len_of_data

    def len_of_data(self, data):
        return len(data)

    def shuffle_data(self, data):
        return data.sample(frac=1)

    def create_prob(self, data):
        prediction = {DEM: 0, REP: 0}
        for i in range(1, 17):
            prediction[d + str(i) + y] = 0
            prediction[d + str(i) + n] = 0
            prediction[d + str(i) + q] = 0
            prediction[r + str(i) + y] = 0
            prediction[r + str(i) + n] = 0
            prediction[r + str(i) + q] = 0
            current_column = list(data[CLASS])
        return prediction, current_column

    def count_occur(self, data, prediction, current_column):
        for i in range(1, 17):
            x_column = list(data[C + str(i)])
            c = 0
            for j in x_column:
                prediction[current_column[c][0] + '_c' + str(i) + line + str(j)] += 1
                c += 1

    def prediction(self, data, column):
        prediction = self.create_prob(data)[0]
        data_class_column_list = self.create_prob(data)[1]
        data_class_column_len = len(data_class_column_list)
        democrats_count = data_class_column_list.count(DEM)
        republicans_count = data_class_column_list.count(REP)
        prediction[DEM] = democrats_count / data_class_column_len
        prediction[REP] = republicans_count / data_class_column_len
        self.count_occur(data, prediction, data_class_column_list)

        #Laplace Smoothing
        for i in range(1, 17):

            prediction[d + str(i) + y] += 1
            prediction[d + str(i) + n] += 1
            prediction[d + str(i) + q] += 1
            prediction[r + str(i) + y] += 1
            prediction[r + str(i) + n] += 1
            prediction[r + str(i) + q] += 1

            prediction[d + str(i) + y] /= democrats_count
            prediction[d + str(i) + n] /= democrats_count
            prediction[d + str(i) + q] /= democrats_count
            prediction[r + str(i) + y] /= republicans_count
            prediction[r + str(i) + n] /= republicans_count
            prediction[r + str(i) + q] /= republicans_count
        return prediction

    def find_for_current_set(self, set_of_ten, test_dataset, prediction, i):
        for elem in range(set_of_ten):
            row = list(test_dataset.iloc[elem])
            class_of_current_row = row[0]
            features = row[1:]
            prob_of_democrat = 0
            prob_of_republican = 0
            for h in range(1, 17):
                prob_of_democrat += log(prediction[d + str(h) + line + features[h - 1]])
                prob_of_republican += log(prediction[r + str(h) + line + features[h - 1]])
            class_predict = self.check_for_prob(prob_of_democrat, prob_of_republican)
            prev_occur = occur[i]
            new_occur = (prev_occur[0], prev_occur[1] + 1)
            if class_predict == class_of_current_row:
                new_occur = (prev_occur[0] + 1, prev_occur[1] + 1)
            occur[i] = new_occur
        return occur

    def check_for_prob(self, prob_of_democrat, prob_of_republican):
        if prob_of_democrat > prob_of_republican:
            class_predict = DEM
        else:
            class_predict = REP
        return class_predict

    def log_of_democrat(self, prediction, index, features):
        return log(prediction[d + str(index) + line + features[index - 1]])

    def log_of_republican(self, prediction, index, features):
        return log(prediction[r + str(index) + line + features[index - 1]])

    def ten_fold_cross_validation(self, data, data_len, column):
        set_of_ten = int(data_len / 10)
        for i in range(9):
            test_dataset = data.iloc[i * set_of_ten:(i + 1) * set_of_ten]
            dataset_train_1 = data.iloc[0:i * set_of_ten]
            dataset_train_2 = data.iloc[(i + 1) * set_of_ten:]
            dataset_train = dataset_train_1.append(dataset_train_2)
            prediction = self.prediction(dataset_train, column)
            occur = self.find_for_current_set(set_of_ten, test_dataset, prediction, i)
        test_dataset = data.iloc[9 * set_of_ten:]
        dataset_train = data.iloc[: 9 * set_of_ten]
        prediction = self.prediction(dataset_train, column)
        for j in range(len(list(test_dataset[CLASS]))):
            row = list(test_dataset.iloc[j])
            class_of_current_row = row[0]
            features = row[1:]
            prob_of_democrat = 0
            prob_of_republican = 0
            for c in range(1, 17):
                prob_of_democrat += self.log_of_democrat(prediction, c, features)
                prob_of_republican += self.log_of_republican(prediction, c, features)
            class_predict = self.check_for_prob(prob_of_democrat, prob_of_republican)
            prev_occur = occur[9]
            new_occur = (prev_occur[0], prev_occur[1] + 1)
            if class_predict == class_of_current_row:
                new_occur = (prev_occur[0] + 1, prev_occur[1] + 1)
            occur[9] = new_occur
        return occur

    def steps(self):
        col = self.create_column()
        data = self.read_data()
        new_data = self.shuffle_data(data)
        len_of_data = len(list(new_data[CLASS]))
        occur = self.ten_fold_cross_validation(new_data, len_of_data, col)
        return occur


if __name__ == '__main__':
    init = NaiveBayesClassifier()
    final_result = init.steps()
    count = 1
    for res in final_result:
        sleep(1)
        print(str(count) + '-------------')
        print(str(res[0]) + '/' + str(res[1]) + '-' + str(round(res[0] / res[1] * 100))  + '%')
        count += 1
    average = round(mean([i[0] / i[1] for i in final_result]) * 100)
    print('Average: ' + str(average) + '%')
         
