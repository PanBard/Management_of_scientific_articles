from pathlib import Path
from natsort import natsorted
import tarfile
import shutil
import json

class TotalChange:

    def __init__(self, working_folders):
        self.directory_manager = working_folders
        self.main_working_folder = "main_working_folder_total_change"
        self.total_change_folder = "TOTAL_CHANGE"
        self.tar_file_change_folder = "TAR_CHANGE"
        self.main_working_folder_path = Path(self.main_working_folder)
        self.total_change_folder_path = self.main_working_folder_path / self.total_change_folder
        self.tar_file_change_folder_path = self.main_working_folder_path / self.tar_file_change_folder
        self.directory_manager.make_directory(self.main_working_folder_path)
        self.directory_manager.make_directory(self.total_change_folder_path)
        self.directory_manager.make_directory(self.tar_file_change_folder_path)


        # #---------- I
        # self.make_folders_for_each_document()
        # self.copy_files_from_input_graphs_to_new_folders()
        # self.checking_function()
        # self.swap_bmp_names_function()
        # self.swap_tar_names_function()
        # self.extract_tar_file_to_change_folder()
        # #--------- I

        # self.change_name_and_json_files()

        # self.move_pdf_filest_to_data_folders()  # before run this functions move new folders from TOTAL_CHANGE to input_data folder
        # self.move_ris_files_to_data_folders()


        # self.function_to_change_one_data_dir('Data15','Data15_1_figure')
        # self.function_to_change_one_data_dir('Data34','Data34_2_figure')


    def move_ris_files_to_data_folders(self):
        data_folders = self.directory_manager.get_only_directory_names_inside_folder(self.directory_manager.input_data_folder_path)
        for data_folder in data_folders:
            path_to_data_folder = self.directory_manager.input_data_folder_path / data_folder
            old_path = self.directory_manager.input_ris_folder_path / (data_folder + '.ris')
            new_path = path_to_data_folder / (data_folder + '.ris')
            shutil.move(old_path, new_path)


    def move_pdf_filest_to_data_folders(self):
        data_folders = self.directory_manager.get_only_directory_names_inside_folder(self.directory_manager.input_data_folder_path)
        for data_folder in data_folders:
            path_to_data_folder = self.directory_manager.input_data_folder_path / data_folder
            old_path = self.directory_manager.input_pdf_folder_path / (data_folder + '.pdf')
            new_path = path_to_data_folder / (data_folder + '.pdf')
            shutil.move(old_path, new_path)


    def swap_tar_names_function(self):
        new_folders = self.directory_manager.get_only_directory_names_inside_folder(self.total_change_folder_path)
        counter = 0
        print(f'new_folders {len(new_folders)}')
        for i in range(len(new_folders)):
            folder = new_folders[i]
            path = self.total_change_folder_path / folder
            files_inside = self.directory_manager.get_files_names_and_extensions_inside_folder(path)
            tar_files = [e for e in files_inside if e[1] == '.tar']
            bmp_files = [e for e in files_inside if e[1] == '.bmp']
            if(len(tar_files) == len(bmp_files)):
                counter = counter + 1
                for index in range(len(tar_files)):
                    old_path = path / (tar_files[index][0] + tar_files[index][1])                    
                    new_path = path / (bmp_files[index][0] + tar_files[index][1])
                    shutil.move(old_path, new_path)




            else:
                print(f'index= {i+1}')
        print(f'counter {counter}')
        print('swap_tar_names_function... DONE')

    def swap_bmp_names_function(self):
        new_folders = self.directory_manager.get_only_directory_names_inside_folder(self.total_change_folder_path)
        for folder in new_folders:
            path = self.total_change_folder_path / folder
            files_inside = self.directory_manager.get_files_names_and_extensions_inside_folder(path)
            for file in files_inside:
                if(file[1] == '.bmp'):                
                    # print(file)
                    elo = file[0].replace('f','')
                    # print(elo)
                    old_path = path / (file[0] + file[1])
                    new_path = path / (elo + '_figure' + file[1])
                    # print(old_path)
                    # print(new_path)
                    shutil.move(old_path, new_path)
        print('swap_bmp_names_function... DONE')

    def checking_function(self):
        counter = 0
        new_folders = self.directory_manager.get_only_directory_names_inside_folder(self.total_change_folder_path)
        for folder in new_folders:
            path = self.total_change_folder_path / folder
            files_inside = self.directory_manager.get_only_files_names_inside_folder(path)
            counter = counter + len(files_inside)
        oryginal_files = self.directory_manager.get_only_files_names_inside_folder(self.directory_manager.input_graph_folder_path)
        if(counter == len(oryginal_files)):
            print(f"{counter} == {len(oryginal_files)}  all files moved to new folders")

    def copy_files_from_input_graphs_to_new_folders(self):
        new_folders = self.directory_manager.get_only_directory_names_inside_folder(self.total_change_folder_path)
        all_files_in_input_graphs = self.directory_manager.get_files_names_and_extensions_inside_folder(self.directory_manager.input_graph_folder_path)

        for file_name in new_folders:
            for name in all_files_in_input_graphs:
                splitted_name = name[0].split('_')
                if splitted_name[0] == file_name:
                    old_path = self.directory_manager.input_graph_folder_path / (name[0] + name[1])
                    new_path = self.total_change_folder_path / splitted_name[0]
                    shutil.copy(old_path, new_path)
        print('copy_files_from_input_graphs_to_new_folders ... DONE')


    def make_folders_for_each_document(self):
        pdf_files = self.directory_manager.get_only_files_names_inside_folder(self.directory_manager.input_pdf_folder_path)
        for file_name in pdf_files:
            new_folder_path = self.total_change_folder_path / file_name
            self.directory_manager.make_directory(new_folder_path)


    def extract_tar_file_to_change_folder(self):
        all_folders = self.directory_manager.get_only_directory_names_inside_folder(self.total_change_folder_path)
        for folder in all_folders:
            path = self.total_change_folder_path / folder
            files_inside = self.directory_manager.get_files_names_and_extensions_inside_folder(path)
            tar_files = [e for e in files_inside if e[1] == '.tar']
            bmp_files = [e for e in files_inside if e[1] == '.bmp']
            if(len(tar_files) == len(bmp_files)):
                for index in range(len(tar_files)):
                    change_folder =  self.total_change_folder_path / folder
                    tar_folder_path  = change_folder / (tar_files[index][0] + tar_files[index][1])
                    with tarfile.open(tar_folder_path, 'r') as tf:
                        tf.extractall( path=change_folder)
    
    def extract_tar_file_to_change_folder_from_one_folder(self, main_input_folder_name):
        folder = main_input_folder_name
        path = self.directory_manager.input_data_folder_path / folder
        files_inside = self.directory_manager.get_files_names_and_extensions_inside_folder(path)
        tar_files = [e for e in files_inside if e[1] == '.tar']
        print(tar_files)
        for index in range(len(tar_files)):
            change_folder =  self.total_change_folder_path / folder
            tar_folder_path  = path / (tar_files[index][0] + tar_files[index][1])
            with tarfile.open(tar_folder_path, 'r') as tf:
                tf.extractall( path=change_folder)


    def change_name_and_json_files(self):
        all_folders = self.directory_manager.get_only_directory_names_inside_folder(self.total_change_folder_path)
        for folder in all_folders:
            path = self.total_change_folder_path / folder
            files_inside = self.directory_manager.get_files_names_and_extensions_inside_folder(path)
            tar_files = [e for e in files_inside if e[1] == '.tar']
            bmp_files = [e for e in files_inside if e[1] == '.bmp']
            if(len(tar_files) == len(bmp_files)):
                change_folder =  self.total_change_folder_path / folder
                new_folders = self.directory_manager.get_only_directory_names_inside_folder(change_folder)
                for inx in  range(len(new_folders)):
                    old_path = change_folder / new_folders[inx]      
                    new_path = change_folder / bmp_files[inx][0]
                    shutil.move(old_path, new_path) # rename tar folder

                    bmp_filess = [(file.stem, file.suffix)for file in new_path.glob('*.bmp')]
                    old_image = new_path / (bmp_filess[0][0] + bmp_filess[0][1])
                    new_image = new_path / (bmp_files[inx][0] + bmp_files[inx][1])
                    shutil.move(old_image, new_image)  #rename inage inside tar folder

                    new_json = new_path / "info.json"
                    data_to_save = {"version":[4,0],"json":"wpd.json","images":["Data1 f1.bmp"]}
                    data_to_save['images'][0] = bmp_files[inx][0] + bmp_files[inx][1]
                    with open(new_json, "w") as json_file:
                        json.dump(data_to_save, json_file)
                    
                    tar_file_folder = change_folder / bmp_files[inx][0]
                    tar_file_path = change_folder / (bmp_files[inx][0] + '.tar')
                    print(tar_file_path)
                    print(f'new_folders ---------------------  {new_folders}')
                    print(f'tar_file_folder ---------------------  {tar_file_folder}')
                    print(f'bmp_files[inx][0] ---------------------  {bmp_files[inx][0]}')
                    with tarfile.open(tar_file_path, "w") as tar:
                        tar.add(tar_file_folder, arcname=bmp_files[inx][0] )

                    self.directory_manager.delete_non_empty_directory(tar_file_folder)




    def function_to_change_one_data_dir(self, main_input_folder_name, image_name):
        self.extract_tar_file_to_change_folder_from_one_folder(main_input_folder_name)
        path = self.total_change_folder_path / main_input_folder_name
        new_folders = self.directory_manager.get_only_directory_names_inside_folder(path)
        # files_inside = self.directory_manager.get_files_names_and_extensions_inside_folder(path)
        print(new_folders)
        print(image_name)
        for inx in  range(len(new_folders)):
            tar_file_new_name = image_name + f'{inx+1}'
            old_path = path / new_folders[inx]      
            new_path = path / tar_file_new_name
            # print(old_path)
            # print(new_path)
            shutil.move(old_path, new_path) # rename tar folder

            bmp_filess = [(file.stem, file.suffix)for file in new_path.glob('*.bmp')]
            old_image = new_path / (bmp_filess[0][0] + bmp_filess[0][1])
            new_image = new_path / (image_name + '.bmp')
            shutil.move(old_image, new_image)  #rename inage inside tar folder

            new_json = new_path / "info.json"
            data_to_save = {"version":[4,0],"json":"wpd.json","images":["Data1 f1.bmp"]}
            data_to_save['images'][0] = (image_name + '.bmp')
            with open(new_json, "w") as json_file:
                json.dump(data_to_save, json_file)
            
            tar_file_folder = path / tar_file_new_name
            tar_file_path = path / (tar_file_new_name + '.tar')
            print(tar_file_path)
            print(f'new_folders ---------------------  {new_folders}')
            print(f'tar_file_folder ---------------------  {tar_file_folder}')
            print(f'bimage_name---------------------  {image_name}')
            with tarfile.open(tar_file_path, "w") as tar:
                tar.add(tar_file_folder, arcname=tar_file_new_name )

            self.directory_manager.delete_non_empty_directory(tar_file_folder)




