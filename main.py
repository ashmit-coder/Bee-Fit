from flask import Flask 
from hashlib import sha512
import pandas as pd
import os,shutil,random
from flask import render_template ,request
app = Flask(__name__)



@app.route("/",methods =['GET','POST'])
def landing_page():
   
    return render_template("landing_page.html")
    

@app.route("/signuppage",methods=['GET','POST'])
def SignUp_page():
    username = ""
    password = ""
    if request.method == 'POST':
        username = request.form['User_name']
        Email_id = request.form['Email_id']
        Phone = request.form['Phone_number']
        password = request.form['password']
        reenter =  request.form['re_password'] 
    
        df = pd.read_csv("User_info.csv")
        user_list = df["User Name"]
        user_list = list(user_list)
        if password == reenter :
            if username not in user_list:
                return account_creation(username, password,Email_id,Phone)
            else:
                return "<h1> User already exists please Sign In</h1>"
        else:
            return "<h1>Wrong Confirm Password go back to home page</h1>"
    else:
        return render_template("signuppage.html")

@app.route("/signinpage",methods=['GET','POST'])
def SignIn_page():
    if request.method == 'POST':
        username = request.form['User_name']
        password = request.form['password']
        password_encoded = sha512(password.encode()).hexdigest()
    
        df = pd.read_csv("User_info.csv")
        user_list = df["User Name"]
        user_list = list(user_list)
        
        if username in user_list:
            password_list = df["Password"]
            password_list = list(password_list)
            num = user_list.index(username)
            pass_in_data = password_list[num]
            salt_list =  df["Salt"]
            salt_list = list(salt_list)
            salt = salt_list[num]
            log_list = df["First_login"]
            log_list = list(log_list)
            log = log_list[num]

            password_encoded = password_encoded + salt

            if pass_in_data == password_encoded:
                if log==0:
                    df.at[num,'First_login'] = 1
                    df.to_csv("User_info.csv")
                    return "<h1> please fill the data</h1>" # return more details page
                
                return "<h1>Your Welcome</h1>" # return main page here
            else:
                return "<h1> Wrong Username or Password</h1>"
        else:
                return "<h1> Wrong Username or Password</h1>"

    return render_template("signinpage.html")



def account_creation(username , password,Email_id,Phone):
    # here we will create a private key and public key for the user
    password_encoded = sha512(password.encode()).hexdigest()
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
    chars=[]

    for i in range(16):
        chars.append(random.choice(ALPHABET))
    salt = "".join(chars)
    password_encoded = password_encoded + salt
    # here we are appending the data to our files
    fields = ["ID","User Name","Email_id","Phone_number","Password","Salt","First_login"]
    df = pd.read_csv("User_info.csv")
    df1 = df[fields]
    Id_arr = df["ID"]
    num = Id_arr[len(Id_arr)-1] + 1
    log = 0
    data = [[num,username,Email_id,Phone,password_encoded,salt,log]]
    df2 = pd.DataFrame(data,columns=fields)
    df1 = df1.append(df2)
    df1.to_csv("User_info.csv")
    return render_template("signupcomplete.html") # here we will return the account confirmation page

if(__name__ ==" __main__"):
    app.run()


