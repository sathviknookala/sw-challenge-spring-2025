import csv 
import os
from statistical_test import compute_global_threshold
from sw_challenge_data_interface import process_ohlcv

#counter variables for each faulty row
faulty_time_count = 0
faulty_negative_count = 0
faulty_missing_count = 0
faulty_outlier_count = 0

# path for original data and cleaned data
csv_dir = "/Users/sathviknookala/Desktop/sw-challenge-spring-2025/data"
output_dir = "/Users/sathviknookala/Desktop/sw-challenge-spring-2025/cleaned_data"


os.makedirs(output_dir, exist_ok = True)

csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

csv_files = sorted(
    [f for f in os.listdir(csv_dir) if f.endswith('.csv')],
    key=lambda x: int(x.split("_")[3])
)

# individual file data cleaning
for file in csv_files:

    file_path = os.path.join(csv_dir, file) # original file path 
    cleaned_file_path = os.path.join(output_dir, f"cleaned_{file}") # cleaned file path

    cleaned_rows = []

    with open(file_path) as file:
        
        reader = csv.reader(file)
        rows = list(reader)   

        header = rows[0]
        data_rows = rows[1:] 
       
        for row in data_rows:
            clean_check = True # check variable for each individual row            
                
            ''' negative price check '''
            try:
                price = float(row[1])
                if(price < 0): # if trade happens at negative price, remove
                    clean_check = False
                    faulty_negative_count +=1 
            except ValueError:
                clean_check = False

            ''' outlier check '''
            try:
                if(price < 400.0): # if trade is priced beyond range, remove
                    clean_check = False
                    faulty_outlier_count += 1
            except ValueError:
                clean_check = False

            ''' no listed price check '''
            if(row[1] == "" or row[1] is None or row[1] == "NaN"): # if trade has no listed price, remove
                clean_check = False
                faulty_missing_count += 1
                
            ''' timestamp check '''
            timestamp = row[0].strip()
            
            hour = int(timestamp[11:13])
            minute = int(timestamp[14:16])

            if(hour < 9 or (hour == 9 and minute < 30) or hour >= 16): # if trade happens outside of market hours, remove
                clean_check = False
                faulty_time_count += 1

            ''' final check '''
            if clean_check: # if clean_check is still True, add the row to the clean file
                cleaned_rows.append(row)
            else:
                continue # if clean_check is False, move onto the next row
    
    # after cleaning all rows, write to new file
    if cleaned_rows:
        with open(cleaned_file_path, "w", newline ="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(header)
            writer.writerows(cleaned_rows)

    
print(f"Summary:")
print(f"Negative prices removed: {faulty_negative_count}")
print(f"Timestamps outside market hours removed: {faulty_time_count}")
print(f"Missing prices removed: {faulty_missing_count}")
print(f"Outliers removed: {faulty_outlier_count}")



        



