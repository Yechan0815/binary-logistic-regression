import sys
import csv
import math

class DataDescribe:
    def __init__(self):
        self.__data__ = []
        # count, mean, var, std, min, 25%, 50%, 75%, max
        self.__feature__ = []

    def __is_numeric__(self, rows):
        is_numeric = True
        try:
            float(rows[1])
        except:
            is_numeric = False
        return is_numeric

    def __count__(self, rows):
        return len(rows) - 1

    def __mean__(self, rows):
        sum = 0.0
        for i in range(1, len(rows)):
            sum += rows[i]
        return sum / len(rows)

    def __var__(self, rows, mean):
        sum = 0.0
        for i in range(1, len(rows)):
            sum += (rows[i] - mean) ** 2
        return sum / len(rows)

    def __std__(self, var):
        return math.sqrt(var)

    def read_csv(self, path):
        # read
        with open(path, 'r', encoding='utf-8') as file:
            csvReader = csv.reader(file)
            for column in csvReader.__next__():
                self.__data__.append([column])
            for row in csvReader:
                for column in range(0, len(row)):
                    self.__data__[column].append(row[column])
        # convert
        for i in range(0, len(self.__data__)):
            if (self.__is_numeric__(self.__data__[i]) == False):
                continue
            for j in range(1, len(self.__data__[i])):
                if (self.__data__[i][j] == ''):
                    self.__data__[i][j] = 0
                else:
                    self.__data__[i][j] = float(self.__data__[i][j])

    def iterate(self, func, index):
        self.__data__[index][1:] = map(func, self.__data__[index][1:])

    def analyze_feature(self):
        for i in range(0, len(self.__data__)):
            if (self.__is_numeric__(self.__data__[i]) == False):
                self.__feature__.append('NULL')
                continue
            # count, mean
            self.__feature__.append([
                self.__count__(self.__data__[i]), 
                self.__mean__(self.__data__[i]),
                ])
            # var, std
            self.__feature__[i].append(self.__var__(self.__data__[i], self.__feature__[i][1]))
            self.__feature__[i].append(self.__std__(self.__feature__[i][2]))

            sorted_temp = sorted(self.__data__[i][1:])
            # min
            self.__feature__[i].append(sorted_temp[0]) 
            # 25%
            least = 0
            if len(sorted_temp) % 2 == 0:
                most = len(sorted_temp) / 2 - 2
            else:
                most = int(len(sorted_temp) / 2) - 1
            if (most - least + 1) % 2 == 0:
                self.__feature__[i].append((sorted_temp[int((most + least + 1) / 2 - 1)] + sorted_temp[int((most + least + 1) / 2)]) / 2)
            else:
                self.__feature__[i].append(sorted_temp[int((most + least + 1) / 2)])
            # 50%
            most = len(sorted_temp) - 1
            if (most - least + 1) % 2 == 0:
                self.__feature__[i].append((sorted_temp[int((most + least + 1) / 2 - 1)] + sorted_temp[int((most + least + 1) / 2)]) / 2)
            else:
                self.__feature__[i].append(sorted_temp[int((most + least + 1) / 2)])
            # 75%
            if len(sorted_temp) % 2 == 0:
                least = len(sorted_temp) / 2 + 1
            else:
                least = int(len(sorted_temp) / 2) + 2
            if (most - least + 1) % 2 == 0:
                self.__feature__[i].append((sorted_temp[int((most + least + 1) / 2 - 1)] + sorted_temp[int((most + least + 1) / 2)]) / 2)
            else:
                self.__feature__[i].append(sorted_temp[int((most + least + 1) / 2)])
            # max
            self.__feature__[i].append(sorted_temp[len(sorted_temp) - 1])
    
    def print_feature(self):
        # field
        print('{0:35}'.format('') + '|', end='')
        for index in ['Count |', 'Mean |', 'Std |', 'Min |', '25% |', '50% |', '75% |', 'Max |']:
            print('{0:>17}'.format(index), end='')
        print()
        for i in range(0, len(self.__data__)):
            print('{0:35}'.format(self.__data__[i][0]), end='')
            if (self.__is_numeric__(self.__data__[i]) == False):
                print('-- Non-numerical features --'.center(16 * 8 + 10))
                continue
            print('|', end='')
            for i in (self.__feature__[i][0:2] + self.__feature__[i][3:]):
                print('{0:>17}'.format(str('{:.5f}'.format(i)) + ' |'), end='')
            print()

    def make_copy(self, columns, min = -1, max = -1):
        if min == -1:
            min = 1
        if max == -1:
            max = len(self.__data__[0])
        copy = DataDescribe()
        copy.__data__ = []
        copy.__feature__ = []
        for i in columns:
            copy.__data__.append(self.__data__[i][0:1] + self.__data__[i][min:max])
        copy.analyze_feature()
        return copy

def main():
    if len(sys.argv) != 2:
        print("usage:")
        print(" python describe.py [.csv]")
        return

    describer = DataDescribe()
    describer.read_csv(sys.argv[1])
    describer.analyze_feature()
    describer.print_feature()

if __name__ == "__main__":
    main()