# -*- coding: utf-8 -*-
"""
@author: Priyanshu Garg
"""
# utils/date_utils.py

from datetime import datetime, timedelta

def get_next_weekday(start_date):
    """
    Returns the next weekday (Monday–Friday) from a given date.
    """
    next_day = start_date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        next_day += timedelta(days=1)
    return next_day

def get_previous_weekday(start_date):
    """
    Returns the previous weekday (Mon–Fri) before start_date.
    """
    prev_day = start_date - timedelta(days=1)
    while prev_day.weekday() >= 5:
        prev_day -= timedelta(days=1)
    return prev_day