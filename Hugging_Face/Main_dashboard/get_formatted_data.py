import pandas as pd
import numpy as np



try:
    original_df = pd.read_csv("hf://datasets/aengusbl/getaround-data/getaround_data.csv")
except Exception as e:
    print("There was an issue when attempting to retrieve the dataset from Hugging Face. Falling back to an S3 bucket.")
    original_df = pd.read_excel("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx")
    original_df["has_previous_rental"] = ~original_df.time_delta_with_previous_rental_in_minutes.isna()

convert_dict = {"delay_at_checkout_in_minutes": "Int64",
                "previous_ended_rental_id": "Int64",
                "time_delta_with_previous_rental_in_minutes": "Int64"}
delays_df = original_df.copy().astype(convert_dict)

# Some of the NaNs actually make sense, so we don't want them all gone. We want the ones that mean "no delay" to be zeros, however.
def replace_delay_nas(row):
    if pd.isna(row["delay_at_checkout_in_minutes"]) \
       and (row.state == "ended") \
       and (row.has_previous_rental == True):
        return 0
    else:
        return row["delay_at_checkout_in_minutes"]

delays_df["delay_at_checkout_in_minutes"] = delays_df.apply(replace_delay_nas, axis=1)



get_series_no_na = lambda col: col[~col.isna()]
delays_series = get_series_no_na(delays_df.delay_at_checkout_in_minutes)
delta_series = get_series_no_na(delays_df.time_delta_with_previous_rental_in_minutes)
delays_before_relevant_cancelled_rentals_list = []

ids_and_delays_dict = {row.rental_id: row.delay_at_checkout_in_minutes for row in delays_df.itertuples() if row.state == "ended"}
# We want to cross-reference late checkouts with cancelled rentals, but only if the delay is more than the delta between each pair of rentals
for row in delays_df.itertuples():
    if (row.state == "canceled") and (row.has_previous_rental == True):
        time_delta_previous_rental = row.time_delta_with_previous_rental_in_minutes
        previous_rental_delay = ids_and_delays_dict[row.previous_ended_rental_id]
        if pd.isna(previous_rental_delay) or pd.isna(time_delta_previous_rental):
            continue # I found that these two columns are always NaN together in the data, but it doesn't work if I don't do this
        if previous_rental_delay > time_delta_previous_rental: #type: ignore
            delays_before_relevant_cancelled_rentals_list.append(previous_rental_delay)
delays_before_relevant_rentals_series = pd.Series(delays_before_relevant_cancelled_rentals_list)

affected_rentals_dict = {"percentage_of_even_later_returns": [],
                         "percentage_of_potentially_affected_rentals": [],
                         "percentage_rentals_cancelled_bc_late": []}
for delay in range(max(delays_series.to_list())):
    percentage_of_even_later_returns = (len(delays_series[delays_series > delay]) / len(delays_series)) * 100
    affected_rentals_dict["percentage_of_even_later_returns"].append(percentage_of_even_later_returns)

    percentage_of_potentially_affected_rentals = (len(delta_series[delta_series < delay]) / len(delta_series)) * 100
    affected_rentals_dict["percentage_of_potentially_affected_rentals"].append(percentage_of_potentially_affected_rentals)

    dbrrs = delays_before_relevant_rentals_series
    percentage_rentals_cancelled_bc_late = (len(dbrrs[dbrrs <= delay]) / len(dbrrs)) * 100
    affected_rentals_dict["percentage_rentals_cancelled_bc_late"].append(percentage_rentals_cancelled_bc_late)
affected_rentals_df = pd.DataFrame(affected_rentals_dict)

def get_affected_rentals_df():
    return affected_rentals_df



# We're only interested in late returns
late_returns_df = delays_df[delays_df.delay_at_checkout_in_minutes.notna() & (delays_df.delay_at_checkout_in_minutes >= 0)]

col = "delay_at_checkout_in_minutes"
mean = late_returns_df[col].mean()
std = late_returns_df[col].std()
late_returns_df_fewer_outliers = late_returns_df[(np.abs(late_returns_df[col] - mean) <= std)] # Not a normal distribution: 1 std is about 20 hours, which is plenty
has_previous_rental_df = delays_df[delays_df.has_previous_rental == True]
has_previous_rental_df_fewer_outliers = has_previous_rental_df[(np.abs(has_previous_rental_df[col] - mean) <= std)]

values_to_optimise_dict_fewer_outliers = {"buffer_value": [], "percentage_helped_late_returns": [], "dummy_income_loss": [], "percentage_hindered_rentals": []}

late_returns_df_len = len(late_returns_df_fewer_outliers)
has_previous_rental_df_len = len(has_previous_rental_df_fewer_outliers)

max_late_return_value_fewer_outliers = int(max(late_returns_df_fewer_outliers.delay_at_checkout_in_minutes.to_list()))

for b in range(max_late_return_value_fewer_outliers):

    values_to_optimise_dict_fewer_outliers["buffer_value"].append(b)
    
    if b == 0: # b is only zero once, but doing it this way is easier to read, and the loop is already checking other values several times
        values_to_optimise_dict_fewer_outliers["percentage_helped_late_returns"].append(0)
        values_to_optimise_dict_fewer_outliers["dummy_income_loss"].append(0)
    else:
        num_helped_late_returns = len(late_returns_df_fewer_outliers[late_returns_df_fewer_outliers.delay_at_checkout_in_minutes <= b])
        values_to_optimise_dict_fewer_outliers["percentage_helped_late_returns"].append((num_helped_late_returns / late_returns_df_len) * 100)

        dummy_income_loss = (b / max_late_return_value_fewer_outliers) * 100
        values_to_optimise_dict_fewer_outliers["dummy_income_loss"].append(dummy_income_loss)

    num_hindered_rentals = len(has_previous_rental_df_fewer_outliers[has_previous_rental_df_fewer_outliers.time_delta_with_previous_rental_in_minutes > b])
    values_to_optimise_dict_fewer_outliers["percentage_hindered_rentals"].append((num_hindered_rentals / has_previous_rental_df_len) * 100)


optimal_buffer_df = pd.DataFrame(values_to_optimise_dict_fewer_outliers)


def get_optimal_buffer_df():
    return optimal_buffer_df



for index, value in enumerate(values_to_optimise_dict_fewer_outliers["percentage_hindered_rentals"]):
        if value == 0:
            plot_width = index + 100
            break

def get_plot_width():
    return plot_width



if __name__ == "__main__":
    print("This script is meant to be imported, not run directly. Look for a file called \"app.py\" and run that one instead :)")