#https://developer.nytimes.com/article_search_v2.json#/Documentation/GET/articlesearch.json


def GetNYTNews(dictSearchTerms):
    import requests
    import pandas as pd
    strAPIKey = '?api-key=5a43ff59fbf54ed8a32fda9857e8b9aa'

    strSearchTerm = dictSearchTerms['strSearchTerm']
    stBegindate = dictSearchTerms['stBegindate']
    strEnDate = dictSearchTerms['strEnDate']
    strSort = dictSearchTerms['strSort']
    strReturnedFields = dictSearchTerms['strReturnedFields']
    print('SearchTerms:')
    print(dictSearchTerms)
    # strSearchTerm = '&q=Facebook'
    # stBegindate = '&begin_date=20170101'
    # strEnDate = '&end_date=20180731'
    # strSort = 'sort=newest'
    # strReturnedFields = '&fl=headline,lead_paragraph,snippet,pub_date,source,web_url'

    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    url = url + strAPIKey + strSearchTerm + stBegindate + strEnDate + strSort + strReturnedFields
    print(url)
    dfNYT = pd.DataFrame()

    for intpage in range(0,11):
        strPage = '&' + str(intpage)
        url = url + strPage

        print(url)

        r = requests.get(url)
        try:
            print(r.json()['response']['docs'][0])
            dfNYT = dfNYT.append(pd.DataFrame.from_dict(r.json()['response']['docs'], orient='columns'))
        except:
            break

    print(dfNYT.shape)
    return dfNYT



strSearchTerm = '&q=Facebook'
stBegindate = '&begin_date=20170101'
strEnDate = '&end_date=20180731'
strSort = 'sort='#'sort=newest'
strReturnedFields = '&fl=headline,lead_paragraph,snippet,pub_date,source,web_url'

dictSearchTerms = {'strSearchTerm':strSearchTerm,'stBegindate':stBegindate,'strEnDate':strEnDate,'strSort':strSort,'strReturnedFields':strReturnedFields}\

print(GetNYTNews(dictSearchTerms))