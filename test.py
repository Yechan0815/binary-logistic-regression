from describe import DataDescribe

def main():
    describer = DataDescribe()
    describer.read_csv("titanic.csv")
    describer.iterate(lambda sex: 1 if sex == "male" else 0, 3)

    print()
    print()

    nd: DataDescribe = describer.make_copy([1, 3, 4, 5, 6, 7], 1, 601)
    nd.print_feature()
    print('\n\n')

    answer_s: DataDescribe = describer.make_copy([0], 601)
    answer_q: DataDescribe = describer.make_copy([1, 3, 4, 5, 6, 7], 601)
    answer_s.print_feature()
    print('\n\n')
    answer_q.print_feature()

if __name__ == "__main__":
    main()