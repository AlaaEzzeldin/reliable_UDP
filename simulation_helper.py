import random
import os

list_of_must_dropped_seq_numbers = []


def get_must_dropped_packets(file_name, probability, size_of_packet, seed_value):
    random.seed(seed_value)
    size_of_file = os.path.getsize(file_name)
    print("size of file= ", size_of_file)
    number_of_chunks = int(size_of_file / size_of_packet)
    print("number_of_chunks", number_of_chunks)
    number_of_must_dropped = int(number_of_chunks * probability)
    print("number_of_must_dropped", number_of_must_dropped)
    print("random", random.randint(seed_value, number_of_must_dropped))
    for i in range(number_of_must_dropped):
        list_of_must_dropped_seq_numbers.append(random.randint(0, number_of_chunks))
    return list_of_must_dropped_seq_numbers


def get_decision(list_of_must_dropped_seq_numbers, seq_number):
    if list_of_must_dropped_seq_numbers.__contains__(seq_number):
        return False  # drop it
    else:
        return True  # don't drop it


def print_dropped_seq(list_of_must_dropped_seq_numbers):
    for i in range(len(list_of_must_dropped_seq_numbers)):
        print(list_of_must_dropped_seq_numbers[i])

