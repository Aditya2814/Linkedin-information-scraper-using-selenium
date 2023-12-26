from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

input_url = input("Enter person's Linkedin URL: ")
email = input("Enter your Email ID registered with Linkedin: ")
pw = input("Enter your Password for linkedin: ")

driver = webdriver.Chrome(options=options)

driver.get("https://www.linkedin.com/")

time.sleep(1)

username = driver.find_element(By.ID, "session_key")
password = driver.find_element(By.ID, "session_password")

username.send_keys(email)
password.send_keys(pw)
password.send_keys(Keys.RETURN)

linkedin_profile_data = {}

driver.get(input_url)

profile_image = driver.find_element(By.CLASS_NAME, "EntityPhoto-circle-9 img")
img_url = profile_image.get_attribute("src")
linkedin_profile_data["profile_picture_url"] = img_url

name_element = driver.find_element(By.CLASS_NAME, "text-heading-xlarge")
name = name_element.text
linkedin_profile_data["name"] = name

about_element = driver.find_element(By.CLASS_NAME, "inline-show-more-text > span")
about = about_element.text
linkedin_profile_data["about"] = about

connections_element = driver.find_element(By.CLASS_NAME, "pvs-header__title-container > p > span")
connections = connections_element.text
linkedin_profile_data["connections"] = connections

linkedin_profile_data["institutes"] = []
institute_element = driver.find_elements(By.XPATH, "//section[div[@id='education']]/div/ul/li/div/div/div/a/div/div/div/div/span[@aria-hidden='true']")
for institute in institute_element:
    linkedin_profile_data["institutes"].append(institute.text)

linkedin_profile_data["degrees"] = []
degrees_element = driver.find_elements(By.XPATH, "//section[div[@id='education']]/div/ul/li/div/div/div/a/span[@class='t-14 t-normal']/span[@aria-hidden='true']")
for degree in degrees_element:
    linkedin_profile_data["degrees"].append(degree.text)

linkedin_profile_data["dates"] = []
dates_element = driver.find_elements(By.XPATH, "//section[div[@id='education']]/div/ul/li/div/div/div/a/span[@class='t-14 t-normal t-black--light']/span[@aria-hidden='true']")
for date in dates_element:
    linkedin_profile_data["dates"].append(date.text)

linkedin_profile_data["education"] = []
for iter in range(len(linkedin_profile_data["institutes"])):
    List = [linkedin_profile_data["institutes"][iter], linkedin_profile_data["degrees"][iter], linkedin_profile_data["dates"][iter]]
    linkedin_profile_data["education"].append(List)

del linkedin_profile_data["institutes"]
del linkedin_profile_data["degrees"]
del linkedin_profile_data["dates"]

driver.get(input_url+"details/skills/")

linkedin_profile_data["skills"] = []
skills_element = driver.find_elements(By.XPATH, "//div[@class='pvs-list__container']/div/div/ul/li/div/div/div/div/a//span[@aria-hidden='true']")
for skill in skills_element:
    linkedin_profile_data["skills"].append(skill.text)

# Saving the JSON file
output_file = "linkedin_profile_data.json"
with open(output_file, "w") as json_file:
    json.dump(linkedin_profile_data, json_file, indent=4)

print(f"LinkedIn profile data saved to {output_file}")
