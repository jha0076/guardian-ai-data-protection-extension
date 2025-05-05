from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import presidio_toolkit as pt
import bedrock_toolkit as bd
import json
import pandas as pd
import os
import shutil

with open('backend/guardians.json','r') as f:
    guardians = json.loads(f.read())

def_guardian = guardians['default']
cur_guardian = def_guardian

upload_path = os.path.join(os.getcwd(),'files','upload')
if os.path.exists(upload_path):
    shutil.rmtree(upload_path)
os.makedirs(upload_path)

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = upload_path


def save_file_to_local(file):
    """
    This method is to save the recieved source file into server
    """
    src_file_path = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
    des_file_path = os.path.join(app.config['UPLOAD_FOLDER'],'pro_'+file.filename)
    file.save(src_file_path)
    with open(src_file_path,'r') as f:
        text = ''.join([line for line in f])
    return text,des_file_path

# def save_protected_file_to_local(file_path,text):
#     with open(file_path,'w') as f:
#         f.write(text)
    




@app.route('/change_guardian',methods=['POST'])
def change_guardian():
    """
    This call is to change the guardian based on users choice
    """
    global cur_guardian
    try:
        if request.method == 'POST':
            guardian = request.args['guardian']
            if guardian in guardians:
                
                cur_guardian = guardian
            else:
                cur_guardian = def_guardian
            print(cur_guardian)
            return cur_guardian
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


@app.route('/anonymize_csv',methods=['POST'])
def anonymize_csv():
    """
    This method is to anonymize the csv file
    """
    try:
        if request.method == 'POST':
            files = request.files
            if 'file' not in files:
                return 'Please upload file to process'
            file = files['file']
            src_file_path = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            des_file_path = os.path.join(app.config['UPLOAD_FOLDER'],'pro_'+file.filename)
            file.save(src_file_path)
            df = pd.read_csv(src_file_path)
            anonymized_df = pt.anonymize_df(df)
            anonymized_df.to_csv(des_file_path,index=False)
            return send_file(des_file_path,as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    


@app.route('/redact_csv',methods=['POST'])
def redact_csv():
    """
    This method is to redact the csv file
    """
    try:
        if request.method == 'POST':
            files = request.files
            if 'file' not in files:
                return 'Please upload file to process'
            file = files['file']
            src_file_path = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
            des_file_path = os.path.join(app.config['UPLOAD_FOLDER'],'pro_'+file.filename)
            file.save(src_file_path)
            df = pd.read_csv(src_file_path)
            anonymized_df = pt.redact_df(df)
            anonymized_df.to_csv(des_file_path,index=False)
            return send_file(des_file_path,as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    


@app.route('/anonymize_text_file',methods=['POST'])
def anonymize_text_file():
    """
    This call is to anonymize the text file
    """
    try:
        if request.method == 'POST':
            files = request.files
            
            if 'file' not in files:
                return 'Please upload file to process'
            
            file = files['file']
            text,des_file_path = save_file_to_local(file)

            if cur_guardian == 'Presidio':
                results = pt.anonymize_text(text=text)
                #save_protected_file_to_local(des_file_path,anonymized_text)
                return results
                
            elif cur_guardian == 'LLM':
                #LLM calls need to be added
                pass
            elif cur_guardian == "Bedrock":
                #Bedrock LLM Model calls should be added
                results = bd.anonymize_text(text=text)
                return results
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


@app.route('/redact_text_file',methods=['POST'])
def redact_text_file():
    """
    This call is to anonymize the text file
    """
    try:
        if request.method == 'POST':
            files = request.files
            if 'file' not in files:
                return 'Please upload file to process'
            
            file = files['file']
            text,des_file_path = save_file_to_local(file)

            if cur_guardian == 'Presidio':
                results = pt.redact_text(text=text)
                #save_protected_file_to_local(des_file_path,redacted_text)
                return results
            elif cur_guardian == 'LLM':
                #LLM calls need to be added
                pass
            elif cur_guardian == "Bedrock":
                #Bedrock LLM Model calls should be added
                results = pt.redact_text(text=text)
                return results
    except Exception as e:
        return jsonify({'error': str(e)}), 400




@app.route('/review_text_file',methods=['POST'])
def review_text_file():
    """
    This call is to anonymize the text file
    """
    try:
        if request.method == 'POST':
            files = request.files
            if 'file' not in files:
                return 'Please upload file to process'
            
            file = files['file']
            text,des_file_path = save_file_to_local(file)

            if cur_guardian == 'Presidio':
                results = pt.review_text(text=text)
                #save_protected_file_to_local(des_file_path,reviewed_text)
                return results
            elif cur_guardian == 'LLM':
                #LLM calls need to be added
                pass
            elif cur_guardian == "Bedrock":
                #Bedrock LLM Model calls should be added
                results = bd.review_text(text=text)
             
                return results
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/anonymize_text',methods=["POST"])
def anonymize():
    """
    This call is to anonymize the text
    """
    print(cur_guardian)
    try:
        if request.method == 'POST':
            text = request.args['text']
            if cur_guardian == 'Presidio':
                result = pt.anonymize_text(text=text)
                return result
            elif cur_guardian == 'LLM':
                #LLM calls need to be added
                pass
            elif cur_guardian == "Bedrock":
                #Bedrock LLM Model calls should be added
                result = bd.anonymize_text(text=text)
                return result
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    



@app.route('/redact_text',methods=['POST'])
def redact():
    """
    This call is to redact the text
    """
    try:
        if request.method == 'POST':
            text = request.args['text']
            if cur_guardian == 'Presidio':
                return pt.redact_text(text=text)
            elif cur_guardian == 'LLM':
                #LLM calls need to be added
                pass
            elif cur_guardian == "Bedrock":
                #Bedrock LLM Model calls should be added
                result = bd.redact_text(text=text)
                return result
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

    

@app.route('/review_text',methods=['POST'])
def review():
    """
    This call is to identify the PII entities in the text
    """
    try:
        if request.method == 'POST':
            text = request.args['text']
            if cur_guardian == 'Presidio':
                result = pt.review_text(text=text)
                return result
            elif cur_guardian == 'LLM':
                #LLM calls need to be added
                pass
            elif cur_guardian == "Bedrock":
                #Bedrock LLM Model calls should be added
                result = bd.review_text(text=text)
                return result

    except Exception as e:
        return jsonify({'error': str(e)}), 400

   
if __name__ == '__main__':
    app.run()

















# text = """Date: October 19, 2021
# Witness: John Doe
# Subject: Testimony Regarding the Loss of Wallet
# Testimony Content:
# Hello Officer,
# My name is John Doe and on October 19, 2021, my wallet was stolen in
# the vicinity of Kilmarnock during a bike trip. This wallet contains
# some very important things to me.
# Firstly, the wallet contains my credit card with number 4111 1111 1111 1111,
#  which is registered under my name and linked to my bank account,
# PL61109010140000071219812874.
# Additionally, the wallet had a driver's license DL No: 999000680
# issued to my name. It also houses my Social Security Number, 602-76-4532.
# -
# What's more, I had my polish identity card there, with the number
# ABC123456.
# I would like this data to be secured and protected in all possible
# ways. I believe It was stolen at 9:30 AM.

# In case any information arises regarding my wallet, please reach out
# to me on my phone number, 999-888-7777, or through my personal email,
# johndoe@example.com.

# Please consider this information to be highly confidential and respect
# my privacy.
# The bank has been informed about the stolen credit card and necessary
# actions have been taken from their end. They will be reachable at their
# official email, support@bankname.com.
# My representative there is Victoria Cherry (her business phone: 987-554-3210).

# Thank you for your assistance
# Jon Doe."""

# #print(identify_and_review(text=text))
