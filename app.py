from flask import Flask, render_template, request, redirect, jsonify
import pymysql
import bcrypt
import webbrowser
import jwt

app = Flask(__name__)

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='userinfo', charset='utf8')

cursor = db.cursor()

app.config['JWT_SECRET_KEY'] = 'WELCOME_TO_CRYPTOGRAPHY_WORLD'
algorithm = 'HS256'

@app.route('/', methods=["GET"])
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        register_info = request.form

        name = register_info['name']
        username = register_info['username']
        hashed_password = bcrypt.hashpw(register_info['password'].encode('utf-8'), bcrypt.gensalt())
        email = register_info['email']
        print(name, username, hashed_password, email)
        sql = """
            INSERT INTO UserInfo (name, username, hashed_password, email)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(sql, (name, username, hashed_password, email))
        db.commit()
        #db.close() 
        return redirect(request.url)

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_info = request.form

        username = login_info['username']
        password = login_info['password']

        sql = "SELECT * FROM UserInfo WHERE username=%s"
        rows_count = cursor.execute(sql, username)    


        if rows_count > 0:
            user_info = cursor.fetchone()
            print("user info: ", user_info)

            name = user_info[1]

            is_pw_correct = bcrypt.checkpw(password.encode('UTF-8'), user_info[3].encode('UTF-8'))
            print("password check: ", is_pw_correct)
            if  is_pw_correct == False:
                return render_template('fail_login.html')

        

                
                
            else:
                user_username = user_info[2]  
                user_password = user_info[3]
                payload = {
                    'user_username' : user_username,
                    'user_password' : user_password
                }
                token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm)


                #return jsonify(result=200, data={'access_token': token})
                return render_template('success_login.html',name=name, token=token)




        else:
            print('User does not exist')
            return {
                "message": "User Not Found"
            }, 404

        return redirect(request.url)

    
    return render_template('login.html')     


    

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=False)




