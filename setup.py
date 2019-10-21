from flask import Flask, jsonify, request
import json
from bson.objectid import ObjectId
from MongoDBManager import mongoDBManager

app = Flask(__name__)

# routes
@app.route('/Login', methods=['GET'])

@app.route('/Register', methods=['POST'])
@app.route('/CheckEmail', methods=['GET'])
@app.route('/CheckUsername', methods=['GET'])

@app.route('/ChangePassword', methods=['POST'])

@app.route('/GetKeywords', methods=['GET'])
@app.route('/GetTweetDetails', methods=['GET'])

@app.route('/UpdateKeywords', methods=['POST'])
# @app.route('/DeleteOldTweets', methods=['GET'])

def start():
    # initialize mongoDB class
    MM = mongoDBManager()

    # rule to get the url of request
    rule = request.url_rule

    # POST requests
    if request.method == "POST":

        # Sign user up
        if 'Register' in rule.rule:
            print("register method called")

            # get parameters
            username = request.args.get('username')
            email = request.args.get('email')
            password = request.args.get('pass')

            #check email availability
            emailAvailability = MM.checkEmailAvailability(email)
            if emailAvailability == True:
                # Register user
                registerStatus = MM.register(username, email, password)


                if registerStatus == True:
                    output = {'status': '001'}
                else:
                    output = {'status': '002'}

                return jsonify(output)

            else:
                print("email is already in use")
                output = {'status': '003'}
                return jsonify(output)

        # Change user password
        elif 'ChangePassword' in rule.rule:
            print("change password method called")
            email = request.args.get('email')
            oldPassword = request.args.get('oldPass')
            newPassword = request.args.get('newPass')

            changeStatus = MM.changePassword(email, oldPassword, newPassword)

            if changeStatus == True:
                output = {'status': '001'}
            else:
                output = {'status' : '002'}

            return jsonify(output)

        # Update keywords
        elif 'UpdateKeywords' in rule.rule:
            keywords = request.args.getlist('keywords')
            id = request.args.get('id')
            status = MM.updateUserKeywords(keywords, id)

            if status == True:
                output = {"Status": "001"}
            else:
                output = {"Status" : "002"}

            return jsonify(output)
# ---------------------------------------------------------------------------------------------------------------------#
    # GET Requests
    elif request.method == "GET":
        # Log user in
        if 'Login' in rule.rule:
            print("login method called")
            email = request.args.get('email')
            password = request.args.get('pass')

            print(email, " ", password)

            user = MM.login(email, password)
            if user is not None :
                output = {'status': '001',
                          'id': str(user['_id']),
                          'username': user['username'],
                          'email': user['email'],
                          'keywords': user['keywords']}
            else:
                output = {'status': '002'}


            return jsonify(output)

        # Check if email is available for sign up
        elif 'CheckEmail' in rule.rule:
            print("login method called")
            email = request.args.get('email')

            checkEmail = MM.checkEmailAvailability(email)

            if checkEmail == True:
                output = {'status': '003',
                          'message': 'email available!'}
            else:
                output = {'status': '004',
                          'message': 'email unavaiable!'}

            return jsonify(output)

        # Get user's keywords history
        elif 'GetKeywords' in rule.rule:
            id = request.args.get('id')
            keywords = MM.getKeywords(id)

            output = {'keywords': keywords}
            return jsonify(output)

        # Get tweets details
        elif 'GetTweetDetails' in rule.rule:
            id = request.args.get('id')
            keyword = request.args.get('keyword')

            tweetCollection = MM.getTweetDetails(keyword, id)

            tweetDetails = []
            for tweet in tweetCollection:
                t = {"name": tweet['name'],
                     "created at" : tweet['created at'],
                     "text": tweet['text'],
                     "sentiment": tweet['sentiment']}
                tweetDetails.append(t)
            output = {"tweets details": tweetDetails}
            return jsonify(output)

        # Delete old tweets details
        # elif 'DeleteOldTweets' in rule.rule:
        #     keyword = request.args.get('keyword')
        #     id = request.args.get('id')
        #
        #     status = MM.deleteOldTweetsDetails(keyword, id)
        #
        #     if status == True:
        #         output = {"Status": "001"}
        #     else:
        #         output = {"Status": "002"}
        #
        #     return jsonify(output)

    else:
        output = {'error': 'Invalid method'}
        print(output)
        return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)