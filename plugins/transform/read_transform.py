import pandas as pd
import glob
import os

# To declare home directory
HOME = os.path.expanduser("~")

def append_all_files(extension, directory):
    """
    The goal of this function is to join and concatenate all of the files.

    Args:
        extension (str): the extension of the file that we want to append
        directory (str): the path of the directory containing the files

    Return:
        a dataframe with the concatenated content of all the files
    """

    # to read all file object in data directory
    all_filesnames = [f for f in glob.glob(f"{directory}/*.{extension}")]

    #  to append all files in one dataframe
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filesnames], ignore_index=True)

    # to clean not valid Quantity Ordered column
    combined_csv.drop(combined_csv[combined_csv["Quantity Ordered"] == "Quantity Ordered"].index, inplace=True)

    return combined_csv
    
# data transformation, group by is filled with product or month
def run_transform(extension="csv", directory="automate_report/data/sales_product_data", group_by='product'):
    """
    The goal of this function is to make a report based (groupby) on a given column

    Args:
        extension (str): the extension of the file that we want to append
        directory (str): the path of the directory containing the files
        group_by (str): the groupby criteria for our report

    Return:
        a dataframe with the report
    """
    data = append_all_files(extension, directory)

    # group by product and summarize by quantity * price
    data["total_price"] = data["Quantity Ordered"].astype(float) * data["Price Each"].astype(float)

    data["Order Date"] = pd.to_datetime(data["Order Date"])

    # drop nulls
    data.drop(data[data["Order Date"].isna()].index, inplace=True)

    if group_by.lower().strip() == "product":
        # group by product
        data_transformed = data.groupby("Product").agg({"total_price": "sum"}).reset_index()
    elif group_by.lower().strip() == "month":
        # group by month
        data_transformed = data.groupby(pd.Grouper(key='Order Date', freq='M')).agg({"total_price": "sum"}).reset_index()

    print(data_transformed)

    return data_transformed

if __name__ == '__main__':
    run_transform()

