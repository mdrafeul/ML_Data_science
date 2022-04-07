import pandas as pd
import matplotlib.pyplot as plt
import helper

# Import main coronafact check  file
# required column 'When did you see the claim?', 'Language of your fact-check' and 'What did you fact-check?'
df_coronavirus_facts = pd.read_csv('C:/Users/rafe7/thesis/thesis_mainclaims/Clustering/CoronavirusFacts database.csv')
df_coronavirus_facts = df_coronavirus_facts[
    ['When did you see the claim?', 'Language of your fact-check', 'What did you fact-check?']]

# Import credibility check file
df_credibility = pd.read_csv('C:/Users/rafe7/thesis/Twitter Data/tweets_url/top_news_domains_credibility_final.csv')
df_credibility = helper.credibilty(df_credibility)
#print(df_credibility)

# Import tweets file for each cluster
df = pd.read_csv('C:/Users/rafe7/thesis/Twitter Data/tweets_url/after_fact_check/elisa_granato.csv')  # For each cluster use the corresponding file
#df_2 = pd.read_csv('C:/Users/rafe7/thesis/Twitter Data/tweets_url/after_fact_check/tea1.csv')
#df_3 = pd.read_csv('C:/Users/rafe7/thesis/Twitter Data/tweets_url/after_fact_check/tea2.csv')
#frames = [df_1, df_2, df_3]
#df = pd.concat(frames).reset_index()

#df = df.drop(['urls', 'index', 'domains'], axis=1)
df = df.drop(['urls', 'domains'], axis=1)
df['extra_urls'] = df['extra_urls'].replace(['no more url', 'twitter.com', 'twitter.com+'], '')
df = df.rename(columns={'extra_urls': 'extra_urls_0'})

df = helper.split_extra_urls(df)

# Adding credibilty with each cluster or dataset
non_credible_domains = df_credibility[df_credibility['credibility'] == 'non-credible']['domain_name'].unique()
credible_domains = df_credibility[df_credibility['credibility'] == 'credible']['domain_name'].unique()
list_credibility = []
for i in range(len(df)):
    d_list = []
    for j in df.columns[2:]:
        if len(df.iloc[i][f'{j}']) == 0:
            break
        else:
            d_list.append(df.iloc[i][f'{j}'])
    cr_level = helper.add_credibility(d_list, credible_domains, non_credible_domains)
    list_credibility.append(cr_level)
df['credibility'] = list_credibility

# Visualization
df_credible = df[df['credibility'] == 'credible'].pivot_table(columns=['create_at'], aggfunc='size').reset_index()
print('crdiblie tweets: ', len(df_credible))
df_non_credible = df[df['credibility'] == 'non-credible'].pivot_table(columns=['create_at'],
                                                                      aggfunc='size').reset_index()
print('non-crdiblie tweets: ', len(df_non_credible))
df_no_url = df[df['credibility'] == 'NO URL'].pivot_table(columns=['create_at'], aggfunc='size').reset_index()
print('No-URL tweets: ', len(df_no_url))
df_mixed = df[df['credibility'] == 'mixed'].pivot_table(columns=['create_at'], aggfunc='size').reset_index()
print('mixed tweets: ', len(df_mixed))
print('Total Tweets: ', len(df))

##converting str to datetime
df_credible['create_at'] = pd.to_datetime(df_credible['create_at'])
df_no_url['create_at'] = pd.to_datetime(df_no_url['create_at'])
df_non_credible['create_at'] = pd.to_datetime(df_non_credible['create_at'])
df_mixed['create_at'] = pd.to_datetime(df_mixed['create_at'])

# Getting fact check dates
cluster = ['Post says "sanitizer will do nothing for the coronavirus."', 'Hand sanitizer will “do nothing for the coronavirus.”', 'Genefir Haller, the woman who voluntereed to try one of the COVID-19 vaccines, is dead.', 'An image of a couple claimed to be doctors who have lost their lives to the coronavirus.', '\r\nThere is no home vaccination against coronavirus in Cuba.', 'The coronavirus dies in the body in 4 days, and one would be pronounced negative for the virus by the 5th day.', 'A volunteer for Oxford coronavirus vaccine died.', 'First volunteer in UK coronavirus vaccine trial Elisa Granato has died.', 'Elisa Granato (32-year-old), the first woman to get vaccine for COVID-19, died. ', '“First volunteer in UK coronavirus vaccine trial has died.”', 'Dr. Elisa Granato, one of the first volunteers to receive a potential COVID-19 vaccine in the U.K., has died.', 'Coronavirus remains in the throat for 4 days.', 'There are no antibiotics to cure the coronavirus.', 'Coronavirus stays in the throat for four days.', 'The vaccine is not the final solution against the novel coronavirus.']
print(len(cluster))
df_fact = helper.find_dates(cluster, df_coronavirus_facts)
max_value = max([max(df_credible[0]), max(df_non_credible[0])])
df_fact['count'] = max_value

# Ploting the graph
plt.rcParams["figure.figsize"] = [15, 7]
plt.xlabel('Date')
plt.ylabel('Number of Tweets')
plt.plot(df_credible['create_at'], df_credible[0], color='green')
plt.plot(df_non_credible['create_at'], df_non_credible[0], color='#6a5e0c')
#plt.plot(df_no_url['create_at'], df_no_url[0], color='#8c387d')
plt.plot(df_mixed['create_at'], df_mixed[0], color='#1e4b95')
plt.bar(df_fact['created_at'], df_fact['count'], color='red')
plt.xticks(df_no_url.create_at[::30])
plt.legend(['credible', 'non-credible', 'mixed'])
#plt.show()
plt.savefig('cure/1_elisa_granato.pdf')