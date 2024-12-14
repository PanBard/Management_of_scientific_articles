import os
from natsort import natsorted
import tarfile
import shutil

class DirectoryManager:

    def __init__(self):
        self.current_working_directory = os.getcwd()
        self.main_working_folder = os.path.join(self.current_working_directory, "main_working_folder")
        self.input_folder_path= os.path.join(self.main_working_folder, "input_folders")
        self.output_folders_path = os.path.join(self.main_working_folder, "output_folders")
        self.temp_folder_path = os.path.join(self.main_working_folder, "temp_folders")
        self.json_inside_tar_name = 'wpd.json'

        self.input_pdf = "input_pdf"
        self.input_ris = "input_ris"
        self.input_graph = "input_graph"
        self.input_sample_features = "input_sample_features"

        self.output_pdf = "output_pdf"
        self.output_folders = "output_folders"
        self.output_excel = "output_excel"
        self.output_json = "output_json"

        self.temp_tar_files = "tar_files"

        self.input_pdf_path = self.made_path(self.input_pdf, self.input_folder_path)
        self.input_ris_path  = self.made_path(self.input_ris, self.input_folder_path)
        self.input_graph_path  = self.made_path(self.input_graph, self.input_folder_path)
        self.input_sample_features_path  = self.made_path(self.input_sample_features, self.input_folder_path)

        self.output_pdf_path  = self.made_path(self.output_pdf, self.output_folders_path)
        self.output_folder_path  = self.made_path(self.output_folders, self.output_folders_path)
        self.output_excel_path  = self.made_path(self.output_excel, self.output_folders_path)
        self.output_json_path  = self.made_path(self.output_json, self.output_folders_path)

        self.temp_tar_files_path  = self.made_path(self.temp_tar_files, self.temp_folder_path)


        self.check_if_exist_and_made_directory(self.input_pdf_path)
        self.check_if_exist_and_made_directory(self.input_ris_path)
        self.check_if_exist_and_made_directory(self.input_graph_path)
        self.check_if_exist_and_made_directory(self.input_sample_features_path)

        self.check_if_exist_and_made_directory(self.output_pdf_path)
        self.check_if_exist_and_made_directory(self.output_folder_path)
        self.check_if_exist_and_made_directory(self.output_excel_path)
        self.check_if_exist_and_made_directory(self.output_json_path)

        self.check_if_exist_and_made_directory(self.temp_folder_path)
        self.check_if_exist_and_made_directory(self.temp_tar_files_path)

        self.extract_tar_file()
        # ----------
        elos = self.copy_bmp_files_to_temp_folders()
        print(f'Number of bmp files: {len(elos)}')
        # ----------

        self.sprawdzawrka()

    def check_if_exist_and_made_directory(self,folder_path):
        if not os.path.isdir(folder_path):      # Check if the directory exists
            os.makedirs(folder_path)# Create the directory
            print(f"Directory '{folder_path}' created.")


    def made_path(self,folder_name, main_path):
        new_path = os.path.join(main_path, folder_name)
        return new_path

    def get_files_inside_folder(self,folder_path):
        entries = os.listdir(folder_path)
        sorted_files = natsorted(entries)
        return sorted_files
    
    def get_path_of_files_inside_folder(self,folder_path):
        entries = os.listdir(folder_path)
        file_paths = [ os.path.join(folder_path, entry) for entry in entries ]
        sorted_file_paths = natsorted(file_paths)
        return sorted_file_paths
    
    def extract_tar_file(self):
        tar_files = self.get_only_tar_files()
        print(f"Number of tar files: {len(tar_files)}")

        for tar_file in tar_files:
            tar_file_path = os.path.join(self.input_graph_path, tar_file)
            file_name_without_extension = tar_file.replace('.tar', '')
            path_inside_tar_file = os.path.join(file_name_without_extension, self.json_inside_tar_name )
            # print(path_inside_tar_file)
            with tarfile.open(tar_file_path, 'r') as tf: # Open the tar file          
                # tf.extract(path_inside_tar_file, path=self.temp_tar_files_path)# Extract the specific file to a temporary location
                tf.extractall( path=self.temp_tar_files_path)# Extract the specific file to a temporary location

    def get_only_tar_files(self):
        entries = self.get_files_inside_folder(self.input_graph_path)
        tar_files = [entry for entry in entries if entry.endswith('.tar')]
        sorted_tar_files = natsorted(tar_files)
        return sorted_tar_files
    

    def copy_bmp_files_to_temp_folders(self):
        entries = self.get_files_inside_folder(self.input_graph_path)
        source_bmp_files = [entry for entry in entries if entry.endswith('.bmp')]
        sorted_source_bmp_files = natsorted(source_bmp_files)
        # destination_bmp_files = 
        return sorted_source_bmp_files
    
    def sprawdzawrka(self):
        bpm = self.copy_bmp_files_to_temp_folders()
        tar = self.get_only_tar_files()

        for i in range(len(bpm)):
            print(bpm[i])
            print(tar[i])
            print("------------------------------------------")




