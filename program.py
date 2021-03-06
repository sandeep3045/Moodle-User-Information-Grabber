from selenium import webdriver
import sqlite3

conn = sqlite3.connect('moodledata.db')
print("Database Connection Ok")

# Get All The Necessary Information From User
print("\n ==== [ Welcome To MOODLE Information Grabber ] ===\n")

login_url = input("(Step 1 of 5) Enter Url Of MoLogin Page : ")

username    = input("(Step 2 of 5) Username : ")
password    = input("(Step 3 of 5) Password : ")

initial_id = int(input('(Step 4 of 5) Enter The Starting Profile Id : '))
final_id = int(input('(Step 5 of 5) Enter The Terminating Profile Id : '))

print("Entry Done ...")

# Open Browser And Load Url
driver = webdriver.Chrome()
driver.get(login_url)

# Login To Moodle
driver.find_element_by_xpath("//input[@id='username']").send_keys(username)
driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
driver.find_element_by_xpath("//button[@id='loginbtn']").click()

# Start Data Grabbing
for i in range(initial_id,final_id):
    driver.get('http://moodlebppimt.ddns.net/user/profile.php?id='+str(i))

    #Get Web Element From WebPage
    try:
        html_list = driver.find_element_by_xpath("//section[@id='region-main']//section[1]//ul[1]")
        name = driver.find_element_by_xpath("//div[@class='page-header-headings']").text
    except:
        continue

    #Initialize Dictionary
    user_details = {
        "Id":i,
        "Name":name,
        "Email address":"", 
        "InstituteName":"", 
        "DepartmentOfCollege":"", 
        "Association":"", 
        "CollegeID / CollegeRoll":"", 
        "UniversityRoll":"", 
        "UniversityRegnNo":"", 
        "YearOfAssociation":"", 
        "SemesterAssociated":"", 
        "SectionAssociated":"", 
        "GroupAssociated":"", 
        "ContactMobile":""
    }

    #Get List Items
    items = html_list.find_elements_by_tag_name("li")
    for item in items:
        try:
            key = item.find_elements_by_tag_name("dt")[0].text
            val = item.find_elements_by_tag_name("dd")[0].text
            user_details[key]=val
        except:
            continue
            
    #Commit to Sqlite DB and display Total Progress 
    sql_query = "INSERT INTO users (Id,Name,Email,InstituteName,DepartmentOfCollege,Association,CollegeID_CollegeRoll,UniversityRoll,UniversityRegnNo,YearOfAssociation,SectionAssociated,GroupAssociated,ContactMobile) VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(user_details['Id'], user_details['Name'], user_details['Email address'], user_details['InstituteName'], user_details['DepartmentOfCollege'], user_details['Association'], user_details['CollegeID / CollegeRoll'], user_details['UniversityRoll'], user_details['UniversityRegnNo'], user_details['YearOfAssociation'], user_details['SectionAssociated'], user_details['GroupAssociated'], user_details['ContactMobile'])    
    conn.execute(sql_query)
    conn.commit()
  
    print("{} Of {} Done".format(i,final_id))

    i=i+1
    
conn.close()