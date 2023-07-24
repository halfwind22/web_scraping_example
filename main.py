import time
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium import webdriver

driver_path = 'C://Users//anaray01//Downloads//edgedriver//msedgedriver.exe'
service = Service(executable_path=driver_path, verbose=True, log_path="edgedriver.log")
options = Options()
options.headless = True
options.set_capability("user-agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
driver = webdriver.Edge(service=service, options=options, verbose=True)
driver.maximize_window()
driver.current_url
df_list = []
for i in range(1, 10):
    url = 'https://www.naukri.com/data-engineering-jobs-in-bangalore-bengaluru-' + str(i)
    print(url)
    driver.get(url=url)
    sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    try:
        results = soup.find(class_='list')
        if results is None or len(results) == 0:
            results = soup.find('listContainer fleft')

        job_elems = results.find_all('article', class_='jobTuple bgWhite br4 mb-8')
        print(f"No of elements in page {i} is {len(job_elems)}")

        iteration = 0
        for job_elem in job_elems:
            iteration += 1
            print(f"Currently in job listing {iteration} of page {i}")
            URL = job_elem.find('a', class_='title fw500 ellipsis').get('href')  # URL to apply for the job
            Title = job_elem.find('a', class_='title fw500 ellipsis')  # Post Title
            Company = job_elem.find('a', class_='subTitle ellipsis fleft')  # Company Name

            # Years of experience Required
            Exp = job_elem.find('li', class_='fleft grey-text br2 placeHolderLi experience')
            Exp_span = Exp.find('span', class_='ellipsis fleft fs12 lh16')
            if Exp_span is None:
                Experience = 'Not Available'
            else:
                Experience = Exp_span.text

            # Location for the job post
            Loc = job_elem.find('li', class_='fleft grey-text br2 placeHolderLi location')
            Loc_exp = Loc.find('span', class_='ellipsis fleft fs12 lh16')
            if Loc_exp is None:
                Experience = 'Not Available'
            else:
                Location = Loc_exp.text

            # Get salary
            salary_element = job_elem.find("li", "fleft grey-text br2 placeHolderLi salary")
            salary_value = salary_element.find("span", {"class": "ellipsis fleft fs12 lh16"}).text

            # Number of days since job posted
            Hist = job_elem.find("div", ["type br2 fleft grey", "type br2 fleft green"])
            Post_Hist = Hist.find('span', class_='fleft fw500')
            if Post_Hist is None:
                Post_History = 'Not Available'
            else:
                Post_History = Post_Hist.text

            Skills = [li.string for li in job_elem.find('ul', class_='tags has-description').findAll('li',
                                                                                                     class_='fleft fs12 grey-text lh16 dot')]  # Skills

            target_dict = {'Title': Title.text, 'Company': Company.text, 'Location': Location, 'Experience': Experience,
                           'Salary': salary_value, 'Skills': Skills, 'URL': URL, 'Job_Post_History': Post_History,
                           'Page': i}

            if target_dict is None:
                with open(f"error_{i}_{iteration}", "w+") as fp:
                    fp.write(results)
            else:
                pass

            # Appending data to the DataFrame
            df_list.append(target_dict)

    except AttributeError:
        driver.save_screenshot(driver.current_url[-1::] + ".png")
        sleep(10)
    except ValueError:
        print("Value Error")

# driver.close()
col_list = columns = ['Title', 'Company', 'Location', 'Experience', 'Salary', 'Skills', 'URL', 'Job_Post_History',
                      'Page']
pd.DataFrame(df_list, columns=col_list).to_csv('result.csv', index=False)
