
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline


def sentimentAnalyzer(data):
    sid = SentimentIntensityAnalyzer()
    newdata = {}
    for key, value in data.items():
        newdata[key] = value
        newdata[key]['sentiments'] = sid.polarity_scores(value['text'])
    return newdata


def plotSentiments(data):
    compoundList = [value['sentiments']['compound'] for key,value in data.items()]
    df = pd.DataFrame(compoundList, columns=['compound'])
    df['message'] = [e for e in range(1,len(data.keys())+1)]
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
