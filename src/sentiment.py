
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')
from statistics import mean
import pandas as pd
import os

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import webbrowser


def sentimentAnalyzer(data):
    sid = SentimentIntensityAnalyzer()
    newdata = {}
    newdata['messages'] = {}
    for key, value in data.items():
        newdata['messages'][key] = value
        newdata['messages'][key]['sentiments'] = sid.polarity_scores(value['text'])
    newdata['chat_sentiment_analysis'] = {'mean_neg': mean([value['sentiments']['neg'] for value in newdata['messages'].values()]),
                                         'mean_neu': mean([value['sentiments']['neu'] for value in newdata['messages'].values()]), 
                                         'mean_pos': mean([value['sentiments']['pos'] for value in newdata['messages'].values()]), 
                                         'mean_compound': mean([value['sentiments']['compound'] for value in newdata['messages'].values()])}
    return newdata


'''
def plotSentiments(data):
    compoundList = [value['sentiments']['compound'] for key,value in data['messages'].items()]
    df = pd.DataFrame(compoundList, columns=['compound'])
    df['message'] = [e for e in range(1,len(data['messages'].keys())+1)]
    df['sentiments'] = ['positive' if e > 0 else ('negative' if e < 0 else 'neutral') for e in compoundList]
    sns.set(style="white")
    sns.set_palette("deep")
    g = sns.lmplot(x = 'message', y= 'compound', hue='sentiments', data=df, fit_reg=False,
    palette = {'neutral':'royalblue','positive':'limegreen','negative':'indianred'})
    h = sns.regplot(x = 'message', y= 'compound', data=df, scatter=False, ax=g.axes[0, 0],color='orange',
    ci=None)
    g._legend.remove()
    h.set_title('Sentiment analysis')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig('./output/sentiments_chart.png', dpi=300, bbox_inches='tight')
    url = "file://{}{}{}".format(str(Path(os.getcwd())),"/output", "/sentiments_chart.png")
    webbrowser.open(url, 2)
'''