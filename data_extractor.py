import pandas as pd
from math import floor, ceil
from statistics import median

import json

HISTORICAL_DATA_CSV="CSCO.csv"

"""
Function that maps the passed percentage to the nearest value in "buckets". Values in "buckets" are generated
from the floored and ceiled values of the passed percentage. The closest "bucket" value is the value that is closest
to the passed the percentage.

@param percentage:      The percentage if difference of the stock between the current week and the previous week
@param bucket_count:    The number of "buckets" you want to test to see how close the percentage fits to.
"""
def fit(percentage, bucket_count=5):
    floored = floor(percentage)
    ceiled = ceil(percentage)
    buckets = [  round(floored + ((ceiled - floored) / bucket_count) * num, 1) for num in range(1, bucket_count+1) ]
    closest_bucket = min(buckets, key=lambda b: abs(b - percentage))
    return closest_bucket


"""
Function to generate the related statistics value such as median and mean of the passed list of
percentages and corresponding occurrance of that percentage. This is basically used to get the
expected value in percentage of how much a stock would move up or down given a week.

*Note: This does not calculate the probability of the stock moving up or down. This only calculates
       how much a stock price is expected to change if it goes up or down.

@param percentage_counts:   The list of percentages and corresponding occurrances of that count
@param top_sample_size:     The top # of samples to choose from for the mean calculation
"""
def get_stats(percentage_counts, top_sample_size):
    pos_count = 0
    neg_count = 0
    up_count = 0
    down_count = 0

    up_list = []
    down_list = []

    for val in percentage_counts:
        bucket, count = val
        if bucket > 0:
            up_list += [bucket for i in range(count)]
            if pos_count < top_sample_size:
                up_count += count
                pos_count += 1
        else:
            down_list += [bucket for i in range(count)]
            if neg_count < top_sample_size:
                down_count += count
                neg_count += 1

    stats = {
        "# of top samples used:": top_sample_size,
        "up_mean": sum(up_list[:up_count]) / up_count,
        "down_mean": sum(down_list[:down_count]) / down_count,
        "up_median": median(up_list),
        "down_median": median(down_list),
    }
    return stats


def run(df):
    fitted_percentage_counts = {}
    prev_price = df["Close"][0]
    
    for date, closing_price in zip(df["Date"][1:-1], df["Close"][1:-1]):
        price_diff = closing_price - prev_price
        percent_diff = (closing_price - prev_price) / prev_price * 100
        prev_price = closing_price

        print (*["Prev price: {}".format(prev_price),
                "Price diff: {}".format(price_diff),
                "Closing price: {}".format(closing_price),
                "Percent diff: {}".format(percent_diff),
                "floored: {}, ceiled: {}".format(floor(percent_diff), ceil(percent_diff)),
                "----------------------------"
                ], sep='\n')

        bucket = fit(percent_diff)
        if bucket in fitted_percentage_counts:
            fitted_percentage_counts[bucket] += 1
        else:
            fitted_percentage_counts[bucket] = 1
        

    sorted_percentage_counts = sorted(fitted_percentage_counts.items(), key=lambda x: x[1], reverse=True)
    #print(*sorted_percentage_counts, sep='\n')

    
    stats = get_stats(sorted_percentage_counts, 10)
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    df = pd.read_csv(HISTORICAL_DATA_CSV)
    run(df)
