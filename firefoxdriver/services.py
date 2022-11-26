from time import sleep


def get_url(driver: object, ):
    sleep(1)
    stories_url = driver.current_url
    return driver.current_url
    get_url(driver=driver)


    