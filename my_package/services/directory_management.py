from pathlib import Path
from natsort import natsorted
import tarfile
import shutil

class DirectoryManager:

    def __init__(self):

        self.main_working_folder = "main_working_folder"
        self.main_working_folder_path = Path("main_working_folder")

        # -------------------------------------- input
        self.input_folder = "input_folders"
        self.input_folder_path = self.main_working_folder_path / self.input_folder

        self.input_graph_folder = "input_graph"
        self.input_graph_folder_path  = self.input_folder_path / self.input_graph_folder

        self.input_data_folder = "input_data"
        self.input_data_folder_path  = self.input_folder_path / self.input_data_folder
        # self.input_pdf_folder = "input_pdf"
        # self.input_pdf_folder_path = self.input_folder_path / self.input_pdf_folder
        # self.input_ris_folder = "input_ris"
        # self.input_ris_folder_path = self.input_folder_path / self.input_ris_folder
        self.input_sample_features = "input_sample_features"
        self.input_sample_features_path = self.input_folder_path / self.input_sample_features
         # -------------------------------------- input

        #---------------------------------------- output
        self.output_folders = "output_folders"
        self.output_folders_path = self.main_working_folder_path / self.output_folders

        # self.output_pdf = "output_pdf"
        # self.output_pdf_path = self.output_folders_path / self.output_pdf
        # self.output_excel = "output_excel"
        # self.output_excel_path = self.output_folders_path / self.output_excel
        # self.output_json = "output_json"
        # self.output_json_path = self.output_folders_path / self.output_json
        self.output_csv = "output_csv"
        self.output_csv_path = self.output_folders_path / self.output_csv

        self.output_csv_file_name = 'all_data.csv'
        #---------------------------------------- output

        self.temp_folder = "temp_folders"
        self.temp_folder_path = self.main_working_folder_path / self.temp_folder
        self.temp_tar_files = "tar_files"
        self.temp_tar_files_path  = self.temp_folder_path / self.temp_tar_files

        
        self.make_folder_enviroment()
        self.extract_tar_file()


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

    def extract_tar_file(self):
        data_folders = self.get_only_directory_names_inside_folder(self.input_data_folder_path)
        for data_folder in data_folders:
            data_folder_path = self.input_data_folder_path / data_folder
            tar_files_paths = list(data_folder_path.glob('*.tar'))
            for tar_path in tar_files_paths:
                with tarfile.open(tar_path, 'r') as tf: # Open the tar file  
                    tf.extractall( path=self.temp_tar_files_path)
                
    def get_files_paths_inside_folder(self, path):
        files_paths = list(path.glob('*.*'))
        return files_paths
    
    def get_files_paths_inside_folder_by_extension(self, path, extension):
        files_paths = list(path.glob(f'*.{extension}'))
        return files_paths

    def make_folder_enviroment(self):
        self.make_directory(self.main_working_folder_path)
        self.make_directory(self.input_folder_path)
        self.make_directory(self.input_data_folder_path)
        self.make_directory(self.input_sample_features_path)
        self.make_directory(self.output_folders_path)
        # self.make_directory(self.output_pdf_path)
        # self.make_directory(self.output_excel_path)
        # self.make_directory(self.output_json_path)
        self.make_directory(self.temp_folder_path)
        self.make_directory(self.temp_tar_files_path)
        self.make_directory(self.output_csv_path)

    def delete_non_empty_directory(self, directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"The directory {directory_path} has been deleted.")
        except OSError as e:
            print(f"Error: {e.strerror}")
