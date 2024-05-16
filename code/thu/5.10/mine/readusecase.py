#!/usr/bin/env python
# coding: utf-8

# In[12]:


import json
import os

def write_list_to_file(file_path, my_list):
    with open(file_path, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
def write_list_to_file_with_numbering(file_path, my_list):
    with open(file_path, 'w') as f:
        for i, item in enumerate(my_list, start=1):
            f.write(f"{i}. {item}\n")
def write_json_to_file(file_path, my_list):
    with open(file_path, 'w') as f:
        for item, value in my_list.items():
            f.write("%s\n" % item % value)
def read_file_into_string(file_path):
    encodings = ['utf-8', 'latin-1', 'utf-16', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                file_content = file.read()
            return file_content
        except UnicodeDecodeError:
            print(f"Failed to decode using {encoding} encoding.")
            continue
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    print("All tried encodings failed. Unable to read the file.")
    return None


file_path_list = [
r'D:\GPT-testing\SpecificationData\Adventura\Adventura - Filter.txt',
r'D:\GPT-testing\SpecificationData\Adventura\Adventura - view attraction.txt',
r'D:\GPT-testing\SpecificationData\Adventura\Adventura- Search Attraction.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Add a new author.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Add a new book.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Add a new genre.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Display author details.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Display book details.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Display genre details.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Display the list of authors.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Display the list of books.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Display the list of genres.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Edit the author.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Edit the book.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Edit the genre.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Remove the author.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Remove the book.txt',
r'D:\GPT-testing\SpecificationData\Book(Github)\Remove the genre.txt',
r'D:\GPT-testing\SpecificationData\Film\Add a comment.txt',
r'D:\GPT-testing\SpecificationData\Film\Watch a film.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Add Booking.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Add Employee.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Add Room.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Check in.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Check out.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Hotel Owner - Generate Reports.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Hotel Owner - Update Hotel Information.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\login.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Request Service.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Update Booking.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Update Employee.txt',
r'D:\GPT-testing\SpecificationData\Hotel Management System\Update Room.txt',
r'D:\GPT-testing\SpecificationData\LNLibrary\Bookmark.txt',
r'D:\GPT-testing\SpecificationData\LNLibrary\Rating a book.txt',
r'D:\GPT-testing\SpecificationData\LNLibrary\Read a chapter.txt',
r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\AddQuestion .txt',
r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Flashcard.txt',
r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Handbook.txt',
r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Login.txt',
r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Registry.txt',
r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Review test.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Add or remove item.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Buy Items.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Feedback.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Login.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Pay Bill.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Prepare Bill.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Register Customer.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Search items.txt',
r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Validate Customer.txt',
r'D:\GPT-testing\SpecificationData\ShopeeWeb\Add a type of product into cart.txt',
r'D:\GPT-testing\SpecificationData\ShopeeWeb\Buy product.txt',
r'D:\GPT-testing\SpecificationData\ShopeeWeb\Edit personal shopping cart.txt',
r'D:\GPT-testing\SpecificationData\ShopeeWeb\Rating a product.txt',
r'D:\GPT-testing\SpecificationData\ShopeeWeb\Search feature.txt',
r"D:\GPT-testing\SpecificationData\ShopeeWeb\Track order's status.txt",
r"D:\GPT-testing\SpecificationData\ShopeeWeb\View detail information of a product.txt",
r"D:\GPT-testing\SpecificationData\Trello\create workspace.txt",
r"D:\GPT-testing\SpecificationData\Trello\login.txt",
r"D:\GPT-testing\SpecificationData\Trello\create boards.txt"
]

file_path = file_path_list
print(file_path)
    file_content = read_file_into_string(file_path)
    if( file_content in "None"):
        continue
    usecase = "Use case: "+ read_file_into_string(file_path)
    if usecase is not None:
        element = ExtractCondition(usecase)
        test_scenario_file_path = file_path.replace("SpecificationData", "ResultSet\\5.9\\Propse 1\\")
        # directory, filename = os.path.split(test_scenario_file_path)
        # name, extension = os.path.splitext(filename)
        # new_filename = f"{name} - {count}{extension}"
        # new_path = os.path.join(directory, new_filename)
        # print(new_path)
        write_json_to_file(test_scenario_file_path,(element))
        