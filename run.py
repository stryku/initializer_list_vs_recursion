#!/usr/bin/python

from subprocess import call
import time
import sys


def build_command(compiler, namespace, number_of_elements):
    return [compiler,
            '-xc++',
            '-fsyntax-only',
            '-std=c++14',
            'main.cpp',
            '-DNUMBER_OF_ELEMENTS=' + number_of_elements,
            '-DNAMESPACE=' + namespace]


def run_test(compiler, namespace, number_of_elements):
    command = build_command(compiler, namespace, number_of_elements)
    start = time.time()
    call(command)
    end = time.time()
    return end - start


def run_tests(times, compiler, namespace, number_of_elements):
    sys.stdout.flush()
    sum = 0.0
    for i in range(0, times):
        sys.stdout.write("%s, \t%s, \t%s, \t[%d%%]   \r" % (compiler, namespace, number_of_elements, (100 * i / times)))
        sys.stdout.flush()
        sum += run_test(compiler, namespace, number_of_elements)

    print(compiler + ', \t' + namespace + ', \t' + number_of_elements + ', \t' + str(sum / times))
    return str(sum / times)


def run_matrix(times, compilers, namespaces, cases):
    results = {}

    for compiler in compilers:
        for namespace in namespaces:
            results_key = "{}_{}".format(compiler, namespace)
            results[results_key] = {}
            for case in cases:
                result = run_tests(times, compiler, namespace, str(case))
                results[results_key][case] = result

    return results


TIMES_TO_RUN = 50
CLANG = 'clang++-5.0'
GXX = 'g++-6'

results = run_matrix(TIMES_TO_RUN,
                     [CLANG, GXX],
                     ['folly', 'initializer_list'],
                     range(0, 250, 10))

print('')
print('')
    
for k,v in results.items():
    print("{}, ".format(k), end='')
    for k2, v2 in v.items():
        print(" {},".format(v2), end='')

    print('')
