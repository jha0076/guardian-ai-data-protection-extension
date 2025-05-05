import boto3
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,RetrievalQA
import json
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent

# from langchain.embeddings import BedrockEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import dotenv_values
creds = dotenv_values()

if creds!={}:

    bedrock_runtime = boto3.client(
        service_name = "bedrock-runtime",
        region_name = creds['ACCESS_KEY'],
        aws_access_key_id=creds['ACCESS_KEY'],
        aws_secret_access_key=creds['SECRET_ACCESS_KEY']
    )
    llm = Bedrock(
        model_id="mistral.mistral-7b-instruct-v0:2",
        client=bedrock_runtime,
        model_kwargs={
            "max_tokens":2000, "temperature":0.1, "top_p":0.9, "top_k":50
        }
    )



    def process_text(template,text):
        prompt = PromptTemplate(template=template,input_variables=['text'])
        chain = LLMChain(prompt=prompt,llm=llm)
        result = chain({'text':text})['text']
        start_index = result.find('{')
        end_index = result.rfind('}')
        result = result[start_index : end_index + 1]

        try:
            json_response = json.loads(result)
            
            return json_response

        except json.JSONDecodeError as e:
            print(f"Error:{e}")
            return result      


    def anonymize_text(text):
        
        template = """
        As a data privacy officer, your responsibility is to identify and anonymize personally identifiable information (PII) within text documents.

        # OBJECTIVE #
        Your task is to process text input containing PII information. Your objective is to replace real PII values with entirely fictitious ones.

        # INSTRUCTIONS #
        When anonymizing PII values, ensure that the structure and context of the data remain intact, and avoid truncating any information.
        Generate fictitious values that are significantly different from the original ones.
        For example, 'Hi, my name is John Doe. I lost my wallet on 22nd October, 2023' could be anonymized as 'Hi, my name is Jane Smith. I lost my wallet on 13th November, 2022'.

        # RESPONSE #
        The expected response format is a JSON object with two keys: 'text' and 'mapping'. 
        The 'text' key should contain the anonymized text, while the 'mapping' key should consist of an array of JSON objects.
        Each JSON object in the 'mapping' array should represent the original and fictitious PII values, ensuring they are entirely dissimilar.
        For instance, every json object should look like "John Doe":'Jane Smith', "22nd October, 2023":'13th November, 2022'.

        Below is the input text:
        ``````````
        {text}
        ``````````
        """

        return process_text(template,text)    
            

    def redact_text(text):
        template = """
        As a data privacy officer, your responsibility is to identify and anonymize personally identifiable information (PII) within text documents.

        # OBJECTIVE #
        Your task is to process text input containing PII information. Your objective is to replace real PII values with entirely fictitious ones.

        # INSTRUCTIONS #
        When anonymizing PII values, ensure that the structure and context of the data remain intact, and avoid truncating any information.
        Generate fictitious values that are significantly different from the original ones.
        For example, 'Hi, my name is John Doe. I lost my wallet on 22nd October, 2023' could be anonymized as 'Hi, my name is *****. I lost my wallet on *****'.

        # RESPONSE #
        The expected response format is a JSON object with two keys: 'text' and 'mapping'. 
        The 'text' key should contain the original text, while the 'mapping' key should consist of an array of JSON objects.
        Each JSON object in the 'mapping' array should represent the original and fictitious PII values, ensuring they are entirely dissimilar.
        For instance, every json object should look like 'John Doe':'*****', '22nd October, 2023':'*****'.

        Below is the input text:
        ``````````
        {text}
        ``````````
        """
        return process_text(template,text)
        
        

    def review_text(text):
        template = """
        As a data privacy officer, your responsibility is to identify and anonymize personally identifiable information (PII) within text documents.

        # OBJECTIVE #
        Your task is to process text input containing PII information. Your objective is to replace real PII values with entirely fictitious ones.

        # INSTRUCTIONS #
        When anonymizing PII values, ensure that the structure and context of the data remain intact, and avoid truncating any information.
        Generate fictitious values that are significantly different from the original ones.
        For example, 'Hi, my name is John Doe. I lost my wallet on 22nd October, 2023' could be anonymized as 'Hi, my name is Jane Smith. I lost my wallet on 13th November, 2022'.

        # RESPONSE #
        The expected response format is a JSON object with two keys: 'text' and 'mapping'. 
        The 'text' key should contain the original text, while the 'mapping' key should consist of an array of JSON objects.
        Each JSON object in the 'mapping' array should represent the original and fictitious PII values, ensuring they are entirely dissimilar.
        For instance, every json object should look like 'John Doe':'Jane Smith', '22nd October, 2023':'13th November, 2022'.

        Below is the input text:
        ``````````
        {text}
        ``````````
        """
        result = process_text(template,text)
        result['text']=text
        return result
    def anonymize_df():
        pass
    def review_df():
        pass

























