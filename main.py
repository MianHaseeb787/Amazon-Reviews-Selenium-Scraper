# import undetected_chromedriver as uc
import re
import time
from selenium.webdriver.common.by import By

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("/Users/mian/ScrapedData/CNF_sel/chromedriver")
driver = webdriver.Chrome(service=service)

# chromeOptions = uc.ChromeOptions()
# chromeOptions.headless = False

# driver = uc.Chrome(use_subprocess=True, options=chromeOptions)


driver.get("https://www.amazon.com/-/es/ap/signin?openid.pape.max_auth_age=3600&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fmyh%2Fhouseholds%3Flanguage%3Des&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&language=en_US&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")

time.sleep(20) 

email = driver.find_element(By.ID, "ap_email")

email.send_keys("mianhaseeb.ce@gmail.com")

driver.find_element(By.ID, "continue").click()

time.sleep(5)

password = driver.find_element(By.ID, "ap_password")



password.send_keys("gggg2001")

driver.find_element(By.ID, "signInSubmit").click()

time.sleep(10)


product_url = "https://www.amazon.de/product-reviews/B09JG7SXKR/ref=cm_cr_arp_d_viewopt_sr?pageNumber=1&filterByStar=all_stars&language=de_DE"


# "https://www.amazon.de/product-reviews/B07DLCC73F/ref=cm_cr_arp_d_viewopt_fmt?formatType=current_format&pageNumber=4&filterByStar=all_stars&language=de_DE&currency=EUR"
# reviews_rating = 5

driver.get(product_url)

time.sleep(10) 

reviews_list = []

def iterate_reviews():


    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.a-section.review.aok-relative')))

    # Once the elements are present, proceed to extract them
    review_elements = driver.find_elements(By.CSS_SELECTOR, '.a-section.review.aok-relative')
    # review_elements = driver.find_elements(By.CSS_SELECTOR, '.a-section.review.aok-relative')

    print(len(review_elements))


    for review_element in review_elements:

       
        author_name = review_element.find_element(By.CLASS_NAME, 'a-profile-name').text

         
        review_text = review_element.find_element(By.CLASS_NAME, 'review-text').text

          
        review_date = review_element.find_element(By.CSS_SELECTOR, '.review-date').text

        
        review_clr_size = review_element.find_element(By.CSS_SELECTOR, '.a-size-mini.a-color-secondary').text

        try:
       
            rating_element = review_element.find_element(By.CSS_SELECTOR, "*[data-hook*=review-star-rating]")

            
            rating_text = rating_element.get_attribute("innerHTML")
            

           
            rating_match = re.search(r"(\d+,*\d*) von \d+ Sternen", rating_text)

            if rating_match:
                rating = rating_match.group(1).replace(',', '.')  
            else:
                rating = None

        except Exception as e:
          rating = None

        
        

        review_data = {
            'Author': author_name,
            'Review': review_text,
            'ReviewDate': review_date,
            'Ratings': rating,
            'ReviewClr': review_clr_size
        }

        print(review_data)

        reviews_list.append(review_data)
      

    time.sleep(5)


time.sleep(10)
iterate_reviews()

time.sleep(3)




for i in range(2, 3):

    next_page_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last'))
    )
               
    next_page_button.click()
    time.sleep(4) 
    iterate_reviews()


   

with open("6th-34-ProductReviews-dropper insert bottle - small clear glass bottle pharmacy jar set with black dropper insert cap", "w", newline="") as csvfile:
    
    fieldnames = ["Author", "Review", "ReviewDate", "Ratings", "ReviewClr"]
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    
    writer.writeheader()
    
    for row in reviews_list:
        writer.writerow(row)







driver.close()
