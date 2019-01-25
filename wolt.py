"""
Wolt Coding Task 2019 - "Pickup times"
Median pickup time for each restaurant between certain hours and date.
"""

import statistics
import datetime
import collections


def write_to_file(data):
    """Get median time for pickup for specific restaurant."""
    # location_id,median_pickup_time
    # 1,21
    # 2,15
    # 3,6
    # etc.

    # sort data with location id
    data = collections.OrderedDict(sorted(data.items()))
    # to calculate how many rows are written so we can inform user
    rows_written = 0
    with open("results.csv", 'w') as outfile:
        # write titles to file
        outfile.write("location_id,median_pickup_time\n")
        for location, time_array in data.items():
            outfile.write("{},{}\n".format(location, statistics.median(time_array)))
            rows_written += 1
    return rows_written


def parse_data(city, wanted_date, wanted_time, file_name):
    """Calculate median for specific restaurant.
        return: median for restaurant
    """
    with open(file_name, 'r') as file:
        # data dictionary has id as key, array of pickup_times as a values
        # {1: [10,32,12,4], 2:[10],...}
        data = {}
        # skip the first line since it contains column titles
        next(file)
        for line in file:
            val = line.split(",")
            time = val[1]     # iso_8601_timestamp
            if is_timeframe_correct(time, wanted_date, wanted_time):
                place = int(val[0])
                pickup_time = int(val[2])
                # find out if id key is already in dictionary
                if place in data:
                    arr = data[place]
                    arr.append(pickup_time)
                    data[place] = arr
                else:
                    data[place] = [pickup_time]

    return data


def is_timeframe_correct(time, wanted_date, wanted_hours):
    """Is requested time in the time frame. Time between the wanted_hours and wanted_date?
        :param: time from pickup_times, wanted_date & hour is the date and hour where we want data
        :return boolean value
    """
    # time format : 2019-01-13T19:32:53Z
    # wanted_date format : 07-01-19
    # wanted_hours format : 19-20
    wanted_date = datetime.datetime.strptime(wanted_date, "%d-%m-%y").strftime("%Y-%m-%d")  # %Y-%m-%d
    wanted_date = datetime.datetime.strptime(wanted_date, "%Y-%m-%d").date()    # converting to date object

    start_hour = int(wanted_hours.split("-")[0])
    end_hour = int(wanted_hours.split("-")[1])

    # get the hour part of time
    hour = int(time.split("T")[1].split(":")[0])

    time_date = time.split("T")[0]
    time_date = datetime.datetime.strptime(time_date, "%Y-%m-%d").date()    # converting to date object

    if time_date == wanted_date:
        if start_hour <= hour <= end_hour:
            # time and date match
            return True
        else:
            return False
    else:
        return False


def create_title():
    print("********************************************************************************")
    print("*                                  WOLT                                        *")
    print("*                        pickup time calculator                                *")
    print("********************************************************************************")


def show_help():
    print("********************************************************************************")
    print("*                               HOW TO USE                                     *")
    print("********************************************************************************")
    print("*                               DESCRIPTION                                    *")
    print("********************************************************************************")
    print("*                                                                              *")
    print("*This software calculates median pickup time for each restaurant between given *")
    print("*conditions. These conditions are city, date and time frame.                   *")
    print("*                                                                              *")
    print("********************************************************************************")
    print("*                                  USAGE                                       *")
    print("********************************************************************************")
    print("*                                                                              *")
    print("*  [CITY], [DATE dd-mm-yyy], [start hour-end hour], [FILENAME]                 *")
    print("*                                                                              *")
    print("*  [FILENAME] has location_id,iso_8601_timestamp,pickup_time in csv format     *")
    print("*                                                                              *")
    print("*  example:                                                                    *")
    print("*  Helsinki, 07-01-19, 10-11, pickup_times.csv                                 *")
    print("*                                                                              *")
    print("*  Note: currently this works only in Helsinki.                                *")
    print("********************************************************************************")


def command_not_valid():
    print("*     Command you typed is not valid. Type 'help' for instructions.            *\n")


def main():
    """UI loop."""

    running = True
    create_title()
    while running:
        print(">> Type 'help' for instructions.                                                  ")
        print(">> Type 'exit' to exit.                                                           ")
        command = input(">> ")
        try:
            if command == "exit":
                running = False
            elif command == "help":
                show_help()
            elif len(command.split(",")) == 4:
                # test command: "Helsinki", "07-01-19", "10-11", "pickup_times.csv"help
                cmd_string = command.split(",")
                # stripping excess spaces and making new list
                cmd_string = [cmd.strip() for cmd in cmd_string]
                if cmd_string[0].lower() == "helsinki":
                    data = parse_data(cmd_string[0], cmd_string[1], cmd_string[2], cmd_string[3])
                    rows = write_to_file(data)
                    if rows == 0:
                        print("Your query didn't got any matches. Please make a new query.\n")
                    else:
                        print("Command successfully completed. Requested data is written to results.csv")
                        print("{} rows of data added.\n".format(rows))
                else:
                    print("Works only in Helsinki. Try again.")

            else:
                command_not_valid()
        except AttributeError or ValueError:
            command_not_valid()
        except FileNotFoundError:
            print("File does not exist. Try again with correct filename.\n")


main()