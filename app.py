#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask
import atexit
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

user_agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36")

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = user_agent
driver = webdriver.PhantomJS(desired_capabilities=dcap)

app = Flask(__name__)

Config = ConfigParser.ConfigParser()
Config.read("credentials.ini")

def bye():
    driver.quit()

def save2file(name, content):
    fout = open(name, "w")
    fout.write(content.encode('utf8'))
    fout.close


def linkedin(driver, uname, pwd):
    # login to linkedin
    driver.get("http://linkedin.com/uas/login")
    emailelement = driver.find_element_by_id("session_key-login")
    passwordelement = driver.find_element_by_id("session_password-login")
    emailelement.send_keys(uname)
    passwordelement.send_keys(pwd)
    passwordelement.submit()
    sleep(2)
    driver.get("https://www.linkedin.com/psettings/")
    settings = driver.find_element_by_xpath(
        "//div[contains(@class, 'settings-grid')]").text
    return settings


def twitter(driver, uname, pwd):
    # login to twitter
    driver.get("http://twitter.com/login")
    emailelement = driver.find_element_by_xpath(
        "//div[@class='signin-wrapper']//input[@name='session[username_or_email]']")
    passwordelement = driver.find_element_by_xpath(
        "//div[@class='signin-wrapper']//input[@name='session[password]']")
    emailelement.send_keys(uname)
    passwordelement.send_keys(pwd)
    passwordelement.submit()

    # get the security & privacy settings
    driver.get("https://twitter.com/settings/security")
    settings = driver.find_element_by_xpath(
        "//div[contains(@class, 'content-main')]").text
    return settings


def fb(driver, uname, pwd):
    # login to facebook
    driver.get("https://facebook.com")
    login = "loginbutton"
    emailelement = driver.find_element_by_name("email")
    passwordelement = driver.find_element_by_name("pass")
    emailelement.send_keys(uname)
    passwordelement.send_keys(pwd)
    loginelement = driver.find_element_by_id(login)
    loginelement.click()

    # get the privacy page
    driver.get("https://www.facebook.com/settings?tab=privacy")
    settings = driver.find_element_by_id('contentArea').text
    return settings


def google(driver, uname, pwd):

    # login to google
    url = 'https://accounts.google.com/Login'
    driver.get(url)

    driver.find_element_by_id("Email").send_keys(uname)
    driver.find_element_by_id("next").click()
    # needs to sleep otherwise it will not find the element
    sleep(1)
    driver.find_element_by_id("Passwd").send_keys(pwd)
    driver.find_element_by_id("signIn").click()

    # get the privacy page
    driver.get("https://myaccount.google.com/privacy?pli=1")
    settings = driver.find_element_by_xpath("//div[contains(@class, 'lc-mc')]")
    return settings.text

def googlePT(driver):
    url = 'https://www.google.com/policies/privacy/'
    driver.get(url)
    terms = driver.find_element_by_xpath("//div[contains(@class, 'maia-article')]").text
    return terms

def InstagramPT(driver):
    url = 'http://instagram.com/legal/privacy/'
    driver.get(url)
    terms = driver.find_element_by_id('hc2content').text
    return terms

def TwitterPT(driver):
    url = 'https://twitter.com/privacy?lang=en'
    driver.get(url)
    terms = driver.find_element_by_xpath("//div[contains(@class, 'UserPolicy-content')]").text
    return terms

def LinkedInPT(driver):
    url = 'https://www.linkedin.com/legal/privacy-policy'
    driver.get(url)
    terms = driver.find_element_by_xpath("//div[contains(@class, 'legal')]").text
    return terms

def FBPT(driver):
    url = 'https://www.facebook.com/legal/terms/update'
    driver.get(url)
    terms = driver.find_element_by_id('content').text
    return terms


@app.route("/GetPrivacyTerms", methods=['GET'])
def GetPrivacyTerms():
    res = {}
    res['fb'] = FBPT(driver)
    res['g'] = googlePT(driver)
    res['tw'] = TwitterPT(driver)
    res['l'] = LinkedInPT(driver)
    res['i'] = InstagramPT(driver)

    json_data = json.dumps(res)
    return str(json_data)

@app.route("/OSPSettings", methods=['GET'])
def GetGlobalSettings():
    res={}
    res['fb'] = fb(driver, Config.get("facebook", "user"),Config.get("facebook", "password"))
    res['g'] = google(driver, Config.get("google", "user"),Config.get("google", "password"))
    res['tw'] = twitter(driver, Config.get("twitter", "user"),Config.get("twitter", "password"))
    res['l'] = linkedin(driver, Config.get("linkedin", "user"),Config.get("linkedin", "password"))

    json_data = json.dumps(res)
    return str(json_data)

if __name__ == "__main__":
    app.run(debug=True)
    atexit.register(bye)
