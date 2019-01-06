import requests
import mechanicalsoup
import sys
from bs4 import BeautifulSoup
import re
import getpass
from prettytable import PrettyTable
import os
import time

global list1
list1=[]
global li
li=[]
global list2
list2=[]
global optionsvalue
optionsvalue=[]
global inp
global headers
global lang_inp
global user

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

browser=mechanicalsoup.StatefulBrowser()

def submit(lang_inp,inp):
        print()
        print()
        print("ENTER THE FILE PATH IN THE FORMAT:- C:\\Users\\Admin\\Desktop\\filename")
        filepath=input("ENTER THE FILE PATH:- ")
        if os.path.exists(filepath):
                    submitlink="https://www.spoj.com/submit/"
                    submitlink=submitlink+inp
                    browser.open(submitlink)
                    browser.select_form('form[id="submit_form"]')
                    browser["file"]=open(filepath,'r').read()
                    browser["lang"] =lang_inp
                    browser.submit_selected()
                    #print(browser.get_url())

                    print("SUCCESSFULLY SUBMITTED YOUR SOLUTION!!")
                    print("Please Wait for 10 seconds till SPOJ judges your solution!!")
                    time.sleep(10);
                    reslink="https://www.spoj.com/status/"
                    reslink+=user
                    result=browser.get(reslink,headers=headers)
                    soup=BeautifulSoup(result.content,'lxml')
                    print()
                    val=soup.find('input',id="max_id")['value']
                    val1=soup.find('table',class_="problems table newstatus")
                    val2=val1.find('tbody')
                    val11=val2.find('tr')
                    a=[]

                    for i in val11.find_all('td'):
                        if(len(i)!=0):
                            string=i.get_text().strip()
                            string=re.sub(r"[\t\xa0]*", "", string)
                            a.append(string)

                    t=PrettyTable(['Id','Name','Result','Time','Space','Language'])
                    t.add_row([a[0],a[3],a[4],a[5],a[6],a[7]])
    
                    print(t)
                    print()
                    choice=(input("Press 1:- for Submitting Again\n 2:- for Submitting Another Problem\n 3:- Exit\n"))
                    if((int)(choice)==1):
                        langinp(optionsvalue,inp)
                    elif((int)(choice)==2):
                        problemcode(list1)
                    else:
                        exit()

        else:
            print()
            print("Wrong Path name!!")
            print("Try Again!!")
            submit(lang_inp,inp)


def langinp(optionsvalue,inp):
    lang_inp=input("ENTER YOUR PREFERRABLE LANGUAGE CODE:- ")
    if(lang_inp in optionsvalue):
            submit(lang_inp,inp)
    else:
            print()
            print("NO SUCH LANGUAGE EXISTS!!")
            print("TRY ANOTHER ONE!!")
            langinp(optionsvalue,inp)
            print()
            print()


def language(inp):
            with requests.Session() as s:
                    probcode="https://www.spoj.com/submit/"
                    probcode=probcode+inp
                    r4=s.get(probcode,headers=headers)
                    soup=BeautifulSoup(r4.content,'lxml')
                    #print(soup)
                    print()
                    print()
                    print("LANGUAGES AVAILABLE FOR THE PROBLEM")
                    print()
                    print()
                    langlist=[]
                    t1=PrettyTable(['LANGUAGE','VALUE'])
                    for option in soup.find_all('option'):
                        langlist.append(option['value'])
                        t1.add_row([option.text,option['value']])
                        optionsvalue.append(option['value'])
                    print(t1)
                    print()
                    print()
                    langinp(optionsvalue,inp)


def problemcode(list1):
        with requests.Session() as s:
            k=0
            pos=0
            inp=input("Enter The Problem Code That You Want To Solve:- ")
            for i in list1:
                if(i[10:]==inp):
                    pos=k
                    k=0
                    break
                else:
                    k=k+1
            #print(pos)
            if(k==0):
                print("Your Problem Code Is:-",inp)
                strk="https://www.spoj.com"
                strk=strk+list1[pos]
                print("Your Problem Name Is:-",li[pos])
                print("Your Problem Link Is:-",strk)
                print()
                print()

                r3=s.get(strk,headers=headers)
                soup=BeautifulSoup(r3.content,'lxml')
                print("                    PROBLEM STATEMENT")
                print(soup.find('div',id='problem-body').text)
                print()
                yesno=input("Want To Submit The Solution Enter YES or NO:- ")
                if(yesno=="YES"):
                    language(inp)
                
                else:
                    print()
                    problemcode(list1)
                    print()  

            else:
                print()
                print()
                print("Wrong Probelm Code!!")
                print("Try Again!!")
                print()
                print()
                problemcode(list1)


def problems(url1):
            with requests.Session() as s:
                r1=s.get(url1,headers=headers)
                soup=BeautifulSoup(r1.content,'lxml')
                #print(soup.prettify())
                
                for question in soup.find_all('td',align='left'):
                    list1.append(question.a.get("href"))
                    li.append(question.a.text)
                k=0
                t=PrettyTable(['PROBLEM NAME','PROBLEM CODE'])
                for prob in li:
                    strl=list1[k]
                    t.add_row([li[k],strl[10:]])
                    k=k+1
                print(t)
                #print(list1)
                problemcode(list1)


def details(soup):
    url="https://www.spoj.com/status/"
    brow=browser.get(url,headers=headers)
    soup=BeautifulSoup(brow.content,'lxml')
    soup1=soup.find('tbody')
    table=PrettyTable(['ID','USER','PROBLEM','RESULT','TIME','LANG'])
    a=[]
    for i in soup1.find_all('tr'):
        for j in i.find_all('td'):
            if(len(j.get_text())!=0):
                string=j.get_text().strip()
                string=re.sub(r"[\t\xa0]*", "", string)
                a.append(string)
        table.add_row([a[0],a[2],a[3],a[4],a[5],a[7]])
        a=[]
    print(table)
    print()
    want=(int)(input("Enter 1 for going to the HomePage:- "))
    if(want==1):
        homepage(soup)
    else:
        exit()


def homepage(soup):
        a1=soup.find_all('a',href='/problems')
        a2=soup.find_all('a',href='/status')
        a3=soup.find_all('a',href='/contests')

        status=input("Enter:-\n 1- Problems\n 2- Status\n 3- Exit\n")
        url2='https://www.spoj.com/problems/classical'
        if(status=='1'):
            s2=input("Enter:-\n 1- Classical\n 2- Challenge\n 3- Partial\n 4- Tutorial\n 5- Riddle\n 6- Basics\n")
            if(s2=='1'):
                url1='https://www.spoj.com/problems/classical'
            elif(s2=='2'):
                url1='https://www.spoj.com/problems/challenge'
            elif(s2=='3'):
                url1='https://www.spoj.com/problems/partial'
            elif(s2=='4'):
                url1='https://www.spoj.com/problems/tutorial'
            elif(s2=='5'):
                url1='https://www.spoj.com/problems/riddle'
            elif(s2=='6'):
                url1='https://www.spoj.com/problems/basics'
            problems(url1)
        elif(status=='2'):
            details(soup)
        else:
            exit()


def login():

    user=input("Enter Your Spoj Username:- ")
    pas=getpass.getpass()     #get password without displaying

    browser.open("https://www.spoj.com/login")
    browser.select_form('form[id="login-form"]')
    browser["login_user"]=user
    browser["password"]=pas
    browser.submit_selected()
    with requests.Session() as s:
        url='https://www.spoj.com/'
        r1=browser.get("https://www.spoj.com/myaccount/",headers=headers)
        soup=BeautifulSoup(r1.content,'lxml')
        #print(soup)
        html=r1.text
        #print(html)
        html.encode('utf-8')
        if(user in html):
            print("Successfully Logged In!!")
            homepage(soup)
        else:
            print ('Authentication Failed!')
            print("Try Again!!")
            login()
login()

