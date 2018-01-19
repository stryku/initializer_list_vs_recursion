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
		sys.stdout.write("%s, \t%s, \t%s, \t[%d%%]   \r" % (compiler, namespace, number_of_elements, (100*i/times)))
		sys.stdout.flush()
		sum += run_test(compiler, namespace, number_of_elements)
	
	print(compiler + ', \t' + namespace + ', \t' + number_of_elements + ', \t' + str(sum / times))


def run_matrix(times, compilers, namespaces, cases):
	for compiler in compilers:
		for namespace in namespaces:
			for case in cases:
				run_tests(times, compiler, namespace, str(case))


TIMES_TO_RUN=500
CLANG='clang++-5.0'
GXX='g++-6'

run_matrix(TIMES_TO_RUN,
		   [CLANG, GXX],
		   ['folly', 'initializer_list'],
		   [0, 700])

