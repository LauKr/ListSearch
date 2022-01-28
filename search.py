import numpy as np
from multiprocessing import Pool
from multiprocessing import Process
import multiprocessing


verbose = False


def import_list(filename: str):
    """
    Imports the file <filename> using numpy.genfromtxt with dtype=str.

    :param filename: str
    :return imported_list: numpy.ndarray
    """
    # Check fileextension from last "." in the filename
    for position, character in enumerate(filename[::-1]):
        if character == '.':
            file_extension = filename[-1-position:]
            if verbose:
                print('File extension: ', file_extension)
    with open(filename) as f:
        if file_extension == '.txt':  # If it is a .txt
            imported_list = np.genfromtxt(f, dtype=str, delimiter=None)
        elif file_extension == '.csv':  # If it is a .csv
            imported_list = np.genfromtxt(f, dtype=str, delimiter=',')
        else:
            print('What type of list is it? ')
            return 1
    return imported_list


def split_lists(whole_list, partials=4):
    """
    Splits up <whole_list> into <partials> sub-lists.

    :param whole_list: numpy.ndarray
    :param partials: int
    :return lists: list
    """
    lists = np.array_split(whole_list, partials)
    if verbose:
        print(f'Original list split into {len(lists)} separate sub-lists.')
    return lists


def searching(lst, search_string):
    result = [s for s in lst if search_string in s]
    return result


def output(return_lists, search_string):
    result = []
    for i in range(len(return_lists)):
        result += return_lists[i]
    if verbose:
        print(f'The list contains following entries with {search_string}: {result}')
    return result


def run(filename, search_string, partials):
    whole_list = import_list(filename)
    partial_lists = split_lists(whole_list, partials)
    return_lists = pool_handler(partials, partial_lists, search_string)
    result = output(return_lists, search_string)
    return result


def pool_handler(n_processes=multiprocessing.cpu_count(), partial_lists=None, search_string=None):
    """
    Uses multiprocessing.Pool to establish <n_processes> processes to run the local searching() function with
    <partial_lists> and <search_string>.

    :param n_processes: int
    :param partial_lists: list
    :param search_string: str
    :return result: list
    """
    if verbose:
        print('Number of processes: ', n_processes)
    # search_string_list = [search_string] * len(partial_lists)
    list_string_pairs = []
    for i in range(len(partial_lists)):
        list_string_pairs.append((partial_lists[i], search_string))
    p = Pool(n_processes)
    result = p.starmap(searching, list_string_pairs)
    return result


if __name__ == '__main__':
    verbose = True
    N_CPUs = multiprocessing.cpu_count()
    if verbose:
        print("Number of CPU cores: ", N_CPUs)
    run('default_list.txt', 'a', N_CPUs)
