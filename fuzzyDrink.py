# pip install fuzzingbook
import sys
import getopt
import rospy
from std_msgs.msg import String
from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.Grammars import is_valid_grammar, simple_grammar_fuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from grammar import get_grammar


def random_fuzz():
    random_fuzzer = RandomFuzzer()
    return random_fuzzer.fuzz()


def use_input(msg):
    global global_seed
    global_seed = msg.data


def get_seed(topic):
    global global_seed
    subscribed = rospy.Subscriber(topic, String, use_input, queue_size=1)
    print(global_seed)
    return str(global_seed)


def mutate_fuzz(seed_input, mutations):
    mutation_list = []
    mutation_fuzzer = MutationFuzzer(seed=seed_input)
    mutation_list += [mutation_fuzzer.fuzz() for i in range(mutations + 1)]
    del mutation_list[0]
    return mutation_list


def generate_fuzz(amount):
    GRAMMAR = get_grammar()
    assert is_valid_grammar(GRAMMAR)
    return [simple_grammar_fuzzer(GRAMMAR) for i in range(amount)]


def fuzzer(topic, rate, input, type):
    print({"Starting to fuzz " + topic + " using " + type + " with input: " + str(input)})
    pub = rospy.Publisher(topic, String, queue_size=1)  # nom du topic (sur rospy)
    rospy.init_node('fuzzer', anonymous=True)  # nom du noeud
    rate = rospy.Rate(rate)
    while not rospy.is_shutdown():
        try:
            if type == "random":
                pub.publish(input)
                rate.sleep()
            else:
                for i in range(len(input)-1):
                    pub.publish(input[i])
                    rate.sleep()
        except rospy.ROSInterruptException:
            pass
    return


def main(argv):
    help = (
        'Usage: fuzzyDrink.py -t <topic> -r <rate> [options...]\n'
        '-a, --random                               Random fuzzer\n'
        '-m, --mutation <seed>                      Mutation fuzzer\n'
        '-f, --mutation_file                        Mutation fuzzer using a ros subscription to topic\n'
        '-s, --size <size>                          For mutation fuzzer, the number of mutations\n'
        '-g, --grammar <population_size>            Grammar based fuzzer imported from grammar.py\n'
    )
    try:
        opts, args = getopt.getopt(argv, "ht:r:am:fs:g:",
                                   ["help", "random", "mutation=", "mutation_file", "size=", "grammar="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(help)
            sys.exit()
        elif opt == '-t':
            topic = arg
        elif opt == '-r':
            rate = float(arg)
        elif opt in ("-a", "--random"):
            type = "random"
            fuzz = random_fuzz()
        elif opt in ("-m", "--mutation"):
            seed_input = str(arg)
            for optm, argm in opts:
                if optm in ("-s", "--size"):
                    mutations = int(argm)
            type = "mutation"
            fuzz = mutate_fuzz([seed_input],mutations)
        elif opt in ("-f", "--mutation_file"):
            for optm, argm in opts:
                if optm in ("-s", "--size"):
                    mutations = int(argm)
            type = "mutation (with file)"
            fuzz = mutate_fuzz(get_seed(topic),mutations)
        elif opt in ("-g", "--grammar"):
            population_size = int(arg)
            type = "mutation (with file)"
            fuzz = generate_fuzz(population_size)
    fuzzer(topic, rate, fuzz, type)


if __name__ == '__main__':
    global global_seed
    global_seed = ""
    main(sys.argv[1:])
