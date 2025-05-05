from presidio_analyzer import AnalyzerEngine,BatchAnalyzerEngine 
from presidio_anonymizer import AnonymizerEngine,BatchAnonymizerEngine
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from langchain_experimental.data_anonymizer import PresidioAnonymizer

import pandas as pd

#Anonymizer with default faker operators
lang_anonymizer_with_faker = PresidioReversibleAnonymizer(add_default_faker_operators=True)
fake_operators=lang_anonymizer_with_faker.operators
#Anonymizer with no default faker operator
lang_anonymizer_without_faker = PresidioReversibleAnonymizer(add_default_faker_operators=False)
lang_n_anonymizer = PresidioAnonymizer()

analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()

df_anonymizer = BatchAnonymizerEngine()

df_analyzer = BatchAnalyzerEngine(analyzer_engine=analyzer)


def anonymize_df(df):
    df_dict = df.to_dict(orient='list')
    #print(df_dict)
    analyzer_results = df_analyzer.analyze_dict(df_dict,language='en')
    analyzer_results = list(analyzer_results)
    anonymizer_results = df_anonymizer.anonymize_dict(analyzer_results,operators=fake_operators)
    anonymized_df = pd.DataFrame(anonymizer_results)
    #print(anonymized_df)
    return anonymized_df

def redact_df(df):
    df_dict = df.to_dict(orient='list')
    #print(df_dict)
    analyzer_results = df_analyzer.analyze_dict(df_dict,language='en')
    analyzer_results = list(analyzer_results)
    anonymizer_results = df_anonymizer.anonymize_dict(analyzer_results)
    redacted_df = pd.DataFrame(anonymizer_results)
    #print(redacted_df)
    return redacted_df   

def anonymize_text(text):
    anonymizer_results = lang_anonymizer_with_faker.anonymize(text)
    anonyizer_mapping = lang_anonymizer_with_faker.anonymizer_mapping
    lang_anonymizer_without_faker.reset_deanonymizer_mapping()
    #print(anonymizer_results)
    print(anonyizer_mapping)
    return {"text":anonymizer_results,"mapping":anonyizer_mapping}


def redact_text(text):
    anonymizer_results = lang_anonymizer_with_faker.anonymize(text)
    anonyizer_mapping = lang_anonymizer_with_faker.anonymizer_mapping
    #print(anonyizer_mapping)
    for entity_type in anonyizer_mapping:
        for entity in anonyizer_mapping[entity_type]:
            #print('Entity Type:',entity)
            text = text.replace(entity,'*'*len(entity))
    lang_anonymizer_without_faker.reset_deanonymizer_mapping()
    return {"text":text,"mapping":anonyizer_mapping}

def review_text(text):
    anonymizer_results = lang_anonymizer_with_faker.anonymize(text)
    anonyizer_mapping = lang_anonymizer_with_faker.anonymizer_mapping
    #entities = []
    # for entity_type in anonyizer_mapping:
    #     for entity in anonyizer_mapping[entity_type]:
    #         entities.append(entity)
    lang_anonymizer_without_faker.reset_deanonymizer_mapping()
    return {"text":text,"mapping":anonyizer_mapping}




