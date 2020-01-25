import os
import pandas as pd
from tqdm import tqdm
from parser import HocrParser

DOCUMENTS_PATH = "./contest/test/reports/"
TRUE_VALUES_PATH = "./contest/test/ground_truth-test.csv"

files_dict = {}
release_date_dict = {}
period_from_dict = {}
period_to_dict = {}
address_info_dict = {}


ids_folders = os.listdir(DOCUMENTS_PATH)
ids_folders = [d for d in ids_folders if os.path.isdir(os.path.join(DOCUMENTS_PATH,d))]
for id_folder in tqdm(ids_folders):
    id_folder_path = os.path.join(DOCUMENTS_PATH, id_folder)
    files = os.listdir(id_folder_path)
    hocr_file = [f for f in files if os.path.isfile(os.path.join(id_folder_path, f)) and f.endswith(".hocr")]
    try:
        hocr_file = hocr_file.pop()
        files_dict[id_folder] = hocr_file

        # Parse file
        parser = HocrParser()
        parser.read_file(os.path.join(id_folder_path, hocr_file))
        document = parser.parse_()        
        
        # Add release date to dict
        release_date = parser.get_release_date()
        release_date_dict[id_folder] = release_date
        
        # Add dates to dict
        dates = parser.get_dates()
        period_from_dict[id_folder] = dates[0]
        period_to_dict[id_folder] = dates[1]

        # Add address data to dicts
        address_info_dict[id_folder] = parser.get_company_address_info()
    
    except Exception as e:
        continue
        
        
# Tests
def print_acc(df, orig_col_name, extracted_col_name, print_name):
    acc = (df.loc[:, orig_col_name] == df.loc[:, extracted_col_name]).sum() / df.shape[0]
    print("%s accuracy: %1.2f" % (print_name, acc))


def create_subdf(data_dict, colnames):
    if isinstance(colnames, str):
        colnames = [colnames]
    df = pd.DataFrame.from_dict(data_dict, orient="index", columns=colnames).reset_index()
    df["index"] = df.loc[:, "index"].astype("int64")
    return df


# Reading the reference data
reference_data = pd.read_csv(TRUE_VALUES_PATH, sep =';')


# Creating the sub-dataframes
release_date_df = create_subdf(release_date_dict, ["drawing_date_extracted"])
period_from_df = create_subdf(period_from_dict, ["period_from_extracted"])
period_to_df = create_subdf(period_to_dict, ["period_to_extracted"])
address_info_df = create_subdf(address_info_dict, [cn + "_extracted" for cn in ("postal_code", "city", "street", "street_no")])


# Merging the sub-dataframes to the reference data
reference_data = pd.merge(reference_data, release_date_df, left_on='id', right_on='index', how='left')
reference_data = pd.merge(reference_data, period_from_df, left_on='id', right_on='index', how='left')
reference_data = pd.merge(reference_data, period_to_df, left_on='id', right_on='index', how='left')
reference_data = pd.merge(reference_data, address_info_df, left_on='id', right_on='index', how='left')


# Printing accuracy
print_acc(reference_data, 'drawing_date', 'drawing_date_extracted', 'Drawing date')
print_acc(reference_data, 'period_from', 'period_from_extracted', 'Period from')
print_acc(reference_data, 'period_to', 'period_to_extracted', 'Period to')
print_acc(reference_data, 'postal_code', 'postal_code_extracted', 'Postal code')
print_acc(reference_data, 'city', 'city_extracted', 'City')
print_acc(reference_data, 'street', 'street_extracted', 'Street')
print_acc(reference_data, 'street_no', 'street_no_extracted', 'Street no.')
