import os 
import pandas as pd
import reportlab 
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet as GetSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import datetime



class FileExplorer(object):

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

    def get_resource_link(string):
        
        # Set a blank string to store the link
        link = ""

        # Save the string to a variable called raw_string
        raw_string = string

        # Get the index of the two key points in the string 
        file_index = raw_string.find("File:") + len("File:")
        membership_index = raw_string.find("Memberships:") - 1

        # Loop through the string and retrieve the resource link
        for i in range(membership_index):
            if file_index <= i <= membership_index:
                link += raw_string[i]

        return link


class Calculate(object): 
    
    def __init__(self, contents_list):
        self.contents_list = contents_list
    
    def total(self):

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # First calculate the total downloads for each resource 
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # Create empty dictionary to store the totals with the resource name/ subject as the key and the count as the values 
        download_count = {}
        subject_count = {}

        for item in self.contents_list:
            
            resource_name = StringSplicer.get_resource_name(item) 
            resource_link = StringSplicer.get_resource_link(item)

            if resource_name not in download_count:

                # Count how many times the resource name is fount in the list 
                count = sum(1 for content in self.contents_list if resource_name and resource_link in content)

                # Store Count in Dictionary 
                download_count[resource_name] = count

            else:

                continue

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Second calculate the total downloads for each subject 
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            
        # Get the name of the subject of the resource
        subjects = ["Maths", "English", "Science", "History", "Geography", "Art", "RE", "DT", "PSHE", "SATs Smasher", "Unit Guide", "The Place Value of Punctuation and Grammar", "PVPG", "Model Texts", "SPaG", "Writing", "Reading", "Phonics", "Comprehension Crusher"]

        for subject in subjects:

            if subject not in subject_count:

                # Count how many times the subject is found in the list 
                count = sum(1 for content in self.contents_list if subject in content)

                # Store Count in Dictionary 
                subject_count[subject] = count

            else:

                continue    
            
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Third Calculate the total downloads for each year group
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        year_group_count = {}
        year_groups = ["EYFS", "KS1", "KS2", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"]

        for year in year_groups:

            if year not in year_group_count:

                # Count how many times the year group is found in the list 
                count = sum(1 for content in self.contents_list if year in content)

                # Store Count in Dictionary 
                year_group_count[year] = count

            else:

                continue
        
        # ADD a way to loop through the year groups and add the totals for each key that is the same
        # e.g. Y1 and Year 1
        # Possibly have to look through the counts and subtract the difference as some strings have both Y1 and Year 1 in them
        
        # Sort each of the dictionaries from high to low based on the values

        download_count = dict(sorted(download_count.items(), key=lambda item: item[1], reverse=True))
        subject_count = dict(sorted(subject_count.items(), key=lambda item: item[1], reverse=True))
        year_group_count = dict(sorted(year_group_count.items(), key=lambda item: item[1], reverse=True))
        
        return download_count, subject_count, year_group_count
            
class GenerateReport(object):
    
    def __init__(self, download_count, subject_count, year_group_count, file_name):
        self.download_count = download_count
        self.subject_count = subject_count
        self.year_group_count = year_group_count
        self.file_name = file_name

    def create_report(self):
        
        # Set the name of the document to be create with a .pdf extension
        report_name = self.file_name + "_Report.pdf"

        # Create a path to save the report to a folder within the users documents folder
        report_path = Path.home() / "Documents" / "Download Statistics Reports" / report_name

        # Check if the directory exists if not create it
        if not os.path.exists(os.path.dirname(report_path)):
            
            os.makedirs(os.path.dirname(report_path))

        # create an empty list to contain all the elements of the document
        elements = [[]]

        # Get the styles for the doocument 
        styles = GetSampleStyleSheet()

        # Set the style for the normal text
        wrap_style = styles['Normal']

        # Set the style for the tables
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),     # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),      # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),            # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),           # Header padding
            ('BACKGROUND', (0, 1), (-1, -1), '#f9f9f9'),    # Body background color
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),       # Grid lines
        ])

        # Add a title to the document
        title = Paragraph("Download Statistics Report - " + datetime.datetime.now().strftime("%Y-%m-%d"), styles['Title'])
        elements.append(title)

        # Add a spacer
        elements.append(Spacer(1, 12))

        # Create the tables for each of the dictionaries and add them to the document elements list
        
        # Resource Download Table
        download_table_data = [['Resource Name', 'Total Downloads']]

        for resource, count in self.download_count.items():
            download_table_data.append([resource, count])

        download_table = Table(download_table_data)
        download_table.setStyle(table_style)

        elements.append(Paragraph("Total Downloads per Resource", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(download_table)
        elements.append(Spacer(1, 24))

        # Subject Download Table
        subject_table_data = [['Subject', 'Total Downloads']]
        for subject, count in self.subject_count.items():
            subject_table_data.append([subject, count])
        subject_table = Table(subject_table_data)
        subject_table.setStyle(table_style)
        elements.append(Paragraph("Total Downloads per Subject", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(subject_table)
        elements.append(Spacer(1, 24))

        
        year_group_table_data = [['Year Group', 'Total Downloads']]
        for year_group, count in self.year_group_count.items():
            year_group_table_data.append([year_group, count])
        year_group_table = Table(year_group_table_data)
        year_group_table.setStyle(table_style)
        elements.append(Paragraph("Total Downloads per Year Group", styles['Heading2']))
        elements.append(Spacer(1, 12))
        elements.append(year_group_table)
        elements.append(Spacer(1, 24))

        # Create the PDF document
        doc = SimpleDocTemplate(report_path, pagesize=A4)
        doc.build(elements)
        
