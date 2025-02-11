import csv
import os

def time_interval_input():
    units = {'s', 'm', 'h', 'd'} # dictionary of acceptable units 

    while True:
        time = input("Enter the time interval (e.g., “4s”, '15m', '2h', '1d', '1h30m')")
        num = ""
        valid = False
        
        for char in time:
            if(char.isdigit()):
                num += char # collect the number
            elif(char in units):
                 if num == "": # only units, no number
                     break
                 valid = True # valid format
                 num = ""
            else:
                valid = False
                break

        if(valid and num == ""):
            print(f"Time interval: {time} is valid")
            return time
        else:
            print("Invalid format, please enter another interval")


def time_frame_selection():
    start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
    end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")

    # check to see if inputted time range is valid (19 characters long and start is less than end)

    if len(start_time) == 19 and len(end_time) == 19 and start_time < end_time:
        print(f"Time range selected: {start_time} to {end_time}")
        return start_time, end_time
    else:
        print("Invalid format, please enter another date")

def process_ohlcv(csv_file, interval, start_time, end_time):
    trades = []

    with open(csv_file) as file:
        reader = csv.reader(file)
        rows = list(reader)

        data_rows = rows[1:]
        for row in data_rows:
            # define, timestamp, price traded at, and how much is traded
            timestamp, price, volume = row[0], float(row[1]), float(row[2])

            if start_time.strip() <= timestamp[:19].strip() <= end_time.strip(): # see if the timestamp is in user-given range
                trades.append([timestamp, price, volume])

    if not trades:
        print("No trades found in the selected time range.")

    ohlcv_bars = []
    current_bar = {"time": trades[0][0], "open": trades[0][1], "high": trades[0][1], "low": trades[0][1], "close": trades[0][1], "volume": trades[0][2]}


    unit_multipliers = {'s': 1, 'm': 60, 'h': 3600}
    interval_value = int(''.join(filter(str.isdigit, interval)))
    interval_unit = ''.join(filter(str.isalpha, interval))

    for i in range(1, len(trades)):
        timestamp, price, volume = trades[i]

        prev_h, prev_m, prev_s = map(int, current_bar["time"][11:19].split(":"))
        curr_h, curr_m, curr_s = map(int, timestamp[11:19].split(":"))

        prev_time = prev_h * 3600 + prev_m * 60 + prev_s
        curr_time = curr_h * 3600 + curr_m * 60 + curr_s

        interval_seconds = interval_value * unit_multipliers[interval_unit]

        # if the timestamp is in the same interval, update values
        if (curr_time - prev_time) >= interval_seconds:
            current_bar["high"] = max(current_bar["high"], price)
            current_bar["low"] = min(current_bar["low"], price)
            current_bar["close"] = price
            current_bar["volume"] += volume
        else:
            ohlcv_bars.append(current_bar)  # append the bar to our overall list of candlesticks
            current_bar = {"time": timestamp, "open": price, "high": price, "low": price, "close": price, "volume": volume}

    ohlcv_bars.append(current_bar)  # save last bar
    return ohlcv_bars

interval = time_interval_input()
start_time, end_time = time_frame_selection()


output_dir = "/Users/sathviknookala/Desktop/sw-challenge-spring-2025/cleaned_data"
os.makedirs(output_dir, exist_ok = True)

output_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]

output_files = sorted(
    [f for f in os.listdir(output_dir) if f.endswith('.csv')],
    key=lambda x: int(x.split("_")[3])
)
output_file = "/Users/sathviknookala/Desktop/sw-challenge-spring-2025/cleaned_data/cleaned_ctg_tick_20240916_0001_a016010f.csv"
ohlcv_result = process_ohlcv(output_file, interval, start_time, end_time)

for bar in ohlcv_result:
    print(bar)
