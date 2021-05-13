import json
import pandas as pd, numpy as np
# import pandas_profiling

# corpus_path = './static/data/corpus_5.txt'
# corpus_path_new = './static/data/corpus_5_new.txt'
corpus_path = 'static/data/corpus_5_new.json'


'''
sentences = []
with open(corpus_path, "r", encoding='utf-8') as fp:
    # 7:811:1:32:18 characterize the distribution of the population .
    # typeId:sentenceId:isExpert:tableId:expertId
    for line in fp.readlines():
        word = line.split()
        query = word[1:]
        info = word[0].split(":")

        typeId = info[0] if info[0][0] == '[' else str([int(info[0])])
        sentenceId = int(info[1])
        isExpert = int(info[2])
        tableId = int(info[3])
        expertId = int(info[4])
        sentence = " ".join(query)

        sentences.append({
            "typeId": typeId,
            "sentenceId": sentenceId,
            "isExpert": isExpert,
            "tableId": tableId,
            "expertId": expertId,
            "sentence": sentence,
            "dataAttribute": [1],
            "dataValue": ["x"],
            "unconfirmed": 0
        })

sentences_df = pd.DataFrame(sentences)
'''
sentences_df = pd.read_json(corpus_path)


def readCorpus(name):
    if name == "":
        return json.loads(sentences_df[sentences_df.isExpert == 1][["typeId", "sentenceId", "sentence", "dataAttribute", "dataValue", "unconfirmed"]].to_json(orient="records"))
    if name == "xk":
        return json.loads(sentences_df[(sentences_df.sentenceId <= 460) & (sentences_df.isExpert == 1)][["typeId", "sentenceId", "sentence", "dataAttribute", "dataValue", "unconfirmed"]].to_json(orient="records"))
    return json.loads(sentences_df[(sentences_df.sentenceId > 460) & (sentences_df.isExpert == 1)][["typeId", "sentenceId", "sentence", "dataAttribute", "dataValue", "unconfirmed"]].to_json(orient="records"))


def updateCorpus(sent_expert):
    '''
    dataAttribute = [] if sent_expert["dataAttribute"] == "" else sent_expert["dataAttribute"].split(";")
    dataValue = [] if sent_expert["dataValue"] == "" else sent_expert["dataValue"].split(";")

    sentences_df.loc[sentences_df["sentenceId"] == sent_expert["sentenceId"], ["typeId","dataAttribute", "dataValue","unconfirmed"]] = \
        np.array([sent_expert["typeId"], [dataAttribute], [dataValue], int(sent_expert["unconfirmed"])], dtype=object)
    '''
    # 如果是非数组的话，可以直接为： sentences_df.loc[sentences_df["sentenceId"] == sent_expert["sentenceId"], sent_expert["field"]] = sent_expert["value"]
    print(sent_expert)
    sentences_df.loc[sentences_df["sentenceId"] == sent_expert["sentenceId"], sent_expert["field"]] = \
        sentences_df.loc[sentences_df["sentenceId"] == sent_expert["sentenceId"], sent_expert["field"]].apply(lambda x: sent_expert["value"])


def writeCorpus():
    with open(corpus_path, "w", encoding='utf-8') as fpw:
        fpw.write(sentences_df[sentences_df.isExpert == 1].to_json(orient="records"))
        '''
        for t in sentences_df.itertuples():
            info = "%s:%d:%d:%d:%d" % (t.typeId, t.sentenceId, t.isExpert, t.tableId, t.expertId)
            fpw.write("%s %s %s\n" % (info, t.sentence, t.dataRelated if type(t.dataRelated) == str else json.dumps(t.dataRelated)))
        '''


'''
def generateReport(isExpert):
    if isExpert:
        profile = pandas_profiling.ProfileReport(sentences_df[sentences_df.isExpert == 1], title='Quda Expert Sentences Report')  # explorative=True
        profile.to_file('./templates/quda_expert_report.html')
    else:
        profile = pandas_profiling.ProfileReport(sentences_df, title='Quda All Sentences Report')  # explorative=True
        profile.to_file('./templates/quda_all_report.html')
'''
