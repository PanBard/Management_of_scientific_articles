import os
import json
from models import Isotherm
import pandas as pd

class DataManager:

    def __init__(self, working_folders):
        self.directory_manager = working_folders
        self.get_data_from_json_file_all()

    def get_data_in_dict_from_all_ris_file(self):
        main_folder_path = self.directory_manager.input_data_folder_path
        data_folders_names =  self.directory_manager.get_only_directory_names_inside_folder(main_folder_path)
        list_of_dicts_of_ris_data = []
        for data_name in data_folders_names:
            data_folder_path = main_folder_path / data_name
            ris_file_path = self.directory_manager.get_files_paths_inside_folder_by_extension(data_folder_path,'ris')
            with open(ris_file_path[0], 'r', encoding='utf-8') as file:
                lines = file.readlines()
                lines = [line.rstrip('\n') for line in lines]
            ris_data = lines
            temporary_dict = {'name':"data", 'ris_data': []}
            temporary_dict['name'] = data_name
            temporary_dict['ris_data'] = ris_data
            list_of_dicts_of_ris_data.append(temporary_dict)
        return list_of_dicts_of_ris_data
    

    def get_specific_ris_data(self, list_of_dicts_of_ris_data ,data_name):
        specific_ris_data = [name['ris_data'] for name in list_of_dicts_of_ris_data if name['name'] == data_name]
        specific_ris_data = specific_ris_data[0]
        ris_dict ={
            'PrimaryTitle' : '',
            'DOI' : '',
            'T1' : '',
            'PY' : '',
            'DA' : ''
        }
        for line in specific_ris_data:
            if (len(line) > 1):
                code = line[0] + line[1]
                if(code == "T1" or code =="TI"): ris_dict['PrimaryTitle'] = line.replace("T1  - ", "").replace("TI  - ", "")
                if(code == "DO"): ris_dict['DOI'] = line.replace("DO  - ", "")
        return ris_dict
        
    def read_all_sample_features_csv_file(self):
        csv_path = self.directory_manager.get_files_paths_inside_folder(self.directory_manager.input_sample_features_path)#  get csv path from imput folder
        df = pd.read_csv(csv_path[0])
        return df


    def get_data_from_json_file_all(self):
        csv_data = self.read_all_sample_features_csv_file()
        csv_data = csv_data.astype({'Sample_name':str}) # make this column as string
        csv_data = csv_data.astype({'Figure_number':str}) # make this column as string
        csv_data = csv_data.astype({'Article_name':str}) # make this column as string
        temp_tar_folder_path = self.directory_manager.temp_tar_files_path
        folders_with_tar_folders =  self.directory_manager.get_only_directory_names_inside_folder(temp_tar_folder_path)
        ris_data = self.get_data_in_dict_from_all_ris_file()
        list_of_isotherms =[]
        for tar_folder in folders_with_tar_folders:
            tar_folder_path = self.directory_manager.temp_tar_files_path / tar_folder
            json_file_path = tar_folder_path / 'wpd.json'
            article_file_name = tar_folder.split('_')[0] 

            graph_image_name_raw = tar_folder.split('_')
            graph_image_name =""
            list_lenght = len(graph_image_name_raw)
            if(list_lenght == 3):
                graph_image_name = graph_image_name_raw[1]
            elif(list_lenght == 4):
                graph_image_name = graph_image_name_raw[1] + '_' + graph_image_name_raw[2]
            elif(list_lenght == 5):
                graph_image_name = graph_image_name_raw[1] + '_' + graph_image_name_raw[2]

            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            min_x = data['axesColl'][0]['calibrationPoints'][0]['dx']
            max_x = data['axesColl'][0]['calibrationPoints'][1]['dx']
            min_y = data['axesColl'][0]['calibrationPoints'][2]['dy']
            max_y = data['axesColl'][0]['calibrationPoints'][3]['dy']

            ris_dict = self.get_specific_ris_data(ris_data, article_file_name)
            csv_data.loc[(csv_data['Article_name'] == article_file_name) , 'DOI'] = ris_dict['DOI']
            csv_data.loc[(csv_data['Article_name'] == article_file_name) , 'PrimaryTitle'] = ris_dict['PrimaryTitle']

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
                #add X and Y data to csv file:
                csv_data.loc[(csv_data['Sample_name'] == new_isotherm.sample_name) & (csv_data['Article_name'] == article_file_name) & (csv_data['Figure_number'] == graph_image_name) , 'isotherm_X'] = str(x_data)
                csv_data.loc[(csv_data['Sample_name'] == new_isotherm.sample_name) & (csv_data['Article_name'] == article_file_name) & (csv_data['Figure_number'] == graph_image_name) , 'isotherm_Y'] = str(y_data)
                

            
 

        blank_indexes_x = csv_data['Article_name'][csv_data['isotherm_X'].isna()].tolist()
        if(len(blank_indexes_x) != 0): 
            print("Blank places in X data: ")
            print(blank_indexes_x)

        duplicates_x = csv_data[csv_data.duplicated(subset=['isotherm_Y'], keep=False)]
        if(len(duplicates_x) != 0): 
            print("Duplicates in data: ")
            print(duplicates_x)

        
        
        

        csv_file_save_path = self.directory_manager.output_csv_path / self.directory_manager.output_csv_file_name
        csv_data.to_csv(csv_file_save_path, index=False) # saving csv file
        print('get_data_from_json_file_all... DONE')

        self.directory_manager.delete_non_empty_directory(self.directory_manager.temp_folder_path)
        
        
        
