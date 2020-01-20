import os
import pandas as pd
from parser import HocrParser

DOCUMENTS_PATH = "./contest/test/reports/"
TRUE_VALUES_PATH = "./contest/test/ground_truth-test.csv"

files_dict = {}
release_date_dict = {}
period_from_dict = {}
period_to_dict = {}

ids_folders = os.listdir(DOCUMENTS_PATH)
ids_folders = [d for d in ids_folders if os.path.isdir(os.path.join(DOCUMENTS_PATH,d))]
for id_folder in ids_folders:
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
    
    except Exception as e:
        continue
        
        
# Tests
release_date_df = pd.DataFrame.from_dict(release_date_dict, orient='index', columns=['drawing_date_extracted']).reset_index()
release_date_df['index'] = release_date_df['index'].astype('int64')

period_from_df = pd.DataFrame.from_dict(period_from_dict, orient='index', columns=['period_from_extracted']).reset_index()
period_from_df['index'] = period_from_df['index'].astype('int64')

period_to_df = pd.DataFrame.from_dict(period_to_dict, orient='index', columns=['period_to_extracted']).reset_index()
period_to_df['index'] = period_to_df['index'].astype('int64')

true_dates = pd.read_csv(TRUE_VALUES_PATH, sep =';')

true_dates = pd.merge(true_dates, release_date_df, left_on='id', right_on='index', how='left')
true_dates = pd.merge(true_dates, period_from_df, left_on='id', right_on='index', how='left')
true_dates = pd.merge(true_dates, period_to_df, left_on='id', right_on='index', how='left')

drawing_date_accuracy = sum(true_dates['drawing_date'] == true_dates['drawing_date_extracted'])/true_dates.shape[0]
period_from_accuracy = sum(true_dates['period_from'] == true_dates['period_from_extracted'])/true_dates.shape[0]
period_to_accuracy = sum(true_dates['period_to'] == true_dates['period_to_extracted'])/true_dates.shape[0]

print(str.format("Drawing date accuracy: " + "%1.2f" % drawing_date_accuracy), end="\n")
print(str.format("Period from accuracy: " + "%1.2f" % period_from_accuracy), end="\n")
print(str.format("Period to accuracy: " + "%1.2f" % period_to_accuracy), end="\n")