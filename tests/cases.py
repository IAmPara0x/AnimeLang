
#### All the test cases for PRINT ####
PRINT_TESTCASE_DICT = {}

PRINT_TESTCASE_DICT["testcase_1"] = ["moshi_moshi(1.0 + 1) meow", 2.0]
PRINT_TESTCASE_DICT["testcase_2"] = [
    "moshi_moshi([1, 1, 2, (5 + 5)]) meow", [1, 1, 2, 10]]
PRINT_TESTCASE_DICT["testcase_3"] = [
    "moshi_moshi(waifu {0} [1, 1, 2, (5 + 5)]) meow", 1]
PRINT_TESTCASE_DICT["testcase_4"] = [
    "moshi_moshi(waifu {0} [(1 + 1), 2, (5 + 5)]) meow", 2]
PRINT_TESTCASE_DICT["testcase_5"] = [
    "moshi_moshi([(1 + 1), (5 * 5), (10 / 10)]) meow", [2, 25, 1]]


#### All the test cases for basic arithemetic ops ####
ARITHMETIC_TESTCASE_DICT = {}

ARITHMETIC_TESTCASE_DICT["testcase_1"] = ["(1.0 - 1)", 0]
ARITHMETIC_TESTCASE_DICT["testcase_2"] = [
    "(((1 + 10) * 22) + 69) - 10 / 30", 310.6666666666667]
ARITHMETIC_TESTCASE_DICT["testcase_3"] = [
    "-1 - 2.0 - 3.0", -6.0]
ARITHMETIC_TESTCASE_DICT["testcase_4"] = [
    "(10 * 10 + ( 20 - 10 / 5))", 118.0]
