import cProfile
import tracemalloc

import numpy as np

from utils import BSTNode, plot_time_results, print_table, plot_memory_results
from utils import to_timedelta as t


def insert_array(bst, arr):
    for num in arr:
        bst.insert(num)


def search_array(bst, arr):
    for num in arr:
        bst.exists(num)


def delete_array(bst, arr):
    for num in arr:
        bst.delete(num)


if __name__ == '__main__':
    array_sizes = [10**x for x in range(2, 7)]
    results = {arr_size: {'insert': 0, 'search': 0, 'delete': 0, 'memory': 0} for arr_size in array_sizes}

    tests = {'insert': insert_array,
             'search': search_array,
             'delete': delete_array}

    # TIME COMPLEXITY
    print('Inserting/searching/deleting of 20 random integers (in same range of generated BST) ...')
    for arr_size in array_sizes:
        new_bst = BSTNode()
        array = np.random.randint(low=1, high=arr_size, size=arr_size)
        insert_array(new_bst, array)

        for test_name, test_func in tests.items():
            total_times = []
            for i in range(110):
                numbers_for_test = np.random.randint(low=1, high=arr_size, size=20)

                with cProfile.Profile() as pr:
                    # profiling execution only inside context manager
                    test_func(new_bst, numbers_for_test)

                total_time = 0
                for stat in pr.getstats():
                    total_time += stat.totaltime
                total_times.append(total_time)

            total_times.sort()
            total_time_avg = sum(total_times[5:-5]) / 100  # remove two smallest and biggest values
            results[arr_size][test_name] += total_time_avg

    print_table(['BST size', 'Insert', 'Search', 'Delete'],
                [[size,
                  t(values['insert']),
                  t(values['search']),
                  t(values['delete'])] for size, values in results.items()],
                'rccc')
    plot_time_results(results, 'bst_time.png')

    # SPACE COMPLEXITY
    print('\n\nCalculating allocated memory ...')
    for arr_size in array_sizes:
        new_bst = BSTNode()
        array = np.random.randint(low=1, high=arr_size, size=arr_size)

        tracemalloc.clear_traces()
        tracemalloc.start()

        insert_array(new_bst, array)

        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot.statistics('lineno')
        total_size = 0
        for stat in top_stats[:10]:
            total_size += stat.size

        results[arr_size]['memory'] += total_size

    print_table(['BST size', 'Memory used (MB)'],
                [[size,
                 round(values['memory'] / 1048576, 4)] for size, values in results.items()],
                'rr')
    plot_memory_results(results, 'bst_memory.png')
