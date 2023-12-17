import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re

#setup for web viewing
def get_driver(link):
    driver = webdriver.Safari()
    driver.get(link)
    
    content = driver.page_source
    
    soup = BeautifulSoup(content,'html.parser')
    driver.quit()
    return soup

#finding all the jobs and storing their info in dictionary
def scraping(page):
    jobs = page.find_all("div", class_="job_seen_beacon")
    for job in jobs:

        company_name = job.find("span", class_="css-1x7z1ps eu4oa1w0").text

        company_location = job.find("div", class_="css-t4u72d eu4oa1w0").text

        try:
            salary = job.find("div", class_="metadata salary-snippet-container").text
            cleaned_str = re.sub(r'[^\d$.,]', '', salary)
            list = cleaned_str.split('$')
            if(len(list)==2):
                min_salary = list[1]
                max_salary = "none"
            else:
                min_salary = list[1]
                max_salary = list[2]
        except:
            min_salary = "click link to find"
            max_salary = "click link to find"

        job_title = job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0").text

        link_tag = job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")
        link_half = link_tag["href"]
        base_url = "https://ca.indeed.com"
        full_url = f"{base_url}{link_half}"

        job_info = {
            "job_title" : job_title,
            "salary_min" : min_salary,
            "salary_max" : max_salary,
            "company_name" : company_name,
            "company_location" : company_location,
            "link" : full_url
        }
        job_list.append(job_info)
        
job_list = []

#put number of pages * 10 in place of the second int in for
for i in range(0,50,10):
    page_html = get_driver(f"https://ca.indeed.com/jobs?q=computer+science&l=Victoria%2C+BC&radius=50&start={i}&vjk=74df27615b32ca3c")
    scraping(page_html)

df = pd.DataFrame(job_list)
df.to_csv("jobs_indeed_computer_science.csv")


