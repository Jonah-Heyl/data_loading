import os
from dotenv import load_dotenv
from os import access, environ
import json

try:
    import requests
except:
    os.system("pip install requests")

class wt():
    def __init__(self,link,user='bob',password='1234',ref_token='NA',access_token='NA'):
        self.link=link
        self.user= user
        self.password=password
        self.ref_token=ref_token
        self.access_token=access_token

    @staticmethod
    def make_file(d1,d2):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = 'client_id=support_token_server&client_secret=4support_server2work&grant_type=password&username={}&password={}'

        # type your user details here
        user=d1
        password= d2
        data=data.format(user, password)

        response = requests.post('https://support.econjobmarket.org/oauth2/token', headers=headers, data=data)
        ref_token=response.json()['refresh_token']
    

        data = {
            'client_id': 'support_token_server',
            'client_secret': '4support_server2work',
            'grant_type': 'refresh_token',
            'refresh_token':ref_token,
        }

        response = requests.post('https://support.econjobmarket.org/oauth2/token', data=data)

        access_token= response.json()['access_token']
        
        #dict={'user':user,'password':password,'ref_token':ref_token,'access_token':access_token}

        with open ("user.env","w") as f:  
            f.write('user='+user+"\n")
            f.write('password='+password+"\n")
            f.write('ref_token='+ref_token+"\n")
            f.write('access_token='+access_token+"\n")


        return  access_token



        
    def file_y_n(self):
        try:
            load_dotenv("user.env")
            ref_token=os.getenv("ref_token")
            access_token=os.getenv("access_token")
            user=os.getenv("user")
            password=os.getenv("password")
                    

        except(FileNotFoundError):
            print("Create a file with your username and passowrd, useing makefile()")

        return wt(self.link,user,password,ref_token,access_token)

    
    
    def get_data(self):
        access_toke=self.access_token
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ access_toke,
        }

        response = requests.get(self.link, headers=headers) 
        
        slice=response.json()
 

        
        try:
            d=slice[0]
        except:
            return 0

        return slice

    def get_new_access_token(self):
        user=self.user
        password=self.password
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = 'client_id=support_token_server&client_secret=4support_server2work&grant_type=password&username={}&password={}'
        data=data.format(self.user, self.password)

        response = requests.post('https://support.econjobmarket.org/oauth2/token', headers=headers, data=data)

        ref_token=response.json()['refresh_token']

        data = {
            'client_id': 'support_token_server',
            'client_secret': '4support_server2work',
            'grant_type': 'refresh_token',
            'refresh_token':ref_token,
        }

        response = requests.post('https://support.econjobmarket.org/oauth2/token', data=data)
        
        try:
            access_token= response.json()['access_token']
            
        except(KeyError):
            return 2

        #dict={'user':user,'password':password,'ref_token':ref_token,'access_token':access_token}

        with open ("user.env","w") as f:  
            f.write('user='+user+"\n")
            f.write('password='+password+"\n")
            f.write('ref_token='+ref_token+"\n")
            f.write('access_token='+access_token+"\n")

        

        self.access_token =access_token
        self.ref_token =ref_token
       

    def run(self):
        slice=self.get_data()
        if slice==0:
            self.get_new_access_token()
            slice=self.get_data()
#,wt(self.link,self.user,self.password,self.ref_token,self.access_token)
        return slice

    @staticmethod
    def full_run(link):
        t=wt(link)
        t=t.file_y_n()
        data=t.run()
        return(data)


#best way:

#wt.make_file('user','password') # for first time use
#wt.full_run("https://support.econjobmarket.org/api/slice")



