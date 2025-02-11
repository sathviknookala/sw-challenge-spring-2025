import csv
import os

def compute_global_threshold(csv_dir):
    prices = []

    # read all CSV files in the directory
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

    for file in csv_files:
        file_path = os.path.join(csv_dir, file)
        
        with open(file_path) as f:
            reader = csv.reader(f)
            next(reader) 

            for row in reader:
                try:
                    price = float(row[1])  # convert price to float
                    if price >= 0:
                        prices.append(price)
                except ValueError:
                    continue  # skip invalid prices

    # Compute median price
    sorted_prices = sorted(prices)
    mid = len(sorted_prices) // 2
    median_price = (sorted_prices[mid] if len(sorted_prices) % 2 != 0 
                    else (sorted_prices[mid - 1] + sorted_prices[mid]) / 2)

    # compute absolute deviations from median
    deviations = [abs(price - median_price) for price in sorted_prices]

    # compute Median Absolute Deviation (MAD)
    sorted_deviations = sorted(deviations)
    mid_dev = len(sorted_deviations) // 2
    median_deviation = (sorted_deviations[mid_dev] if len(sorted_deviations) % 2 != 0
                        else (sorted_deviations[mid_dev - 1] + sorted_deviations[mid_dev]) / 2)

    # define global minimum threshold (3 * MAD below median)
    global_min_threshold = median_price - 3 * median_deviation

    return global_min_threshold

