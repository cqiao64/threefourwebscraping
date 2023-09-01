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
    # Remove comma
    name = name.replace(',', '')
   
    # Split the name into words
    words = name.split()
   
    # If the name has more than two words, remove the third word
    if len(words) > 2:
        words = words[:2]
   
    # Join the words back together into one name
    name = ' '.join(words)
   
    return name

# Dictionary to store names and IDs
name_id_dict = {}

# List to store names for which no ID was found
no_id_found = []

# Setup Edge driver
driver = webdriver.Edge(service=Service(r"C:\Users\LPE4047\Desktop\msedgedriver.exe"))

# Go to your webpage
driver.get('https://esaf.hca.corpad.net/#/users')

# Wait for the page to load completely
driver.implicitly_wait(10)

# Find the dropdown menu button and click it
dropdown_button = driver.find_element(By.CSS_SELECTOR, 'button.icc-select-button')
dropdown_button.click()

# Wait for the dropdown menu to appear
time.sleep(2)  # Adjust the sleep time as needed

# Find the '3-4 ID' option and click it
dropdown_option = driver.find_element(By.XPATH, '//span[text()="Facility"]')
dropdown_option.click()

# Find the search box, clear it, and enter the ID '00144'
search_box = driver.find_element(By.CSS_SELECTOR, 'div.icc-searchbox.search-input input')
search_box.clear()
search_box.send_keys('00144')
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)  # Adjust the sleep time as needed

# Find the dropdown menu button again and click it
dropdown_button = driver.find_element(By.CSS_SELECTOR, 'button.icc-select-button')
dropdown_button.click()

# Wait for the dropdown menu to appear
time.sleep(2)  # Adjust the sleep time as needed

# Find the 'Last name and First name' option and click it
dropdown_option = driver.find_element(By.XPATH, '//span[text()="Last name and First name"]')
dropdown_option.click()

# Wait for the dropdown to close
time.sleep(2)  # Adjust the sleep time as needed

# Read names from the file and clean them up
with open('names.txt', 'r') as file:
    names = [clean_name(line.strip()) for line in file]

# Loop over the names
for cleaned_name in names:

    # Find the search box again, clear it, and enter the name
    search_box = driver.find_element(By.CSS_SELECTOR, 'div.icc-searchbox.search-input input')
    search_box.clear()
    search_box.send_keys(cleaned_name)
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to load
    time.sleep(5)  # Adjust the sleep time as needed

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the span element with the class 'username'
    username_element = soup.find('span', class_='username')

    # If the span element was found, store the username (text content) in the dictionary
    if username_element:
        name_id_dict[cleaned_name] = username_element.text
    else:
        no_id_found.append(cleaned_name)

# Close the driver
driver.quit()

# Write names with no ID found to a text file
with open('no_id_found.txt', 'w') as file:
    for name in no_id_found:
        file.write(name + '\n')

# Create a DataFrame from the dictionary
df = pd.DataFrame(list(name_id_dict.items()), columns=['Cleaned Name', 'ID'])

# Write the DataFrame to an Excel file using pandas
df.to_excel('name_id_dict.xlsx', index=False)

# Print the dictionary and the list of names with no ID found
print(name_id_dict)
print(no_id_found)
