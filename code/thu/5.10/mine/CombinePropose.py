#!/usr/bin/env python
# coding: utf-8

# In[12]:


from openai import OpenAI
import json
import os

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
    )

    return response.choices[0].message.content

def askJSON(prompt, client, model, temperature = 0):
    response = None
    
    response = client.chat.completions.create(
      model=model,
      messages=prompt,
      temperature=temperature,
      response_format={ "type": "json_object" },
    )

    return response.choices[0].message.content


# In[13]:


#Prompt
MAIN_FLOW_SYSTEM_PROMPT="""
I want you to act as software tester.
Your task is to read this information about one main flow of a use case.
Then you predict all scenarios that can happen in this flow.

Rules to predict scenarios:
- Stay close to the details described in the flow.
- Choose important cases to generate, important scenario is the scenario that users are more likely to encounter it.
- Limit the appearance of scenarios that are hard to happen. 
- A scenario encompasses a whole function, not just verifying individual steps.
- If there is no other action in the flow beside clicking or there is no condition to vary the user's actions, that flow has one scenario only.
- A scenario often refers to a specific sequence of events or user actions that could potentially lead to a change in how the application behaves or responds.
- Test scenarios should be derived from cohesive sequences of steps that represent meaningful user interactions, rather than isolated steps.
- A scenario should cover from the first step to the final step in the flow, the start or the result of the scenario could be different.
- You cannot separate parts of a flow to be a scenario (Example: predict multiple scenarios for a flow by dividing steps into parts) because each scenarios should be independent and require a complete flow to proceed.
I only need scenarios's name for the output, I do not need the steps to go with it.
"""

SUB_FLOW_SYSTEM_PROMPT="""
I want you to act as software tester.
Your task is to read this information about one main flow and one alternative or exception flow of a use case.
Then you predict all scenarios that can lead user from the main flow to change to the alternative or exception flow mentioned for creating test cases.

Rules to predict scenarios:
- A scenario encompasses a whole function, not just verifying individual steps.
- If there is no other action in the flow beside clicking or there is no condition to vary the user's actions, that flow has one scenario only.
- A scenario often refers to a specific sequence of events or user actions that could potentially lead to a change in how the application behaves or responds.
- Test scenarios should be derived from cohesive sequences of steps that represent meaningful user interactions, rather than isolated steps.
- A scenario should cover from the first step to the final step in the flow, the start or the result of the scenario could be different.
- You cannot separate parts of a flow to be a scenario (Example: predict multiple scenarios for a flow by dividing steps into parts) because each scenarios should be independent and require a complete flow to proceed.
- Do not generate scenarios with user analysis. (Example: User accidentally do A and user intentionally do A is the same scenario, so do not consider about "accidentally" or "intentionally" in scenario)
- Do not choose another option that is not chosen by the flow, eventhough it is mentioned (Example: A pop up with OK and Cancel, the flow only has step choose OK. Do not generate scenario that press Cancel)
- Do not generate scenario to test only the main flow.
I only need scenarios's name for the output, I do not need the steps to go with it.
"""

EXTRACT_CONDITION_SYSTEM_PROMPT="""
Given use case flows of a feature.
Your task is to identify all the interactive elements within the feature. 
For each interactive element:
Identify what type of that element (button,buttons, icon,scroll, text field,text area, tab, radio buttons, menu, combobox, sliders, switches, dialog, link, form,rating, filter).
Identify all the conditions mentioned in the use case of that element that would make the element valid and the conditions that would make the element invalid based on the description of the use case flow.
Do not arbitrarily create additional conditions that not mention in the use case flow.

Return the element extracted in json format.
The JSON format should follow the following structure:
{"Name of interactive element": {"condition": {valid:"conditions that make element valid", invalid: "conditions that make element invalid"}, "type": "element type"}}
Examples of output json format template: 
{"Username": {"condition": {"valid": "must be over 8 characters and below 30 characters, must be entered", "invalid": "below 8 characters, over 30 character, empty"}, "type": "text field"}}
{"Search button": {"condition": {"valid": "", "invalid": ""}, "type": "text field"}}
"""

CHECK_CONDITION_AVAILABLE_PROMPT="""
You will be given a test scenario's list and a condition list written in JSON format related to the use case specification description.
Your task is to read and define which conditions are not tested and generate corresponding test scenario for the mentioned use case.
Return only the name list of the given test scenario combine with the test scenario you generated. 
"""

FILTER_SYSTEM_PROMPT="""
Your task is to read all of this scenarios generation from many sources.
Then you remove all the same copies because there are many duplicate scenarios in meanings inside the input.
Make sure every scenarios in the response is unique.
"""

# Identify what type of that element (button,buttons, icon,scroll, text field, radio buttons, menu, menu for navigation,menu for opening dialog or another menu, menu for filter, sliders, switches, dialog, link, form,rating, filter).


# In[14]:


main_flow_prompt="""
Step 1: User click button 'Create' on the navbar.
Step 2: system show up drop down with options button: Create board, start with a template, create workspace.
Step 3: user click create board.
Step 4: System show up dropdown with text field 'Board title', combo box 'Workspace', combo box 'Visibility', button 'Create' is disable, button 'Use template'. 'Board title' is required and the button 'Create' will be change to clickable when 'Board title' is filled . 'Workspace''s value default is your lastest open workspace, 'Workspace''s options are the user's created workspace . 'Visibility' value default is Workspace, 'Visibility' option is Private, Workspace, Public.
Step 5: User enter 'Board title'.
Step 6: User select 'Workspace' value.
Step 7: User select 'Visibility' value.
Step 8: The button 'Create' is clickable.
Step 9: User click 'Create' button.
Step 10: New board is created and the system redirect user to that new board.
"""

alt_prompt_1="""
main flow: 
Step 1: User click button 'Create' on the navbar.
Step 2: system show up drop down with options button: Create board, start with a template, create workspace.
Step 3: user click create board.
Step 4: System show up dropdown with text field 'Board title', combo box 'Workspace', combo box 'Visibility', button 'Create' is disable, button 'Use template'. 'Board title' is required and the button 'Create' will be change to clickable when 'Board title' is filled . 'Workspace''s value default is your lastest open workspace, 'Workspace''s options are the user's created workspace . 'Visibility' value default is Workspace, 'Visibility' option is Private, Workspace, Public.
Step 5: User enter 'Board title'.
Step 6: User select 'Workspace' value.
Step 7: User select 'Visibility' value.
Step 8: The button 'Create' is clickable.
Step 9: User click 'Create' button.
Step 10: New board is created and the system redirect user to that new board.

alternative flow 1: create boards with create button and template.
At step 3 of the basic flow: user click 'start with a template'
step 4: system display a list of template.
step 5: user click one of the template.
step 6: the system enter the board's name with the template's name. 
Go back to step 9 in the basic flow and continue with the steps from step 9.
"""

alt_prompt_2="""
main flow: 
Step 1: User click button 'Create' on the navbar.
Step 2: system show up drop down with options button: Create board, start with a template, create workspace.
Step 3: user click create board.
Step 4: System show up dropdown with text field 'Board title', combo box 'Workspace', combo box 'Visibility', button 'Create' is disable, button 'Use template'. 'Board title' is required and the button 'Create' will be change to clickable when 'Board title' is filled . 'Workspace''s value default is your lastest open workspace, 'Workspace''s options are the user's created workspace . 'Visibility' value default is Workspace, 'Visibility' option is Private, Workspace, Public.
Step 5: User enter 'Board title'.
Step 6: User select 'Workspace' value.
Step 7: User select 'Visibility' value.
Step 8: The button 'Create' is clickable.
Step 9: User click 'Create' button.
Step 10: New board is created and the system redirect user to that new board.

alternative flow 2: create new boards by template tab.
At step 1 of the basic flow: user click templates tab.
step 2: system display a list of template.
step 3: user click one of the template.
step 4: the system enter the board's name with the template's name. 
Go back to step 9 in the basic flow and continue with the steps from step 9.
"""

prompt_all="""
use case name: create boards
main flow: 
Step 1: User click button 'Create' on the navbar.
Step 2: system show up drop down with options button: Create board, start with a template, create workspace.
Step 3: user click create board.
Step 4: System show up dropdown with text field 'Board title', combo box 'Workspace', combo box 'Visibility', button 'Create' is disable, button 'Use template'. 'Board title' is required and the button 'Create' will be change to clickable when 'Board title' is filled . 'Workspace''s value default is your lastest open workspace, 'Workspace''s options are the user's created workspace . 'Visibility' value default is Workspace, 'Visibility' option is Private, Workspace, Public.
Step 5: User enter 'Board title'.
Step 6: User select 'Workspace' value.
Step 7: User select 'Visibility' value.
Step 8: The button 'Create' is clickable.
Step 9: User click 'Create' button.
Step 10: New board is created and the system redirect user to that new board.

alternative flow:
alternative flow 1: create boards with create button and template.
At step 3 of the basic flow: user click 'start with a template'
step 4: system display a list of template.
step 5: user click one of the template.
step 6: the system enter the board's name with the template's name. 
Go back to step 9 in the basic flow and continue with the steps from step 9.

alternative flow 2: create new boards by template tab.
At step 1 of the basic flow: user click templates tab.
step 2: system display a list of template.
step 3: user click one of the template.
step 4: the system enter the board's name with the template's name. 
Go back to step 9 in the basic flow and continue with the steps from step 9.
"""


# In[15]:


# promptMainScenario = [
#     { "role": "system", "content": MAIN_FLOW_SYSTEM_PROMPT},
#     { "role": "user", "content": main_flow_prompt}
#   ]
# main_gpt_response = ask(promptMainScenario, client, model)

# promptSubScenario1 = [
#     { "role": "system", "content": SUB_FLOW_SYSTEM_PROMPT},
#     { "role": "user", "content": alt_prompt_1}
#   ]
# sub1_gpt_response = ask(promptSubScenario1, client, model)

# promptSubScenario2 = [
#     { "role": "system", "content": SUB_FLOW_SYSTEM_PROMPT},
#     { "role": "user", "content": alt_prompt_2}
#   ]
# sub2_gpt_response = ask(promptSubScenario2, client, model)

# filtercontent = main_gpt_response + "/n" + sub1_gpt_response + "/n" + sub2_gpt_response



# In[16]:


promptExtractCondition = [
    { "role": "system", "content": EXTRACT_CONDITION_SYSTEM_PROMPT},
    { "role": "user", "content": prompt_all}
  ]
gpt_response = askJSON(promptExtractCondition, client, model)
print(gpt_response)


# In[17]:


full_elements = json.loads(gpt_response)
condition_element = {key: value for key, value in full_elements.items() 
                              if (value['type'] in ['text field','text area'] and (value['condition']['valid'] or value['condition']['invalid'] ))}
print(condition_element)


# In[18]:


for i,v in condition_element.items():
    print (i,v)


# In[19]:


# full_elements = json.loads(gpt_response)
# filter_element_select_value = {key: value for key, value in full_elements.items() 
#                              if ( value['value'] and value['type'] not in ['button','menu for navigation',' menu for opening dialog or another dropdown',  'tab', 'card','link','icon','title','dialog'])}
# filter_element_enter_value = {key: value for key, value in full_elements.items() 
#                               if (value['type'] in ['text field','text area'] and value['condition']['valid'] or value['condition']['invalid'] )}
# combined_json = filter_element_select_value.copy()
# combined_json.update(filter_element_enter_value)
# # value['type'] in ['text field','text area']


# In[20]:


# promptFinal = [
#     { "role": "system", "content": CHECK_CONDITION_AVAILABLE_PROMPT},
#     { "role": "user", "content": filter_gpt_response + '/n' + str(combined_json)}
#   ]
# final_gpt_response = ask(promptExtractCondition, client, model)
# print(final_gpt_response)


# In[21]:


# promptFilter = [
#     { "role": "system", "content": FILTER_SYSTEM_PROMPT},
#     { "role": "user", "content": filtercontent}
#   ]
# filter_gpt_response = ask(promptFilter, client, model)
# print(filter_gpt_response)

