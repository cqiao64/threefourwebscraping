from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time
import pandas as pd

# Function to clean up the names
def clean_name(name):
    name = name.replace(',', '')
    words = name.split()
    if len(words) > 2:
        words = words[:2]
    name = ' '.join(words)
    return name

# Dictionary to store names and IDs
name_id_dict = {}

# List to store names for which no ID was found
no_id_found = []

# Setup Edge driver
driver = webdriver.Edge(service=Service(r"PATH_TO_EDGE_DRIVER"))

# Go to your webpage
driver.get('WEBPAGE_URL')

# Wait for the page to load completely
driver.implicitly_wait(10)

# Find the dropdown menu button and click it
dropdown_button = driver.find_element(By.CSS_SELECTOR, 'DROPDOWN_BUTTON_SELECTOR')
dropdown_button.click()

# Wait for the dropdown menu to appear
time.sleep(2)

# Find the 'Facility' option and click it
dropdown_option = driver.find_element(By.XPATH, '//span[text()="Facility"]')
dropdown_option.click()

# Find the search box, clear it, and enter the ID
search_box = driver.find_element(By.CSS_SELECTOR, 'SEARCH_BOX_SELECTOR')
search_box.clear()
search_box.send_keys('SEARCH_ID')
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)

# Repeat dropdown click
dropdown_button = driver.find_element(By.CSS_SELECTOR, 'DROPDOWN_BUTTON_SELECTOR')
dropdown_button.click()

# Wait for the dropdown menu to appear
time.sleep(2)

# Find the 'Last name and First name' option and click it
dropdown_option = driver.find_element(By.XPATH, '//span[text()="Last name and First name"]')
dropdown_option.click()

# Wait for the dropdown to close
time.sleep(2)

# Read names from the file and clean them up
with open('PATH_TO_NAMES_FILE', 'r') as file:
    names = [clean_name(line.strip()) for line in file]

# Loop over the names
for cleaned_name in names:
    search_box = driver.find_element(By.CSS_SELECTOR, 'SEARCH_BOX_SELECTOR')
    search_box.clear()
    search_box.send_keys(cleaned_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    username_element = soup.find('span', class_='USERNAME_CLASS')

    if username_element:
        name_id_dict[cleaned_name] = username_element.text
    else:
        no_id_found.append(cleaned_name)

# Close the driver
driver.quit()

# Write names with no ID found to a text file
with open('PATH_TO_NO_ID_FOUND_FILE', 'w') as file:
    for name in no_id_found:
        file.write(name + '\n')

# Create a DataFrame from the dictionary
df = pd.DataFrame(list(name_id_dict.items()), columns=['Cleaned Name', 'ID'])

# Write the DataFrame to an Excel file using pandas
df.to_excel('OUTPUT_EXCEL_FILE', index=False)

# Print the dictionary and the list of names with no ID found
print(name_id_dict)
print(no_id_found)
