import os 
import pandas as pd
import reportlab as rprt
from pathlib import Path


class FileEplorer(object):
    
    def __init__(self, file_name):
        self.file_name = file_name
    
    def read_file(self):

        # Create an empty list to store the data from the csv file 
        file_contents = []

        # Save the filename with the .csv file extension 
        file_name = self.file_name + ".csv"

        # Create a path to find the given file
        csv_path = Path.home() / "Downloads" / file_name

        # ADD CODE TO CHECK IF FILE EXISTS
        # - - - - - - - - - - - - - - - - - - - - - - - - -
        # IF FILE EXISTS THEN OPEN AND READ FROM FILE
        raw_data = pd.read_csv(csv_path)

        # Read from the collumn containing the download message
        for row in raw_data['Message']:
            
            file_contents.append(row)
        
        return file_contents
    
        # ELSE RETURN ERROR 
        # - - - - - - - - - - - - - - - - - - - - - - - - -

class StringSplicer(object):
    
    def __init__(self):
        self = self
        
    def get_subject(self):
        pass # Add code to splice the subject from the string

    def get_resource_name(string):
        
        # Set a blank string to store the name 
        name = ""
        
        # Save the string to a variable called raw_string
        raw_string = string

        title_index = raw_string.find("Title:") + len("Title:")
        post_type_index = raw_string.find("Post type:") - 1
        
        # Loop through the string and retrieve the resource name
        for i in range(post_type_index):
            if title_index <= i <= post_type_index:
                name += raw_string[i]

        return name

    def get_resource_link(self):
        pass # Add code to splice the resource link from the string

class Calculate(object): 
    
    def __init__(self, contents_list):
        self.contents_list = contents_list
    
    def total():

        # Create empty dictionary to store the totals with the resource name/ subject as the key and the count as the values 
        download_count = {}
        subject_count = {}

        for item in Calculate.contents_list:
            
            resource_name = StringSplicer.get_resource_name(item) 
            resource_link = StringSplicer.get_resource_link(item)

            if resource_name not in download_count:

                # Count how many times the resource name is fount in the list 
                count = sum(1 for content in Calculate.contents_list if resource_name and resource_link in content)

                # Store Count in Dictionary 
                download_count[resource_name] = count

            else:

                continue
        
        for item in Calculate.contents_list:
            
            # Get the name of the subject of the resource
            subject_name = str(StringSplicer.get_subject(item))

            if subject_name not in subject_count:
                
                # Count how many times the subject name is found in the list
                count = sum(1 for subject in Calculate.contents_list if subject_name in subject)

                # Store count in Dictionary 
                subject_count[subject_name] = count


        return download_count, subject_count  
            

            

