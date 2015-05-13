#!/usr/bin/python

"""
    Author          Paula Dwan
    Email           paula.dwan@gmail.com
    Student ID      13208660

    Module          COMP47270 (Computational Network Analysis and Modeling)
    Course          MSc ASE
    Due date        11-May-2015
    Lecturer 	    Dr. Neil Hurley

    CASE STUDY 2 :  Community Finding

"""

import timeit
import logging

src_file = "../DataSets/test.txt"
edges_original = 0
edges_current = 0
cs_ref = 'CS 2 : Computations : '


def init():
    print "initializing ..."


def get_start_time():
    """
    get_start_time()
    Calculate run-time --> start-time
    :return: current system time, start_time
    """
    return timeit.default_timer()


def show_time_taken(start):
    """
    show_time_taken(start)
    Calculate run-time --> end-time - start-time (already calculated)
    :param start: starting time
    :return: time_taken - string summary containing time taken to complete
    """
    logging.info(cs_ref, 'calculate Time Taken to run partitioning')
    time_end = timeit.default_timer()
    time_taken = '\tTime taken to run = {0} - {1} = {2} usec'.format(time_end*1000000, start*1000000, (time_end - start)*1000000)
    return time_taken
