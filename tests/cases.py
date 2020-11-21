
#### All the test cases for PRINT ####
PRINT_TESTCASE_DICT = {}

PRINT_TESTCASE_DICT["print_testcase_1"] = ["moshi_moshi(1.0 + 1) meow", 2.0]
PRINT_TESTCASE_DICT["print_testcase_2"] = [
    "moshi_moshi([1, 1, 2, (5 + 5)]) meow", [1, 1, 2, 10]]
PRINT_TESTCASE_DICT["print_testcase_3"] = [
    "moshi_moshi(waifu |0| [1, 1, 2, (5 + 5)]) meow", 1]
PRINT_TESTCASE_DICT["print_testcase_4"] = [
    "moshi_moshi(waifu |0| [(1 + 1), 2, (5 + 5)]) meow", 2]
PRINT_TESTCASE_DICT["print_testcase_5"] = [
    "moshi_moshi([(1 + 1), (5 * 5), (10 / 10)]) meow", [2, 25, 1]]


#### All the test cases for basic arithemetic ops ####
ARITHMETIC_TESTCASE_DICT = {}

ARITHMETIC_TESTCASE_DICT["calc_testcase_1"] = ["(1.0 - 1)", 0]
ARITHMETIC_TESTCASE_DICT["calc_testcase_2"] = [
    "(((1 + 10) * 22) + 69) - 10 / 30", 310.6666666666667]
ARITHMETIC_TESTCASE_DICT["calc_testcase_3"] = [
    "-1 - 2.0 - 3.0", -6.0]
ARITHMETIC_TESTCASE_DICT["calc_testcase_4"] = [
    "(10 * 10 + ( 20 - 10 / 5))", 118.0]

#### All the test cases for variables ####

VARIABLE_TESTCASE_DICT = {}

VARIABLE_TESTCASE_DICT["var_testcase_1"] = ["new tsundere touka = 10 meow", 10]
VARIABLE_TESTCASE_DICT["var_testcase_2"] = ["touka*10", 100]
VARIABLE_TESTCASE_DICT["var_testcase_3"] = ["new yandere yuno = 11 meow", 11]
VARIABLE_TESTCASE_DICT["var_testcase_4"] = ["yuno*touka", 110]
VARIABLE_TESTCASE_DICT["var_testcase_5"] = ["yuno*touka+yuno/touka", 111.1]
VARIABLE_TESTCASE_DICT["var_testcase_6"] = ["new harem ki = [touka, yuno, 13] meow", [10,11,13]]
VARIABLE_TESTCASE_DICT["var_testcase_7"] = ["waifu |0| ki", 10]
VARIABLE_TESTCASE_DICT["var_testcase_7"] = ["ki", [10,11,13]]
VARIABLE_TESTCASE_DICT["var_testcase_8"] = ["waifu |1 + 0| ki", 11]
VARIABLE_TESTCASE_DICT["var_testcase_9"] = ["( waifu |1 + 0| ki ) * 10", 110]

#### All the test cases for conditionals ####

CONDITIONALS_TESTCASE_DICT = {}

CONDITIONALS_TESTCASE_DICT["conditionals_testcase_1_a"] = ["create_ship(10 |X| 10) {new tsundere kaori = 50 meow} meow", "kawai"]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_1_b"] = ["kaori", 50]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_2_a"] = ["create_ship(kaori |X| 10) {new yandere ami = 40 meow} nani {waifu kaori = 50 - 10 meow} meow", "kawai"]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_2_b"] = ["kaori", 40]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_3_a"] = ["create_ship(kaori |X| 40) {create_ship(1 |X| 1){ new yandere ami = 40 meow } meow } nani {waifu kaori = 50 - 10 meow} meow", "baaka"]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_3_b"] = ["kaori", 40]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_3_c"] = ["ami", 40]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_4_a"] = ["create_ship(kaori |X| 30) {waifu kaori = 50 - 10 meow} nani {new harem ki = [1,2,2] meow create_ship(1 |X| 1){ waifu |0| ki = 10 meow} meow} meow", "kawai"]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_4_b"] = ["kaori", 40]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_4_c"] = ["ki", [10,2,2]]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_5_a"] = ["""create_ship(kaori |X| 40) {waifu kaori = kaori - 10 meow create_ship(kaori |X| 30){ waifu kaori = kaori - 10 meow } meow } nani
                                                           {new harem ki = [1,2,2] meow } meow""", "baaka"]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_5_b"] = ["ki", [10,2,2]]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_5_c"] = ["kaori", 20]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_6_a"] = ["create_ship((kaori - 20) |X| ((waifu |0| ki) - 10)) {new yandere yui = 40 meow} nani {waifu kaori = 50 - 10 meow} meow", "baaka"]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_6_b"] = ["kaori", 20]
CONDITIONALS_TESTCASE_DICT["conditionals_testcase_6_c"] = ["yui", 40]

