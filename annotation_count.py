import pandas as pd
import glob
import os
from collections import Counter
import helper

#all orginal urls
path = r'C:/Users/rafe7/thesis/Twitter Data/tweets_url/after_fact_check'
all_clusters = sorted(glob.glob(path + "/*.csv"))


#list_credibility = []
# Import credibility check file
df_credibility = pd.read_csv('C:/Users/rafe7/thesis/Twitter Data/tweets_url/top_news_domains_credibility_final.csv')
df_credibility = helper.credibilty(df_credibility)
non_credible_domains = df_credibility[df_credibility['credibility'] == 'non-credible']['domain_name'].unique()
credible_domains = df_credibility[df_credibility['credibility'] == 'credible']['domain_name'].unique()

for cluster in all_clusters:
    list_credibility = []
    df = pd.read_csv(cluster)
    name = os.path.basename(os.path.realpath(cluster))
    #print('File Name: ', name)
    #print('total tweets: ', len(df))
    df = df.drop(['urls', 'domains'], axis=1)
    df['extra_urls'] = df['extra_urls'].replace(['no more url', 'twitter.com', 'twitter.com+'], '')
    df = df.rename(columns={'extra_urls': 'extra_urls_0'})
    df = helper.split_extra_urls(df)

    # Adding credibilty with each cluster or dataset

    for i in range(len(df)):
        d_list = []
        if df.iloc[i][2] == 'NO URL':
            list_credibility.append('NO URL')
        else:
            for j in df.columns[2:]:
                if len(df.iloc[i][f'{j}']) == 0:
                    break
                else:
                    d_list.append(df.iloc[i][f'{j}'])
            if len(d_list) == 0:
                list.append('NO URL')
            cr_level = helper.add_credibility(d_list, credible_domains, non_credible_domains)
            list_credibility.append(cr_level)
    #df['credibility'] = list_credibility
    z = Counter(list_credibility)
    with open('annotation_count.txt', 'a') as f:
        f.write(name)
        f.write('\t')
        f.write(str(z['credible']))
        f.write('\t')
        f.write(str(z['non-credible']))
        f.write('\t')
        f.write(str(z['NO URL']))
        f.write('\t')
        f.write(str(len(df)))
        f.write('\n')


#print(Counter(list_credibility))
