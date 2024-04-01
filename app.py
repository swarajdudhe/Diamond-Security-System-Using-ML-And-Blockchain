from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
import requests
import pickle
import numpy as np
import hashlib
import math
from block import write_block, check_integrity, get_owner_name

app = Flask(__name__)  

# MySQL database configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="diamond_security_system"
)
mycursor = mydb.cursor()


# importing the ML models
five_parameter_rfa = pickle.load(open('colab_files/five_parameter_rfa.pkl','rb'))
fourty_parameter_rfa = pickle.load(open('colab_files/fourty_parameter_rfa.pkl','rb'))
DiamondPrice_linearReg = pickle.load(open('colab_files/DiamondPrice_linearReg.pkl','rb'))


@app.route('/', methods = ['POST','GET'])
def index():
    return render_template('index.html')



# contact us page start
@app.route('/contact', methods = ['POST','GET'])
def contact():
    if request.method == 'POST':
        # Get form data
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        number = request.form.get('number')
        message = request.form.get('message')
        
        # Store data in MySQL database
        mycursor.execute("INSERT INTO `contact-us-table` (FirstName, LastName, EmailAddress, MobileNumber, Message) VALUES (%s, %s, %s, %s, %s)",
                         (fname, lname, email, number, message))
        mydb.commit()
        
        # Prepare data for Web3Forms API
        data = {
            'access_key': 'f2313c7a-4933-4163-9f6a-d8cbec9b95cd',
            'fname': fname,
            'lname': lname,
            'email': email,
            'number': number,
            'message': message
        }
        
        # Send data to Web3Forms API
        response = requests.post('https://api.web3forms.com/submit', data=data)
        
        # Check if the submission was successful
        if response.status_code == 200:
            #return render_template('contact-us.html')
            result = "Submitted Successfully, Thank you"
        else:
            # return render_template('contact-us.html')
            result = "Something went wrong please try again later"

        return render_template('contact-us.html',result = result)
    
    return render_template('contact-us.html')

# contact us page end

# log in page start
@app.route('/login', methods = ['POST','GET'])
def login():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #     registerAs = request.form.get('registerAs')
    #     mycursor.execute("select * from `registration-table` where Email='"+email+"' and Password='"+password+"' and RegisterAs='"+registerAs+"'")
    #     r = mycursor.fetchall()
    #     count = mycursor.rowcount
    #     if count == 1:
    #         return render_template('dashboard.html')
    #     else:
    #         result = "invalid credentials please try again"
    #         return render_template('login.html', result=result)
    # return render_template('login.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        registerAs = request.form.get('registerAs')
        
        # Hash the input password
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()

        mycursor.execute("SELECT Name FROM `registration-table` WHERE Email=%s AND Password=%s AND RegisterAs=%s", (email, password, registerAs))
        user = mycursor.fetchone()  # Fetch one row
        
        if user:
            # Successful login, redirect to dashboard with user's name
            global username
            username=user[0].strip()
            return redirect(url_for('dashboard', username=username))

            # return redirect(url_for('dashboard', username=user[0]))
        else:
            result = "Invalid credentials, please try again"
            return render_template('login.html', result=result)
    return render_template('login.html')

# log in page end

# registration page start
@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        mobileno = request.form.get('mobileno')
        registerAs = request.form.get('registerAs')
        email = request.form.get('email')
        vemail = request.form.get('vemail')
        password = request.form.get('password')
        vpassword = request.form.get('vpassword')

        # Check if the email already exists in the database
        mycursor.execute("SELECT * FROM `registration-table` WHERE Email = %s", (email,))
        existing_user = mycursor.fetchone()  # Fetch one row

        if existing_user:
            result = "Email ID is already registered"
        else:
            # Store data in MySQL database
            mycursor.execute("INSERT INTO `registration-table` (Name, Address, MobileNo, RegisterAs, Email, `Verify-Email`, Password, `Verify-password`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                             (name, address, mobileno, registerAs, email, vemail, password, vpassword))
            mydb.commit()

            result = "Registration Successfully Completed, Thank you"

        return render_template('registration.html', result=result)

    return render_template('registration.html')

# registration page end


# # Dashboard start
# @app.route('/dashboard', methods=['POST', 'GET'])
# def dashboard():
#      return render_template('dashboard.html')

# Dashboard End

@app.route('/dashboard/<username>', methods=['POST', 'GET'])
def dashboard(username):
    return render_template('dashboard.html', username=username)

# sale diamond start
@app.route('/sale_diamond', methods=['POST', 'GET'])
def sale_diamond():
    if request.method == 'POST':
        GIA_name = request.form.get('GIA_name')
        Type_diamond = request.form.get('type_diamond')
        owner_name = request.form.get('owner_name')
        owner_number = request.form.get('owner_number')
        carat = request.form.get('carat')
        cut = request.form.get('cut')
        color = request.form.get('color')
        clearity = request.form.get('clearity')
        symmetry = request.form.get('symmetry')
        price = request.form.get('price')
        Image = request.form.get('file')

        mycursor.execute("INSERT INTO `salesdata` (GIA_name, Type_diamond, owner_name, owner_number, carat, cut, color, clearity, symmetry, price, Image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (GIA_name, Type_diamond, owner_name,owner_number,carat, cut, color, clearity, symmetry, price, Image))
        mydb.commit()

        result = "Diamond Registered Successfully"
        return render_template('sale_diamond.html',result=result)

    return render_template('sale_diamond.html')

# sale diamond end


@app.route('/buy_diamond', methods=['POST', 'GET'])
def buy_diamond():
    try:
        # Fetch data from the database
        mycursor.execute("SELECT * FROM `salesdata`")
        data = mycursor.fetchall()
        print(data)

        # Render the buy_diamond.html template with the fetched data
        return render_template('buy_diamond.html', data=data)
    except mysql.connector.Error as e:
        # Print any error that occurs during database access for debugging
        print("Error fetching data from database:", e)
        # Return an error page or handle the exception as appropriate
        return render_template('error occured')



@app.route('/secure_diamond', methods=['POST', 'GET'])
def secure_diamond():
     message = None
     if request.method == 'POST':
        DiamondId = request.form.get('DiamondId')
        DiamondName = request.form.get('DiamondName')
        OwnerName = request.form.get('OwnerName')
        DateOfMine = request.form.get('DateOfMine')
        carat = request.form.get('carat')
        cut = request.form.get('cut')
        color = request.form.get('color')
        clarity = request.form.get('clarity')
        symmetry = request.form.get('symmetry')
        TypeOf = request.form.get('TypeOf')
        # Call write_block function and capture the returned message
        message = write_block(DiamondId=DiamondId, DiamondName=DiamondName, OwnerName=OwnerName,DateOfMine=DateOfMine,carat=carat,cut=cut,color=color,clarity=clarity,symmetry=symmetry,TypeOf=TypeOf)
        return render_template('secure_diamond.html', result=message)
     return render_template('secure_diamond.html')

@app.route('/checking',methods=['POST', 'GET'])
def check():
    results = check_integrity()
    return render_template('secure_diamond.html', checking_results=results)


# diamond 5c start
@app.route('/diamond_5c', methods=['POST', 'GET'])
def diamond_5c():
     if request.method == 'POST':
        carat = request.form.get('carat')
        cut = request.form.get('cut')
        color = request.form.get('color')
        clarity = request.form.get('clarity')
        symmentry = request.form.get('symmentry')

        prediction = five_parameter_rfa.predict(np.array([carat,cut,color,clarity,symmentry]).reshape(1,-1))
        if prediction[0] == 1:
            result = "Data relates to the Natural Diamond"
            return render_template('diamond_5c.html',result= result)
        else:
            result = "Data relates to the Artificial Diamond"
            return render_template('diamond_5c.html',result= result)
     
     return render_template('diamond_5c.html')

# diamond 5c End

# diamond 5c start
@app.route('/diamond_40c', methods=['POST', 'GET'])
def diamond_40c():
    if request.method == 'POST':
        DiamondPrice = request.form.get('DiamondPrice')
        Carat = request.form.get('Carat')
        Cut = request.form.get('Cut')
        Color = request.form.get('Color')
        Clarity = request.form.get('Clarity')
        Symmetry = request.form.get('Symmetry')
        Depth = request.form.get('Depth')
        Table = request.form.get('Table')
        Length = request.form.get('Length')
        Width = request.form.get('Width')
        Height = request.form.get('Height')
        Cut_Grade = request.form.get('Cut_Grade')
        Polish_Grade = request.form.get('Polish_Grade')
        Fluorescence = request.form.get('Fluorescence')
        Girdle = request.form.get('Girdle')
        Culet = request.form.get('Culet')
        Length_CW_Ratio = request.form.get('Length_CW_Ratio')
        Width_CW_Ratio = request.form.get('Width_CW_Ratio')
        Height_CW_Ratio = request.form.get('Height_CW_Ratio')
        Ang_Pav_Polish = request.form.get('Ang_Pav_Polish')
        Ang_Girdle = request.form.get('Ang_Girdle')
        Ang_Culet = request.form.get('Ang_Culet')

        prediction = fourty_parameter_rfa.predict(np.array([DiamondPrice,Carat,Cut,Color,Clarity,Symmetry,Depth,Table,Length,Width,Height,Cut_Grade,Polish_Grade,Fluorescence,Girdle,Culet,Length_CW_Ratio,Width_CW_Ratio,Height_CW_Ratio,Ang_Pav_Polish,Ang_Girdle,Ang_Culet]).reshape(1,-1))
        
        if prediction[0] == 1:
            result = "Data relates to the Natural Diamond"
            return render_template('diamond_40c.html',result= result)
        else:
            result = "Data relates to the Artificial Diamond"
            return render_template('diamond_40c.html',result= result)
     
    return render_template('diamond_40c.html')
# diamond 5c End

@app.route('/recommendation', methods=['POST', 'GET'])
def recommendation():
     return "Apologies for the inconvenience. Rest assured, we're actively addressing the issue."

@app.route('/priceDetection', methods=['POST', 'GET'])
def priceDetection():
     if request.method == 'POST':
        carat = float(request.form.get('carat'))
        cut = float(request.form.get('cut'))
        color = float(request.form.get('color'))
        clarity = float(request.form.get('clarity'))
        symmentry = float(request.form.get('symmentry'))
        TypeOfDiamond = float(request.form.get('TypeOfDiamond'))

        prediction = DiamondPrice_linearReg.predict(np.array([carat,cut,color,clarity,symmentry,TypeOfDiamond]).reshape(1,-1))
        return render_template('price_detection.html',result=prediction)
     return render_template('price_detection.html')

@app.route('/VerifyBeforeBuy', methods=['POST', 'GET'])
def VerifyBeforeBuy():
     data = []
     if request.method == 'POST':
         Carat = float(request.form.get('Carat'))
         Cut = float(request.form.get('Cut'))
         Color = float(request.form.get('Color'))
         Clarity = float(request.form.get('Clarity'))
         Symmetry = float(request.form.get('Symmetry'))
         Hash = request.form.get('hash')
         DiamondName = str(request.form.get('DiamondName'))
         DiamondID = str(request.form.get('diamondID'))
         OtherData = request.form.get('otherData')
         YourName = str(request.form.get('yourname'))
         MoNumber = str(request.form.get('monumber'))
         Email = str(request.form.get('email'))

         mycursor.execute("INSERT INTO `verifybeforebuy` (Carat, Cut, Color, Clarity, Symmetry, Hash, DiamondName, DiamondID, OtherData, YourName, MoNumber,Email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (Carat, Cut, Color,Clarity,Symmetry, Hash, DiamondName, DiamondID, OtherData, YourName, MoNumber,Email))
         mydb.commit()

         prediction_diamond = five_parameter_rfa.predict(np.array([Carat,Cut,Color,Clarity,Symmetry]).reshape(1,-1))
         if prediction_diamond[0] == 1:
            TypeOfDiamond = int(1)
            prediction_diamond_result = "Diamond data relates to Natural Diamond"
         else:
            TypeOfDiamond = int(0)
            prediction_diamond_result = "Diamond data relates to Artificial Diamond"
         data.append(prediction_diamond_result)

         prediction_price = DiamondPrice_linearReg.predict(np.array([Carat,Cut,Color,Clarity,Symmetry,TypeOfDiamond]).reshape(1,-1))
         prediction_price_result = f"The approximate price of your diamond is {prediction_price}"
         data.append(prediction_price_result)

         fetch_owner_name = get_owner_name(carat=Carat, cut=Cut, color=Color, clarity=Clarity, symmetry=Symmetry, TypeOf=TypeOfDiamond, DiamondId=DiamondID)
         data.append(fetch_owner_name)

         return render_template('verify_before_buy.html',data=data)
     
     return render_template('verify_before_buy.html')

if __name__ == '__main__':
    app.run(debug = True)