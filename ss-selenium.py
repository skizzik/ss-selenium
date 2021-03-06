import os, sys, getopt, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def login_url(username,password,url):
    width = 1024
    height = 768

    ###
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36")
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = user_agent
    serv_args = ["--disk-cache=false"]
    driver = webdriver.PhantomJS(desired_capabilities = dcap, service_args = serv_args)
    ### 
    
    driver.get(url)

    assert "Gmail" in driver.title

    #esto es el form del login
    filluser = driver.find_element_by_id('Email')    
    filluser.send_keys(username)

    nextButton = driver.find_element_by_id('next')
    nextButton.click()
    time.sleep(1)
    
    fillpass = driver.find_element_by_id('Passwd')
    fillpass.send_keys(password)

    submit = driver.find_element_by_id('signIn')
    submit.click()

    #do_snap
    driver.set_window_size(width, height) 
    
    timestr = time.strftime("%d%m%Y_%H%M%S")
    ssfile = 'ss_'+timestr+'.jpg'
    
    time.sleep(2)
    driver.save_screenshot(ssfile)
    print 'Archivo creado : '+ssfile
    driver.delete_all_cookies()
    driver.quit()

def main(argv):
    username = ''
    password = ''
    url = 'https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier'

    try:
        opts, args = getopt.getopt(argv,"hu:p:",["ifile=","ofile="])
        if len(dict(opts)) > 1:
            for opt, arg in opts:
                if opt == '-h':
                    print __file__+' -u <username> -p <password>'
                    sys.exit()
                elif opt in ("-u", "--user"):
                    username = arg
                elif opt in ("-p", "--pass"):
                    password = arg

            print 'Cargando..'
            login_url(username,password,url)

        else:
            print 'Error de sintaxis, faltan argumentos, para ayuda dale con '+__file__+' --h'
            pass

    except getopt.GetoptError:
        print __file__+' -u <user> -p <pass>'
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])