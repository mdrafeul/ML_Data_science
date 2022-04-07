import pandas as pd
def split_extra_urls(df):
    for i in range(len(df)):
        col_track = 0
        if (len(df['extra_urls_0'][i])) > 1:
            s = df['extra_urls_0'][i]
            # print(str(i) + s)
            s = s.split('+')
            s = s[:-1]  ##Just to remove extra element at the end due extra '+' in dataset
            for j in range(len(s)):
                if s[j] == 'twitter.com':
                    df[f'extra_urls_{col_track}'][i] = ''
                elif s[j] == 'youtube.com':
                    df[f'extra_urls_{col_track}'][i] = ''
                elif s[j] == 'google.com':
                    df[f'extra_urls_{col_track}'][i] = ''
                elif s[j] == 'instagram.com':
                    df[f'extra_urls_{col_track}'][i] = ''
                else:
                    df[f'extra_urls_{col_track}'][i] = s[j]
                    col_track += 1
                    if (f'extra_urls_{col_track}') in df.columns:
                        pass
                    else:
                        df[f'extra_urls_{col_track}'] = ''
    return (df)

def credibilty(df):
    df = df.dropna().reset_index()
    df = df.drop(['index'], axis=1)
    df['checked'] = df['checked'].str.lower()
    #changing the credibilty value 
    df.loc[df['checked'] == 'low', ['checked']] = 'non-credible'
    df.loc[df['checked'] == 'medium ', ['checked']] = 'credible'
    df.loc[df['checked'] == 'medium', ['checked']] = 'credible'
    df.loc[df['checked'] == 'high', ['checked']] = 'credible'
    df.loc[df['checked'] == 'high or medium', ['checked']] = 'credible'
    df = df.rename(columns={'checked': 'credibility'})
    df = df.drop(['count', 'percent', 'category'], axis=1)
    return (df)

def add_credibility(d_list, credible_domains, non_credible_domains):
    level = []
    if d_list[0] == 'NO URL':
        return ('NO URL')
    else:
        for i in range(len(d_list)):
            if d_list[i] in(credible_domains):
                level.append('credible')
            elif d_list[i] in(non_credible_domains):
                level.append('non-credible')
            else:
                pass
        if (len(level)) < 1:
            return ('')
        elif (len(level))< 2:
            return(level[0])
        else:
            result=False
            result = all(element == level[0] for element in level)
            if result :
                return(level[0])
            else:
                return('mixed')


def find_dates(cluster, df):
    dates = []
    lang = []
    l=1
    k=1
    for i in cluster:
            row_num = 0
            for j in df['What did you fact-check?']:
                if (i == j):
                    l=l+1
                    dates.append(df['When did you see the claim?'].iloc[row_num])
                    lang.append(df['Language of your fact-check'].iloc[row_num])
                row_num = row_num + 1
    df = pd.DataFrame({'created_at': dates, 'lang':lang})
    df = df[df['lang']=='English']
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['count'] = df.groupby('created_at')['created_at'].transform('count')

    return (df)