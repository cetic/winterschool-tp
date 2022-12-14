# pip install fuzzingbook
# pip install rospy
import sys
import getopt
import rospy
from std_msgs.msg import String
from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.Grammars import is_valid_grammar, simple_grammar_fuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from grammar import get_grammar


def get_topics():
    rospy.init_node('fuzzer', anonymous=True)
    topiclist_raw = rospy.get_published_topics()
    if len(topiclist_raw) != 0:
        topiclist=[]
        for i in topiclist_raw:
            topiclist.append(i[0][1:])
        choice = get_choice(topiclist, "Please choose a topic in the list:\n")
        return topiclist[choice]
    else:
        return "notopic"


def get_choice(messages, probe):
    ok = False
    print("Choose your destiny:")
    for i in range(len(messages)):
        print(str(i + 1)+" : "+str(messages[i]))
    while not ok:
        try:
            choice = int(input(probe))
        except Exception as e:
            print(e)
        if (choice < 1 or choice > 10):
            print("Please use a suitable input and stop fuzzing arround")
        else:
            ok = True
    return choice - 1


def get_seed(msg):
    global topic
    global rate
    global mutations
    global seed_candidates
    global subscribed
    global asked

    if not asked:
        if len(seed_candidates) < 10:
            seed_candidates.append(msg.data)
        else:
            choice = get_choice(seed_candidates, "Please choose a suitable input to use as fuzzing base:\n")
            asked = True
            seed = seed_candidates[choice]
            fuzz = mutate_fuzz([seed], mutations)
            fuzzer(topic, rate, fuzz, "Mutation (with files)")
            subscribed.unregister()


def random_fuzz():
    random_fuzzer = RandomFuzzer()
    return random_fuzzer.fuzz()
    

def mutate_fuzz(seed_input, mutations):
    mutation_list = []
    #coverage
    for i in range(mutations):
        mutation_fuzzer = MutationFuzzer(seed=seed_input)
        mutation_list.append([mutation_fuzzer.fuzz() for j in range(2)][1])

    return mutation_list


def generate_fuzz(population):
    GRAMMAR = get_grammar()
    assert is_valid_grammar(GRAMMAR)
    return [simple_grammar_fuzzer(GRAMMAR) for i in range(population)]


def fuzzer(topic, rate, input, type):
    print({"Starting to fuzz " + topic + " using " + type})
    pub = rospy.Publisher(topic, String, queue_size=1)
    rospy.init_node('fuzzer', anonymous=True)
    rosrate = rospy.Rate(rate)
    while not rospy.is_shutdown():
        try:
            if type == "random":
                pub.publish(input)
                print("sending:" + input)
                rosrate.sleep()
            else:
                for i in range(len(input)-1):
                    pub.publish(input[i])
                    print("sending:" + input[i])
                    rosrate.sleep()
        except rospy.ROSInterruptException:
            pass
    return


def main(argv):
    global topic
    global rate
    global mutations
    global subscribed
    help = (
    'Usage: rachel.py -t <topic> -r <rate> [options...]\n'
        '-a, --random                               Random fuzzer\n'
        '-m, --mutation <seed>                      Mutation fuzzer\n'
        '-f, --mutation_file                        Mutation fuzzer using a ros subscription to topic\n'
        '-s, --size <population_size>               For mutation fuzzer, the number of mutations\n'
        '-g, --grammar <population_size>            Grammar based fuzzer imported from grammar.py\n'
        ''
        'Hint: if you want to list the available topics just mention Rachel as topic'
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
            if topic == "Rachel":
                topic = get_topics()
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
            fuzz = mutate_fuzz([seed_input], mutations)
        elif opt in ("-f", "--mutation_file"):
            for optm, argm in opts:
                if optm in ("-s", "--size"):
                    mutations = int(argm)
            type = "mutation (with file)"
        elif opt in ("-g", "--grammar"):
            population_size = int(arg)
            type = "grammar"
            fuzz = generate_fuzz(population_size)
    if type != "mutation (with file)":
        fuzzer(topic, rate, fuzz, type)
    else:
        print("================Collecting messages from "+topic+"================")
        rospy.init_node('fuzzer', anonymous=True)
        subscribed = rospy.Subscriber(topic, String, get_seed, queue_size = 1)
        rosrate = rospy.Rate(rate)
        while not rospy.is_shutdown():
            rosrate.sleep


if __name__ == '__main__':
    topic = ""
    rate = ""
    mutations = ""
    seed_candidates = []
    asked = False
    main(sys.argv[1:])
