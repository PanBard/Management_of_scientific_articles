import os
import json
from models import Isotherm
import pandas as pd

class JSONManager:

    def __init__(self, working_folders):
        self.directory_manager = working_folders
        self.get_data_from_json_file_all()
        

    def add_article_name_to_each_csv_files(self):
        features_folder_path = self.directory_manager.input_sample_features_path
        features_files_names =  self.directory_manager.get_files_inside_folder(features_folder_path)
        all_data = pd.DataFrame()
        
        for file_name in features_files_names:
            csv_path = os.path.join(features_folder_path, file_name)
            data_name = file_name.replace('.csv', '').replace('_features','')
            df = pd.read_csv(csv_path)  # Load CSV file into a DataFrame
            df.insert(0, 'Article_name', data_name)
            all_data = pd.concat([all_data, df], ignore_index=True)

        # all_data.to_csv('all_features.csv', index=False) # saving
        return all_data
        
    def get_data_from_json_file_all(self):
        csv_data = self.add_article_name_to_each_csv_files()
        csv_data = csv_data.astype({'Sample_name':str})
        temp_tar_folder_path = self.directory_manager.temp_tar_files_path
        folders_with_json_from_tar =  self.directory_manager.get_files_inside_folder(temp_tar_folder_path)
        list_of_isotherms =[]

        for json_folder_name in folders_with_json_from_tar:
            json_file_path = os.path.join(temp_tar_folder_path, json_folder_name, self.directory_manager.json_inside_tar_name)
            article_file_name = json_folder_name.split('_')[0] 
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            min_x = data['axesColl'][0]['calibrationPoints'][0]['dx']
            max_x = data['axesColl'][0]['calibrationPoints'][1]['dx']
            min_y = data['axesColl'][0]['calibrationPoints'][2]['dy']
            max_y = data['axesColl'][0]['calibrationPoints'][3]['dy']

            for isotherm in data['datasetColl']:
                new_isotherm = Isotherm()
                x_data = []
                y_data = []
                for d in isotherm['data']:
                    x_data.append(d['value'][0])
                    y_data.append(d['value'][1])
                new_isotherm.sample_name = str(isotherm['name'])

                new_isotherm.max_x = max_x
                new_isotherm.min_x = min_x
                new_isotherm.max_y = max_y
                new_isotherm.min_y = min_y

                new_isotherm.x_axis_data = x_data.sort()
                new_isotherm.y_axis_data = y_data.sort()

                list_of_isotherms.append(new_isotherm)
                
                
                #Insert new data where Sample_name is 
                csv_data.loc[(csv_data['Sample_name'] == new_isotherm.sample_name) & (csv_data['Article_name'] == article_file_name), 'isotherm_X'] = str(x_data)
                csv_data.loc[(csv_data['Sample_name'] == new_isotherm.sample_name) & (csv_data['Article_name'] == article_file_name), 'isotherm_Y'] = str(y_data)
                #Get indexes of rows where 'Sample_name' is NaN or None


        # blank_indexes_x = csv_data['Article_name'][csv_data['isotherm_X'].isna()].tolist()
        # print(blank_indexes_x)
        # blank_indexes_y = csv_data['Sample_name'][csv_data['isotherm_Y'].isna()].tolist()
        # print(blank_indexes_y)

        # Total_surface_area = csv_data['Article_name'][csv_data['Total_surface_area[m2/g]'].isna()].tolist()
        # print(f'Total_surface_area {Total_surface_area}')


        duplicates_x = csv_data[csv_data.duplicated(subset=['isotherm_X'], keep=False)]
        print(duplicates_x)




        # people_dict = [isotherm.__dict__ for isotherm in list_of_isotherms]
        # print(f'len of dict: {len(people_dict)}')
        # with open('data.json', 'w') as json_file:
            # json.dump(people_dict, json_file,indent=4) # 'indent' for pretty printing
        csv_data.to_csv('all_features.csv', index=False) # saving
        # print(csv_data.info())
        
        
        
