from models import Article
from services import DirectoryManager, DataManager, TotalChange
import os
def main():
    
    working_folders= DirectoryManager()
    data_operator = DataManager(working_folders)

if __name__ == "__main__":
    main()