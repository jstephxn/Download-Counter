import os 
import pandas as pd
import datetime 
import tkinter
from tkinter import *
from tkinter import messagebox
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet as GetSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


class FileExplorer(object):

    def __init__(self):
        self = self
    
    def read_file(self, file_name):

        # Create an empty list to store the data from the csv file 
        file_contents = []

        # Save the filename with the .csv file extension 
        input_name = file_name + ".csv"

        # Create a path to find the given file
        csv_path = Path.home() / "Downloads" / input_name

        # ADD CODE TO CHECK IF FILE EXISTS
        # - - - - - - - - - - - - - - - - - - - - - - - - -
        # IF FILE EXISTS THEN OPEN AND READ FROM FILE
        raw_data = pd.read_csv(csv_path)

        # Read from the collumn containing the download message
        for row in raw_data['Message']:
            
            file_contents.append(row)
        
        # Clear the raw data variable to free up memory
        raw_data = None

        return file_contents
    
        # ELSE RETURN ERROR 
        # - - - - - - - - - - - - - - - - - - - - - - - - -

class StringSplicer(object):
    
    def __init__(self):
        pass


    def get_resource_name(self, string):
        
        
        # Set a blank string to store the name 
        name = ""
        
        # Save the string to a variable called raw_string
        raw_string = string

        title_index = raw_string.find("Title:") + 6
        post_type_index = raw_string.find("Post Type:") - 1
        
        # Loop through the string and retrieve the resource name
        for i in range(post_type_index):
            
            # if i is more than or equal to the title index and less than or equal to the post type index then add the character to the name string
            if title_index <= i <= post_type_index:
                name += raw_string[i]
               
            # Remove any Semicolons from the name string
        name = name.replace(";", "")

        # Remove any leading or trailing whitespace from the name string
        name = name.strip()

        return name

    def get_resource_link(self,string):
        
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

        string_splicer = StringSplicer()

        # Create empty dictionary to store the totals with the resource name/ subject as the key and the count as the values 
        download_count = {}
        subject_count = {}

        for item in self.contents_list:

            resource_name = string_splicer.get_resource_name(item)
            resource_link = string_splicer.get_resource_link(item)

            # If the resource name is not already in the dictionary then count how many times it appears in the list
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
        subjects = [
                    "Maths", "English", "Science", "History", "Geography", "Art", "RE", "DT", 
                    "Spelling with Grammarsaurus", "Sentence Pattern Building", "SATs Smasher", 
                    "Unit Guide", "The Place Value of Punctuation and Grammar", "PVPG", "Model Texts", 
                    "SPaG", "Writing", "Reading", "Phonics", "Comprehension Crusher"
                    ]

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
        Raw_year_groups = [
                        "EYFS", "KS1", "KS2", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", 
                        "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"
                      ]  

        for year in Raw_year_groups:

            if year not in year_group_count:

                # Count how many times the year group is found in the list 
                count = sum(1 for content in self.contents_list if year in content)

                # Store Count in Dictionary 
                year_group_count[year] = count

            else:

                continue

        final_year_group_count = self.calculate_difference(year_group_count)
        final_subject_count = self.calculate_subject_values(subject_count)

        # Sort each of the dictionaries from high to low based on the values

        download_count = dict(sorted(download_count.items(), key=lambda item: item[1], reverse=True))
        final_subject_count = dict(sorted(subject_count.items(), key=lambda item: item[1], reverse=True))
        final_year_group_count = dict(sorted(year_group_count.items(), key=lambda item: item[1], reverse=True))
        
        total_downloads = len(self.contents_list)

        # Clear the contents list to free up memory
        self.contents_list.clear()
        self.contents_list = None

        # Return the three dictionaries and the total downloads figure
        return download_count, final_subject_count, final_year_group_count, total_downloads
    
    def calculate_difference(self, dict):

        for i in range(1, 7):
            short_key = f"Y{i}"
            long_key = f"Year {i}"

            short_count = dict.get(short_key, 0)
            long_count = dict.get(long_key, 0)

            # Calculate the difference between the two counts
            if short_count > long_count:
                combined_count = abs(short_count - long_count) + min(short_count, long_count)
            else:
                combined_count = abs(long_count - short_count) + min(short_count, long_count)

            # remove the individual keys from the original dictionary
            if short_key in dict:
                del dict[short_key]
            dict[f"Year {i}"] = combined_count

        return dict
    
    def calculate_subject_values(self, dict):

        # In the Data PVPG and The Place Value of Punctuation and Grammar are the same subject so need to be combined
        if "PVPG" in dict and "The Place Value of Punctuation and Grammar" in dict:
            
            dict["The Place Value of Punctuation and Grammar"] += dict["PVPG"]
            
            # Remove PVPG from the dictionary
            del dict["PVPG"]
        
        # In the Data The place Value of Punctuation and Grammar and SPaG fall under the same subject so need to subtract The Place Value of Punctuation and Grammar from SPaG
        if "SPaG" in dict and "The Place Value of Punctuation and Grammar" in dict:
            
            dict["SPaG"] -= dict["The Place Value of Punctuation and Grammar"]
            
            # Ensure SPaG does not go below 0
            if dict["SPaG"] < 0:
                dict["SPaG"] = 0

        return dict


class GenerateReport(object):

    def __init__(self, download_count, subject_count, year_group_count, total_downloads):
        self.download_count = download_count
        self.subject_count = subject_count
        self.year_group_count = year_group_count
        self.total_downloads = total_downloads

    def create_report(self, report_name):
        
        # Set the name of the document to be create with a .pdf extension
        report_name = report_name + ".pdf"

        # Create a path to save the report to a folder within the users documents folder
        report_path = Path.home() / "Documents" / "Download Statistics Reports"

        # Check if the directory exists if not create it
        if not os.path.exists(report_path):
            
            os.makedirs(report_path)

        output_path = report_path / report_name

        # create an empty list to contain all the elements of the document
        elements = []

        # Get the styles for the doocument 
        styles = GetSampleStyleSheet()

        # Set the style for the normal text
        wrap_style = styles['Normal']

        # Set the style for the tables
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),     # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),      # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),              # Left align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),           # Header padding
            ('BACKGROUND', (0, 1), (-1, -1), '#f9f9f9'),    # Body background color
            ('GRID', (0, 0), (-1, -1), 1, "#242424"),       # Grid lines
        ])

        # Add a title to the document
        title = Paragraph("Download Statistics Report - " + datetime.datetime.now().strftime("%Y-%m-%d"), styles['Title'])
        elements.append(title)

        # Add a spacer
        elements.append(Spacer(1, 12))

        # Add the total downloads figure to the elements list
        total_downloads_para = Paragraph(f"<b>Total Downloads:</b> {self.total_downloads}", wrap_style)
        elements.append(total_downloads_para)
        
        # Add a spacer
        elements.append(Spacer(1, 12))
        
        # Create the tables for each of the dictionaries and add them to the document elements list
        
        # Resource Download Table
        download_table_data = [['#','Resource Name', 'Total Downloads']]
        
        download_data = self.download_count

        for i, (resource, count) in enumerate(download_data.items()):
            if i >= 50:
                break
            download_table_data.append([int(i + 1), Paragraph(resource, wrap_style), int(count)])
                

        download_table = Table(download_table_data)
        download_table.setStyle(table_style)

        elements.append(Paragraph("Total Downloads per Resource", styles['Heading2']))
        
        elements.append(download_table)
        
        # Add a spacer
        elements.append(Spacer(1, 12))

        # Subject Download Table
        subject_table_data = [['Subject', 'Total Downloads']]
        for subject, count in self.subject_count.items():
            subject_table_data.append([subject, count])

        subject_table = Table(subject_table_data)
        subject_table.setStyle(table_style)
        elements.append(Paragraph("Total Downloads per Subject", styles['Heading2']))
        
        elements.append(subject_table)

        # Add a spacer
        elements.append(Spacer(1, 12))

        year_group_table_data = [['Year Group', 'Total Downloads']]
        for year_group, count in self.year_group_count.items():
            year_group_table_data.append([year_group, count])

        year_group_table = Table(year_group_table_data)
        year_group_table.setStyle(table_style)
        elements.append(Paragraph("Total Downloads per Year Group", styles['Heading2']))
        
        elements.append(year_group_table)
        

        # Create the PDF document
        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        doc.build(elements)
        

class Application(object):
    
    def __init__(self):
        self = self
    
    def button_clicked(self, csv_name, report_name):
        if not csv_name or not report_name:
            messagebox.showerror("Input Error", "Both fields are required.")
        
        else:
 
            # Read the file
            file_explorer = FileExplorer()
            contents_list = file_explorer.read_file(csv_name)

            # Calculate the totals
            calculator = Calculate(contents_list)
            download_count, subject_count, year_group_count, total_downloads = calculator.total()

            # Generate the report
            report_generator = GenerateReport(download_count, subject_count, year_group_count, total_downloads)
            report_generator.create_report(report_name)

            messagebox.showinfo("Success", f"Report '{report_name}_Report.pdf' has been generated successfully in your Documents folder.")

    

    def run(self):
        
        master = Tk()
        master.title("Download Statistics Report Generator")
        master.geometry("250x250")
        master.resizable(False, False)

        # Create empty string vairables to store inputs from the user in the application 
        csv_name = tkinter.StringVar()
        report_name = tkinter.StringVar()

        # Create a label and entry for the file name
        report_label = Label(master, text="Please enter the name of the csv file:")
        report_label.pack()

        report_entry = Entry(master, textvariable= csv_name)
        report_entry.pack()

        # Create a label and entry for the report name
        file_label = Label(master, text="Please enter a name for the report:")
        file_label.pack(padx=5, pady=5)

        file_entry = Entry(master, textvariable= report_name)
        file_entry.pack(padx=5, pady=5)

        # Create a button to generate the report
        generate_button = Button(master, text="Generate Report", command=lambda: self.button_clicked(csv_name.get(), report_name.get()))
        generate_button.pack(pady=20)

        master.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()
