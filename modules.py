"""
Functions to be imported into the ghost-names app to immitate db
"""

import csv
import random


def convert_to_dict(filename):
    """
    Convert a CSV file to a list of Python dictionaries
    """

    # Open a CSV file - note - must have column headings in top row
    datafile = open(filename, encoding="utf8", newline="")

    # Read and process data
    my_reader = csv.DictReader(datafile)
    list_of_dicts = list(my_reader)
    datafile.close()

    return list_of_dicts


def reserve_names(dict_list):
    """
    Dummy data generation //POST
    Mutates dict_list reserving some random names
    use get_taken_free_names(dict_list) to get updated names

    """

    dummy_data = [
        ("Fred", "Again", "fred@phntms.com"),
        ("Sufjan", "Stevens", "sufjan@phntms.com"),
        ("Peggy", "Gou", "peggy@phntms.com"),
        ("Charli", "xcx", "charli@phntms.com"),
        ("Kendrick", "Lamar", "kendrick@phntms.com"),
    ]

    # Take k random names without replacement
    taken_ghost_names = random.sample(dict_list, k=len(dummy_data))

    # Mutating passed dict_list to reserve names
    for d, (first, family, email) in zip(taken_ghost_names, dummy_data):
        d["First name"] = first
        d["Family name"] = family
        d["Email"] = email
        d["Taken"] = True

    return


def get_free_names(dict_list):
    """
    Return free names
    """
    # Splitting up into two lists to help display taken names on top of the list
    free = [d for d in dict_list if d.get("Taken") is not True]

    return free


def get_taken_names(dict_list):
    """
    Return taken names
    """
    taken = [d for d in dict_list if d.get("Taken") is True]

    return taken


def set_new_ghost_name(dict_list, info):
    """
    Set a new ghost name in dict_list
    info should be a tuple containing (first, ghost, family, email) vars
    """

    first, ghost, family, email = info

    # Find the entry to update, if exists
    entry = next(d for d in dict_list if "Ghost name" in d and d["Ghost name"] == ghost)

    # Update the entry with user details, set to taken
    entry["First name"] = first
    entry["Family name"] = family
    entry["Email"] = email
    entry["Taken"] = True
    return


def clear_old_ghost_name(dict_list, email):
    """
    Update entry to remove old user data and free up ghost name
    """

    # Find entry to update, if exists
    entry = next((d for d in dict_list if "Email" in d and d["Email"] == email), None)

    # If the entry was found and the entry is taken, clear old user data and free up the ghost name
    if entry and entry["Taken"] is True:
        entry["First name"] = ""
        entry["Family name"] = ""
        entry["Email"] = ""
        entry["Taken"] = False
    return
