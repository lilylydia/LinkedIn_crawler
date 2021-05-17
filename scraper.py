# Import libraries and packages for the project 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re
import csv
import datetime
from dateutil.parser import parse

print('- Finish importing packages')

# Task 1: Login to Linkedin

# Task 1.1: Open Chrome and Access Linkedin login site
driver = webdriver.Chrome()
sleep(2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Task 1.2: Import username and password
credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finish importing the login credentials')
sleep(2)

# Task 1.2: Key in login credentials
email_field = driver.find_element_by_id('username')
email_field.send_keys(username)
print('- Finish keying in email')
sleep(5)

password_field = driver.find_element_by_name('session_password')
password_field.send_keys(password)
print('- Finish keying in password')
sleep(2)

# Task 1.2: Click the Login button
#signin_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
sleep(3)
#signin_field.click()
sleep(3)

print('- Finish Task 1: Login to Linkedin')

# Task 2: Search for the profile we want to crawl
# Task 2.1: Locate the search bar element
search_field = driver.find_element_by_xpath('//*[@class="search-global-typeahead__input always-show-placeholder"]')
# Task 2.2: Input the search query to the search bar
#search_query = input('What profile do you want to scrape? ')
#search_field.send_keys(search_query)

# Task 2.3: Search
#search_field.send_keys(Keys.RETURN)

print('- Finish Task 2: Search for profiles')


# Task 3: Scrape the URLs of the profiles
# Task 3.1: Write a function to extract the URLs of one page
def GetURL():
    page_source = BeautifulSoup(driver.page_source,features="lxml")
    profiles = page_source.find_all('a', class_ = 'app-aware-link') #('a', class_ = 'search-result__result-link ember-view')
    all_profile_URL = []
    for profile in profiles:
        # profile_ID = profile.get('href')
        # profile_URL = "https://www.linkedin.com" + profile_ID
        profile_URL = profile.get('href')
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL


# # Task 3.2: Navigate through many page, and extract the profile URLs of each page
# input_page = int(input('How many pages you want to scrape: '))
# URLs_all_page = []
# # URLs_all_page = 'https://www.linkedin.com/in/zakaria-saoudi-mabrouk-a89789190/'
# for page in range(input_page):
#     URLs_one_page = GetURL()
#     sleep(2)
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
#     sleep(3)
#     next_button = driver.find_element_by_class_name("artdeco-pagination__button--next")
#     driver.execute_script("arguments[0].click();", next_button)
#     URLs_all_page = URLs_all_page + URLs_one_page
#     sleep(2) 

# print('- Finish Task 3: Scrape the URLs')


# # Task 4: Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
# with open('output.csv', 'w',  newline = '') as file_output:
#     headers = ['Name', 'Job Title', 'Location', 'NbrRelation', 'description', 'URL']
#     writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
#     writer.writeheader()
#     for linkedin_URL in URLs_all_page:
#         driver.get(linkedin_URL)
#         print('- Accessing profile: ', linkedin_URL)
#         sleep(3)
#         page_source = BeautifulSoup(driver.page_source, "html.parser")
#         #print('page_source: ',page_source)
#         info_div = page_source.find('div',{'class':'flex-1 mr5 pv-top-card__list-container'})
#         print('info_div: ',info_div)
#         description = page_source('div',{'class':'pv-oc ember-view'})
#         print('description: ',description)
#         try:
#             name = info_div.find('li', class_='inline t-24 t-black t-normal break-words').get_text().strip() #Remove unnecessary characters 
#             print('--- Profile name is: ', name)
#             location = info_div.find('li', class_='t-16 t-black t-normal inline-block').get_text().strip() #Remove unnecessary characters 
#             print('--- Profile location is: ', location)
#             NbRelation = info_div.find('span', class_='t-16 t-black t-normal').get_text().strip() #Remove unnecessary characters 
#             print('--- Nbr relations is: ', NbRelation)
#             title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
#             print('--- Profile title is: ', title)
#             description_detail = description.find('p',class_='pv-about__summary-text mt4 t-14 ember-view')
#             writer.writerow({headers[0]:name, headers[1]:location, headers[2]:title, headers[3]:NbRelation, headers[4]:description_detail, headers[5]:linkedin_URL})
#             print('\n')
#         except:
#             pass

# print('Mission Completed!')

# read data from csv file
URLs_all_page = []

with open('profile.csv','rt')as f:
    data = csv.reader(f)
    for row in data:
        URLs_all_page = URLs_all_page + row


# Task 5: Scrape one profile
with open('output.csv', 'w',  newline = '') as file_output:
    #headers = ['id','Name', 'Location', 'Job Title', 'NbrRelation','NbrExperProf','NbrFormations', 'NbrLicenceCertif', 'Experience']
    headers = ['id','entreprise','dateDeb','duree','attrition']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    employee_id = 0
    for linkedin_URL in URLs_all_page:
      
        #https://www.linkedin.com/in/ayushi-singh-b5ba4714b/
        #https://www.linkedin.com/in/zakaria-saoudi-mabrouk-a89789190/
        driver.get(linkedin_URL)
        print('- Accessing profile: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('div',{'class':'flex-1 mr5 pv-top-card__list-container'})
        # description = page_source.find('div',{'class':'pv-oc ember-view'})
        # print('description: ',description)
        nbr_exp_prof = 0
        Nbr_formations = 0
        Nbr_licence_form = 0 
        Experience = ''
                                                            
        career = page_source.find_all('div',{'class':'pv-profile-section-pager ember-view'})
       
        for index_career in career:   
              
            test = index_career.find('ul',{'class':'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more'})
            if test is None:
                test = index_career.find('ul',{'class':'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more'})
            person_experience = test.find_all('li',{'class':'pv-entity__position-group-pager pv-profile-section__list-item ember-view'})
            
            for index, index_exp in enumerate(person_experience, start=0):                                                
                
                 # search if there is ul in this li
                # grp = index_exp.find_all('ul',{'class':'pv-entity__position-group mt2'})
                # print('grp',grp)
                # if grp : 
                                                            
                entreprise = index_exp.find('div',{'class':'pv-entity__summary-info pv-entity__summary-info--background-section'})
                if entreprise is None :
                    entreprise = index_exp.find('div',{'class':'pv-entity__summary-info pv-entity__summary-info--background-section mb2'})                                  
                    # entreprise = index_exp.find('div',{'class':'pv-entity__summary-info pv-entity__summary-info--background-section'})
                    if entreprise:
                        print('je suis ici 1')  
                        entreprise_name = index_exp.find('p',{'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).find(text=True) 
                    else:
                        print('je suis ici 2')
                        entreprise_name = index_exp.find('span',{'class': None}).find(text=True) 
                else:
                    print('je suis ici 3')  
                    entreprise_name = index_exp.find('p',{'class':'pv-entity__secondary-title t-14 t-black t-normal'}).find(text=True)                                   

                #     print('entreprise_name',entreprise_name)
                # else:
                # print('je suis la')
               
                experiences_detail = index_exp.find('h4',{'class':'pv-entity__date-range t-14 t-black--light t-normal'})
                duree_emploi = index_exp.find('span',{'pv-entity__bullet-item-v2'})
                dates =  index_exp.find('h4',{'pv-entity__date-range t-14 t-black--light t-normal'})                                        
                date_deb = dates.find('span',{'class':None})
                
               
                date = date_deb.get_text().split(" ")
                if date[1] == '–':
                    date[1] = date[0] 
                    date[0] = 'Jan'
                
                if parse(date[0]+' '+date[1], fuzzy=False):
                    date_time_obj  = datetime.datetime.strptime(date[0]+' '+date[1], '%b %Y')
                print('Date:', date_time_obj.date())
                
                
                print('entreprise_name',entreprise_name.strip())
                nbr_exp_prof = nbr_exp_prof + 1
                word_list = experiences_detail.get_text().split() 
               
                if word_list[-1] == 'Present':
                    Experience = Experience + 'E'+ str(index) + '_' + '0'
                    attrition = '0'
                    #writer.writerow({headers[0]:employee_id, headers[1]:entreprise_name.strip(),headers[2]:date_time_obj,headers[3]:'0'}) 
                   
                else:
                    Experience = Experience + 'E'+ str(index) + '_' + '1' 
                    attrition = '1'
                    #writer.writerow({headers[0]:employee_id, headers[1]:entreprise_name.strip(),headers[2]:date_time_obj,headers[3]:'1'}) 
                test_duree_emploi = duree_emploi.get_text().split(" ") 
                print('test_duree_emploi',test_duree_emploi)
                res = [int(i) for i in  duree_emploi.get_text().split() if i.isdigit()]
                
                
                if len(res) == 2:
                    Experience = Experience + '_' + str(res[0]*12 + res[1]) + '#'
                    writer.writerow({headers[0]:employee_id, headers[1]:entreprise_name.strip(),headers[2]:date_time_obj,headers[3]:str(res[0]*12 + res[1]),headers[4]:attrition}) 
                
                else:
                    if len(res) == 0:
                        Experience = Experience + '_' + '1' + '#'
                        writer.writerow({headers[0]:employee_id, headers[1]:entreprise_name.strip(),headers[2]:date_time_obj,headers[4]:attrition}) 
                    else:
                        if test_duree_emploi[1] =='yrs':
                            print('annee est ', test_duree_emploi)
                            Experience = Experience + '_' + str(res[0]*12) + '#'
                            writer.writerow({headers[0]:employee_id, headers[1]:entreprise_name.strip(),headers[2]:date_time_obj,headers[3]:str(res[0]*12),headers[4]:attrition}) 
                        else: 
                            Experience = Experience + '_' + str(res[0]) + '#'
                            writer.writerow({headers[0]:employee_id, headers[1]:entreprise_name.strip(),headers[2]:date_time_obj,headers[3]:str(res[0]),headers[4]:attrition}) 
                            print('mois est ', res)
                        
                        
                #Experience = Experience + '_' +  date_deb
            # Educations
            all_school_name = index_career.find_all('h3',{'pv-entity__school-name t-16 t-black t-bold'})
            for school_name in all_school_name:
                Nbr_formations = Nbr_formations + 1;
                print('Nom de letablissament: ',school_name.get_text())
            print('nombre formations est: ',Nbr_formations)
            #Licence et certifications
            all_licence_certif = index_career.find_all('h3',{'t-16 t-bold'})
            for licence_certif in all_licence_certif:
                Nbr_licence_form = Nbr_licence_form + 1
                print('Licence & certification: ',licence_certif.get_text())
            print('Experience: ',Experience)
            print('nombre expérience est: ',nbr_exp_prof)

        try:
            name = info_div.find('li', class_='inline t-24 t-black t-normal break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile name is: ', name)
            location = info_div.find('li', class_='t-16 t-black t-normal inline-block').get_text().strip() #Remove unnecessary characters 
            print('--- Profile location is: ', location)
            #NbRelation = info_div.find('span', class_='t-16 t-black t-normal').get_text().strip() #Remove unnecessary characters 
            #NbRelation = re.findall(r'\b\d+\b', info_div.find('span', class_='t-16 t-black t-normal').get_text().strip())
            NbRelation = int(''.join(filter(str.isdigit, info_div.find('span', class_='t-16 t-black t-normal').get_text().strip())))
            print('--- Nbr relations is: ', NbRelation)
            title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
            print('--- Profile title is: ', title)
            #description_detail = description.find('p',class_='ember-view')
            #print('--- Profile description is: ',description_detail)
            
            #writer.writerow({headers[0]:index, headers[1]:name, headers[2]:location, headers[3]:title, headers[4]:NbRelation, headers[5]:nbr_exp_prof, headers[6]: Nbr_formations, headers[7]: Nbr_licence_form, headers[8]: Experience })
            print('\n')
        except:
            pass
        employee_id = employee_id + 1
    print('Mission Completed!')



