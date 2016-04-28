# Copyright (c) 2016 {UPRC}.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the The MIT License (MIT).
# which accompanies this distribution, and is available at
# http://opensource.org/licenses/MIT
# Contributors:
# {Constantinos Patsakis} {UPRC}
# Initially developed in the context of OPERANDO EU project www.operando.eu

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask
app = Flask(__name__)
driver = webdriver.Firefox()
Config = ConfigParser.ConfigParser()
Config.read("credentials.ini")

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
    time.sleep(2)
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
    time.sleep(1)
    driver.find_element_by_id("Passwd").send_keys(pwd)
    driver.find_element_by_id("signIn").click()

    # get the privacy settings page
    driver.get("https://myaccount.google.com/privacy?pli=1")
    settings = driver.find_element_by_xpath("//div[contains(@class, 'lc-mc')]")
    return settings.text


@app.route("/")
def get_privacy_seetings():
	f_res = fb(driver, Config.get("facebook", "user"),
	           Config.get("facebook", "password"))
	g_res = google(driver, Config.get("google", "user"),
	               Config.get("google", "password"))
	t_res = twitter(driver, Config.get("twitter", "user"),
        Config.get("twitter", "password"))
	l_res = linkedin(driver, Config.get("linkedin", "user"),
         Config.get("linkedin", "password"))
	ret_value="{1:'"+f_res+"',"
	ret_value+="2:'"+g_res+"',"
	ret_value+="3:'"+t_res+"',"
	ret_value+="4:'"+l_res+"'}"
	return ret_value

if __name__ == "__main__":
	app.run(debug=True)