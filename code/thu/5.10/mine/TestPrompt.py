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
# Identify what type of that element (button,buttons, icon,scroll, text field, radio buttons, menu, menu for navigation,menu for opening dialog or another menu, menu for filter, sliders, switches, dialog, link, form,rating, filter).


# In[ ]:





# In[14]:


u


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

