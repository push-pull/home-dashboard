from selenium import webdriver
import requests

url = 'https://www.att.com/olam/downloadUverseInternetUsage.myworld?downloadType=csv&billStatementID=RecentUnbilled&accountNumber=153017755'

browser = webdriver.Firefox()
browser.get(url)

# Login
browser.find_element_by_id('userID').send_keys('')
browser.find_element_by_id('password').send_keys('')
browser.find_element_by_id('btnPrimarySmall').click()

# Grab cookies
cookies = browser.get_cookies()

# Close browser
browser.close()

# Make a new request session
session = requests.Session()

# Set cookies
for cookie in cookies:
	session.cookies.set(cookie['name'], cookie['value'])

# Download file
response = session.get(url)

# Save it...?
