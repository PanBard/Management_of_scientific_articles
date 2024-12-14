from pathlib import Path
from natsort import natsorted
import tarfile
import shutil

class TotalChange:

    def __init__(self):

        self.main_working_folder = "main_working_folder_total_change"
        self.main_input_folder = "input_folders"
        self.main_input_graph_folder = "input_graph"
        self.main_input_pdf_folder = "input_pdf"
        self.input_ris_folder = "input_ris"
        self.input_sample_features = "input_sample_features"
        self.total_change_folder = "TOTAL_CHANGE"


        self.main_working_folder_path = Path(self.main_working_folder)
        self.main_input_folder_path = self.main_working_folder_path / self.main_input_folder 
        self.main_input_graph_folder_path = self.main_input_folder_path / self.main_input_graph_folder
        self.main_input_pdf_folder_path = self.main_input_folder_path / self.main_input_pdf_folder
        self.input_ris_folder_path = self.main_input_folder_path / self.input_ris_folder
        self.input_sample_features_path = self.main_input_folder_path / self.input_sample_features
        self.total_change_folder_path = self.main_input_folder_path / self.total_change_folder

        self.make_directory(self.total_change_folder_path)


        
        self.make_folders_for_each_document()
        self.copy_files_from_input_graphs_to_new_folders()
        self.checking_function()
        self.swap_bmp_names_function()
        self.swap_tar_names_function()

    def swap_tar_names_function(self):
        new_folders = self.get_only_directory_names_inside_folder(self.total_change_folder_path)
        counter = 0
        print(f'new_folders {len(new_folders)}')
        for i in range(len(new_folders)):
            folder = new_folders[i]
            path = self.total_change_folder_path / folder
            files_inside = self.get_files_names_and_extensions_inside_folder(path)
            tar_files = [e for e in files_inside if e[1] == '.tar']
            bmp_files = [e for e in files_inside if e[1] == '.bmp']
            if(len(tar_files) == len(bmp_files)):
                counter = counter + 1
                # print(tar_files)
                # print(bmp_files)
                for index in range(len(tar_files)):
                # for bmp_file in bmp_files: #bmp becouse we want change tar files name 
                    # print(f'index: {index}')
                    old_path = path / (tar_files[index][0] + tar_files[index][1])                    
                    new_path = path / (bmp_files[index][0] + tar_files[index][1])
                    shutil.move(old_path, new_path)
                    # print(f'old: {old_path}')
                    # print(f'new: {new_path}')
                    # print('--------------------')



            else:
                print(f'index= {i+1}')
        print(f'counter {counter}')
        print('swap_tar_names_function... DONE')

    def swap_bmp_names_function(self):
        new_folders = self.get_only_directory_names_inside_folder(self.total_change_folder_path)
        for folder in new_folders:
            path = self.total_change_folder_path / folder
            files_inside = self.get_files_names_and_extensions_inside_folder(path)
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
        new_folders = self.get_only_directory_names_inside_folder(self.total_change_folder_path)
        for folder in new_folders:
            path = self.total_change_folder_path / folder
            files_inside = self.get_only_files_names_inside_folder(path)
            counter = counter + len(files_inside)
        oryginal_files = self.get_only_files_names_inside_folder(self.main_input_graph_folder_path)
        if(counter == len(oryginal_files)):
            print(f"{counter} == {len(oryginal_files)}  all files moved to new folders")

    def copy_files_from_input_graphs_to_new_folders(self):
        new_folders = self.get_only_directory_names_inside_folder(self.total_change_folder_path)
        all_files_in_input_graphs = self.get_files_names_and_extensions_inside_folder(self.main_input_graph_folder_path)

        for file_name in new_folders:
            new_folder_path = self.total_change_folder_path / file_name
            for name in all_files_in_input_graphs:
                splitted_name = name[0].split('_')
                if splitted_name[0] == file_name:
                    old_path = self.main_input_graph_folder_path / (name[0] + name[1])
                    new_path = self.total_change_folder_path / splitted_name[0]
                    shutil.copy(old_path, new_path)




    def make_folders_for_each_document(self):
        pdf_files = self.get_only_files_names_inside_folder(self.main_input_pdf_folder_path)
        for file_name in pdf_files:
            # print(file_name)
            new_folder_path = self.total_change_folder_path / file_name
            self.make_directory(new_folder_path)



       


    def make_directory(self,directory_path:Path):
        try:
            directory_path.mkdir()
            print(f"Directory '{directory_path}' created successfully.")
        except FileExistsError:
            # print(f"Directory '{directory_path}' already exists.")
            return
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def get_only_files_names_inside_folder(self,directory_path: Path):
        files = [file.stem for file in directory_path.iterdir() if file.is_file()]
        sorted_files = natsorted(files)
        return sorted_files
    
    def get_files_names_and_extensions_inside_folder(self,directory_path: Path):
        files = [(file.stem, file.suffix) for file in directory_path.iterdir() if file.is_file()]
        sorted_files = natsorted(files)
        return sorted_files
    

    def get_only_directory_names_inside_folder(self,directory_path: Path):
        directory_names = [entry.name for entry in directory_path.iterdir() if entry.is_dir()]
        sorted_directories = natsorted(directory_names)
        return sorted_directories
    
    









