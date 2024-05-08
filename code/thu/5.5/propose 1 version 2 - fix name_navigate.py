#!/usr/bin/env python
# coding: utf-8

# In[1500]:


from openai import OpenAI
import json
import os

GPT_MODEL_3_5 = "gpt-3.5-turbo-1106"
GPT_MODEL_4 = "gpt-4-0125-preview"

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()
model = GPT_MODEL_4

def ask(prompt, client, model, temperature = 0):
    response = None
    
    response = client.chat.completions.create(
      model=model,
      messages=prompt,
      temperature=temperature,
      response_format={ "type": "json_object" },
    )

    return (response.choices[0].message.content)




# In[1501]:


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


# In[1502]:


def write_to_file(filename, s):
    try:
        with open(filename, 'w') as file:
            file.write(s)
        print("Content has been written to", filename)
    except Exception as e:
        print("An error occurred:", e)

def gentestscenario(usecase):

    default_flow = "Basic flow"

    SYSTEM_PROMPT_extract_flow ="""
    Given use case specification flows.
    Extract all the contents of flows into json format.
    Return the flows in json format.
    {
    "Flow name":[ contents of corresponding flow],
    }
    For example: 
    {
    "Main flow:": [
        "Step 1: Learner fills in the username field by a valid username that has been registered",
        "Step 2: Learner fills in the password field by the correct password for the corresponding username",
        "Step 3: Learner press \"Login\" button",
        "Step 4: System redirects learner to Home page"
    ],
    "Alternative flow 1: Login by email": [
        "At step 1 of the basic flow: Learner fills in the username field by a valid email that has been registered",
        "Step 2: Learner fills in the password field by the correct password for the corresponding email",
        "Go back to step 3 in the basic flow and continue with the steps from step 3"
    ]
    }
    """


    # In[1507]:


    promptExtractCondtition = [
        { "role": "system", "content": SYSTEM_PROMPT_extract_flow},
        { "role": "user", "content": usecase}
    ]

    gpt_response = ask(promptExtractCondtition, client, model)
    print(gpt_response)
    usecase_flow = json.loads(gpt_response)
    flows_name = [key for key in usecase_flow]

    # usecase_temp = 
    # flows_name = ["Basic Flow","Alternative flow 1","Alternative flow 2","Alternative flow 3","Alternative flow 4","Alternative flow 5","Alternative flow 6","Alternative flow 7","Alternative flow " ]
    # usecase_flow = json.loads(usecase_temp)


    # In[1508]:


    for flow_name in flows_name:
        if 'Basic' in flow_name:
            default_flow = flow_name
        if 'Main' in flow_name:
            default_flow = flow_name

    print(default_flow)


    # In[1509]:


    SYSTEM_PROMPT_extract_condition ="""
    Given use case flows of a feature.
    Your task is to identify all the interactive elements within the application. 
    For each interactive element:
    Identify what type of that element (button,buttons, icon,scroll, text field, radio buttons, menu, menu for navigation,menu for opening dialog or another menu, menu for filter, sliders, switches, dialog, link, form,rating, filter).
    If element is used to input/enter data, then determine all the condition of that element which to make make the input valid and the conditions that would render it invalid base on the description of the use case specification. Do not arbitrarily create additional conditions that not mention in the use case flow.
    If element is used to select a value, then determine all the value of the element. Do not determine any values that haven't already been mentioned in the use case.

    Try not to generate duplicate element. 
    Return the element extracted in json format.
    The JSON format should follow the following structure:
    {"Name of interactive element": {"condition": "condition of that element", "value": "value of that element", "type": "element type"}}
    Examples of output json format template: 
    {"Username": {"condition": {"valid": "must be over 8 characters and below 30 characters", "invalid": "below 8 characters or over 30 character"}, "value": [], "type": "text field"}}
    {"Search button": {"condition": {"valid": "", "invalid": ""}, "value": [], "type": "button"}}
    """

    #có nên đổi cái code lọc fliter_data không????


    # In[1510]:


    promptExtractCondtition = [
        { "role": "system", "content": SYSTEM_PROMPT_extract_condition},
        { "role": "user", "content": str(usecase_flow) }
    ]
    gpt_response = ask(promptExtractCondtition, client, model)
    print(gpt_response)
    full_elements = json.loads(gpt_response)


    filter_element_select_value = {key: value for key, value in full_elements.items() 
                                if ( value['value'] and value['type'] not in ['button','menu for navigation',' menu for opening dialog or another dropdown',  'tab', 'card','link','icon','title','dialog'])}


    # In[1515]:


    for key, value in filter_element_select_value.items():
        print(key)
        print(value)    


    # In[1516]:


    filter_element_enter_value = {key: value for key, value in full_elements.items() 
                                if (value['type'] in ['text field','text area'] and value['condition']['valid'] or value['condition']['invalid'] )}
    # value['type'] in ['text field','text area']


    # In[1517]:


    for key, value in filter_element_enter_value.items():
        print(key)
        print(value)    


    # In[1518]:


    SYSTEM_PROMPT_get_flow_name ="""
    Given use case flows of a feature and a list of interaction elements extracted from that use case flows.
    For each given interactive element:
    Identify the flow through which the element is interacted in the use case flow and the type of interaction has with the element and who make that interact.
    Ignore interactive elements not mentioned in the given list.
    Return the flows in json format.
    The JSON format should follow the following structure:
    {"Name of interactive element":[{"flow 1":[{"action":"interaction 1","by":"actor","at sentence":"sentence mention that interaction element"},{"action":"interaction 2","by":"actor","at sentence":"sentence mention that interaction element"}]}]}
    Examples of output json format template: 
    {"Username":[{"Alternative flow 1: Login by valid username":[{"action":"enter","by":"user","at sentence":"Step 4: user enter valid username that above 8 and below 10 characters"}]},{"Exception flow 1: Login by invalid username":[{"action":"fill","by":"user","at sentence":"Step 4: user enter invalid username below 8 characters"}]}]}
    {"Rating filter":[{"Alternative flow 1: User rating order":[{"action":"skip","by":"user","at sentence":"Step 3: user skip the rating filter select"},{"action":"select","by":"user","at sentence":"Step 10: user rate the order by select the number of star"}]}]}
    """


    # In[1519]:


    Element = "Element: "
    for key,value in filter_element_enter_value.items():
        # print(key)
        # print(value)
        Element += key+ " ,"
    for key,value in filter_element_select_value.items():
        # print(key)
        # print(value)
        Element += key+ " ,"
    Element = Element[:-2] 
    Element += "."
    print(Element)


    # In[1520]:


    print(Element + "\nUse case flow:" + str(usecase_flow)  )


    # In[1521]:


    if(len(filter_element_enter_value) != 0 or len(filter_element_select_value) !=0 ):
        promptExtractCondtition = [
        { "role": "system", "content": SYSTEM_PROMPT_get_flow_name},
        { "role": "user", "content":Element + "\nUse case flow:" + str(usecase_flow) }
        ]
        gpt_response = ask(promptExtractCondtition, client, model)
        print(gpt_response)
        element_actions_flow = json.loads(gpt_response)
        print(element_actions_flow)


    # In[1522]:


    non_actions = ['display','show']
    non_actors = ['system','System']


    # In[1523]:


    if(len(filter_element_enter_value) != 0 or len(filter_element_select_value) !=0  ):

        for flow_lists_log in element_actions_flow.values():
            for flow_list_element in flow_lists_log:
                flows_to_delete = []
                for flow_name, actions in flow_list_element.items():
                    filtered_actions = []
                    for action in actions:
                        if(default_flow in flow_name and 'At step' in action['at sentence'] ):
                            continue

                        if (action['action'] not in non_actions and action['by'] not in non_actors): 
                            filtered_actions.append(action)

                    flow_list_element[flow_name] = filtered_actions
                    if not filtered_actions:
                        flows_to_delete.append(flow_name)
                flows_to_delete = list(set(flows_to_delete))
                for flow_name in flows_to_delete:
                    del flow_list_element[flow_name]

        # Convert modified data back to JSON
        modified_json_content = json.dumps(element_actions_flow, indent=2)
        print(modified_json_content)
        element_flow = element_actions_flow.copy()


    # In[1524]:


    print(filter_element_select_value)
    print(filter_element_enter_value)
    filter_element_select_value_flow_list = []
    filter_element_enter_value_flow_list = []


    # In[1525]:


    if(len(filter_element_enter_value) != 0 or len(filter_element_select_value) !=0  ):
        print(element_flow)


    # In[1526]:


    if(len(filter_element_enter_value) != 0 or len(filter_element_select_value) !=0  ):
        for key in filter_element_select_value:
            if key in element_flow:
                for obj in element_flow[key]:
                    filter_element_select_value_flow_list.extend(obj.keys())

            else:
                print(f"No flow found for '{key}' in element_flow.")
        filter_element_select_value_flow_list = list(set(filter_element_select_value_flow_list))
        print(filter_element_select_value_flow_list)


    # In[1527]:


    if(len(filter_element_enter_value) != 0 or len(filter_element_select_value) !=0  ):
        for key in filter_element_enter_value:
            if key in element_flow:
                for obj in element_flow[key]:
                    filter_element_enter_value_flow_list.extend(obj.keys())

            else:
                print(f"No flow found for '{key}' in element_flow.")

        filter_element_enter_value_flow_list = list(set(filter_element_enter_value_flow_list))
        print(filter_element_enter_value_flow_list)


    # In[1528]:


    # flow with input value
    click_only_flow_name = flows_name.copy()
    print(flows_name)

    for key in flows_name:
        for key_check in filter_element_enter_value_flow_list:
            if (key in key_check or key_check in key) and key in click_only_flow_name:
                click_only_flow_name.remove(key)
            
    for key in flows_name:
        for key_check in filter_element_select_value_flow_list:
            if (key in key_check or key_check in key) and key in click_only_flow_name:
                click_only_flow_name.remove(key)
    print(click_only_flow_name)
    # click_only_flow_name = [key for key in flows_name if key not in filter_element_enter_value_flow_list]
    # click_only_flow_name = [key for key in click_only_flow_name if key not in filter_element_select_value_flow_list]



    # In[1529]:


    print(flows_name)
    print(filter_element_enter_value_flow_list)
    print(filter_element_select_value_flow_list)
    print(click_only_flow_name)


    # In[1530]:


    click_only_flows = {}

    for key,value in usecase_flow.items():
        if key in click_only_flow_name:
            click_only_flows[key] = value

    print("click_only_flows = " + str(click_only_flows))


    # In[1531]:


    input_flows = {}

    for key,value in usecase_flow.items():
        if key in filter_element_enter_value_flow_list:
            input_flows[key] = value

    print("input_flows = " + str(input_flows))
    print(input_flows.keys())


    # In[1532]:


    select_flows = {}

    for key,value in usecase_flow.items():
        if key in filter_element_select_value_flow_list:
            select_flows[key] = value

    print("select_flows = " + str(select_flows))


    # In[1533]:


    SYSTEM_PROMPT_gen_no_condition_test_scenarios ="""
    Given use case specification flows.
    Your task is to generate one test scenario only to test each given flow.
    Return the test scenarios generated in json format.
    The JSON format should follow the following structure:
    {
        "Test Scenarios":[ "name of test scenario"]
    }
    For example :
    {
    "Test Scenarios": [
        "Administrator Cancels Adding New Lesson Before Saving"
    ]
    }
    """


    # In[1534]:


    SYSTEM_PROMPT_gen_test_scenarios_input_element ="""
    Given a list of interaction element for input value and their extracted conditions and use case flows that reflect those element.
    Your task is to generate a comprehensive set of test scenarios that test all given the conditions of given elements.
    The test scenarios generated must have clear conditions descritions and mention conditions is tested but do not need example data. 
    The positive test scenarios generated must test the combination of valid elements (the combination follow the description in the use case flow). 
    The negative test scenarios generated must test only one given invalid condition at a time. If there is no invalid condition, you don't need to write negative test scenario.
    For cases where the invalid condition does not have a corresponding output description, predict the possible outcome to test.


    Do not generate test scenario to test element that not mention in the given element list.

    Return the test scenarios generated in json format.
    The JSON format should follow the following structure:
    {
    "Positive Test Scenarios": [{ "name of test scenario": {"conditions": conditions tested}}],
    "Negative Test Scenarios": [{ "name of test scenario": {"conditions": conditions tested}}]
    }

    An example of a test scenario: 
    {
    "Positive Test Scenarios": [{ "create a new account with valid email and valid passowrd.": {"conditions": login with email}}],
    "Negative Test Scenarios": [{" Lesson Creation with Missing Name": {"conditions": lesson name must be entered }}}]
    }
    """


    # In[1535]:


    SYSTEM_PROMPT_gen_test_scenarios_select_element ="""
    Given a list of element for selecting value, their value options and use case flows use given element.
    For each given element:
    Generate only one test scenario to test the selection for each element value options. 

    Do not generate test scenario to test the display of object.
    Do not generate test scenario to test element that not mention in the given element list.

    The JSON format should follow the following structure:
    {
        "Test Scenarios":[ "name of test scenario","name of test scenario"]
    }
    For example :
    {
    "Test Scenarios": [
        "create Book with Default Genre value and Default Share value.",
        "create Book with Genre value 'Adventural'."
    ]
    }
    """
    # Generate test scenarios to test the selection for each element's value.
    # Generate test scenarios for the condition invalid if element mentions.



    # In[1536]:


    all_test_scenario = []


    # In[1537]:


    if( len(click_only_flows)!= 0 ):
        promptExtractCondtition = [
        { "role": "system", "content": SYSTEM_PROMPT_gen_no_condition_test_scenarios},
        { "role": "user", "content": str(click_only_flows) }
    ]

        gpt_response = ask(promptExtractCondtition, client, model)
        print(gpt_response)
        temp = json.loads(gpt_response)["Test Scenarios"]
        all_test_scenario.extend(temp)

        


    # In[1538]:


    print("Element: "+str(filter_element_enter_value) +"\nUse case:" +str(input_flows) )


    # In[1539]:


    if( len(filter_element_enter_value)!= 0 ):
        promptExtractCondtition = [
        { "role": "system", "content": SYSTEM_PROMPT_gen_test_scenarios_input_element},
        { "role": "user", "content": "Element: "+str(filter_element_enter_value) +"\nUse case:" +str(input_flows)  }
    ]

        gpt_response = ask(promptExtractCondtition, client, model)
        data = json.loads(gpt_response)

        # Extract only the test scenario names
        all_scenario_names = []
        for scenario_type in data:
            for scenario in data[scenario_type]:
                scenario_desc = list(scenario.keys())[0]
                all_scenario_names.append(scenario_desc)

        print("All Test Scenario Names:")
        print(json.dumps(all_scenario_names, indent=2))
        all_test_scenario.extend(all_scenario_names)
        


    # In[1540]:


    if( len(filter_element_select_value)!= 0):
        promptExtractCondtition = [
        { "role": "system", "content": SYSTEM_PROMPT_gen_test_scenarios_select_element},
        { "role": "user", "content": str(select_flows) + "Element: "+str(filter_element_select_value) }
    ]

        gpt_response = ask(promptExtractCondtition, client, model)
        print(gpt_response)
        select_testscenario = json.loads(gpt_response)["Test Scenarios"]
        all_test_scenario.extend(select_testscenario)
        
    return all_test_scenario

def write_list_to_file(file_path, my_list):
    with open(file_path, 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)
def write_list_to_file_with_numbering(file_path, my_list):
    with open(file_path, 'w') as f:
        for i, item in enumerate(my_list, start=1):
            f.write(f"{i}. {item}\n")
file_path_list = [
"D:\GPT-testing\SpecificationData\ShopeeWeb\View detail information of a product.txt"]


#     r'D:\GPT-testing\SpecificationData\Adventura\Adventura - Filter.txt',
#     r'D:\GPT-testing\SpecificationData\Adventura\Adventura - view attraction.txt',
#     r'D:\GPT-testing\SpecificationData\Adventura\Adventura- Search Attraction.txt',
#     r'D:\GPT-testing\SpecificationData\Book(Github)\Add a new author.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Add a new book.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Add a new genre.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Display author details.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Display book details.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Display genre details.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Display the list of authors.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Display the list of books.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Display the list of genres.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Edit the author.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Edit the book.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Edit the genre.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Remove the author.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Remove the book.txt',
# r'D:\GPT-testing\SpecificationData\Book(Github)\Remove the genre.txt',
# r'D:\GPT-testing\SpecificationData\Film\Add a comment.txt',
# r'D:\GPT-testing\SpecificationData\Film\Watch a film.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Add Booking.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Add Employee.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Add Room.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Check in.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Check out.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Hotel Owner - Generate Reports.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Hotel Owner - Update Hotel Information.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\login.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Request Service.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Update Booking.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Update Employee.txt',
# r'D:\GPT-testing\SpecificationData\Hotel Management System\Update Room.txt',
# r'D:\GPT-testing\SpecificationData\LNLibrary\Bookmark.txt',
# r'D:\GPT-testing\SpecificationData\LNLibrary\Rating a book.txt',
# r'D:\GPT-testing\SpecificationData\LNLibrary\Read a chapter.txt',
# r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\AddQuestion .txt',
# r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Flashcard.txt',
# r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Handbook.txt',
# r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Login.txt',
# r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Registry.txt',
# r'D:\GPT-testing\SpecificationData\MatchaEnglishWebsite\Review test.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Add or remove item.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Buy Items.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Feedback.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Login.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Pay Bill.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Prepare Bill.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Register Customer.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Search items.txt',
# r'D:\GPT-testing\SpecificationData\OnlineShoppingSystem\Validate Customer.txt',
# r'D:\GPT-testing\SpecificationData\ShopeeWeb\Add a type of product into cart.txt',
# r'D:\GPT-testing\SpecificationData\ShopeeWeb\Buy product.txt',
# r'D:\GPT-testing\SpecificationData\ShopeeWeb\Edit personal shopping cart.txt',
# r'D:\GPT-testing\SpecificationData\ShopeeWeb\Rating a product.txt',
# r'D:\GPT-testing\SpecificationData\ShopeeWeb\Search feature.txt'

for i in file_path_list:
    file_path = i
    print(file_path)
    file_content = read_file_into_string(file_path)
    if( file_content in "None"):
        continue
    usecase = "Use case: "+ read_file_into_string(file_path)
    if usecase is not None:
        for count in range(1,3):
            all_test_scenario = gentestscenario(usecase)
            for i in (all_test_scenario):
                print(i)
            test_scenario_file_path = file_path.replace("SpecificationData", "ResultSet\\5.5\\Propse 1\\")
            directory, filename = os.path.split(test_scenario_file_path)
            name, extension = os.path.splitext(filename)
            new_filename = f"{name} - {count}{extension}"
            new_path = os.path.join(directory, new_filename)
            print(new_path)
            write_list_to_file_with_numbering(new_path,(all_test_scenario))