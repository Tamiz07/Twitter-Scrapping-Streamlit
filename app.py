import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import requests
from streamlit_lottie import st_lottie

tweets_df = pd.DataFrame()
st.set_page_config(page_title='Twitter scraper', page_icon=':iphone:', layout='wide', initial_sidebar_state='expanded')
st.subheader("""
Let's scrape some Tweets... Hope Twitter doesn't ban me :smile:
""")

option = st.selectbox('How would you like the data to be searched?', ('Keyword', 'Hashtag'))
word = st.text_input('Please enter a hashtag :hash:', 'Messi')
start = st.date_input("Select the start date :date:", datetime.date(2022, 1, 1), key='d1')
end = st.date_input("Select the end date :date:", datetime.date(2023, 1, 1), key='d2')
tweet_c = st.slider('How many tweets to scrape', 0, 1000, 5, key='slider1')
tweets_list = []

# SCRAPE DATA USING TwitterSearchScraper
if word:
    if option == 'Keyword':
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i >= tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.user.username, tweet.replyCount,
                                tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'Source', 'Url'])
    else:
        for i, tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i > tweet_c:
                break
            tweets_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.user.username, tweet.replyCount,
                                tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])
        tweets_df = pd.DataFrame(tweets_list,
                                 columns=['ID', 'Date', 'Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount',
                                          'LikeCount', 'Source', 'Url'])
else:
    st.warning(option, ' cant be empty', icon="⚠️")


# SIDEBAR
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

with st.sidebar:
    st.info('DETAILS', icon="ℹ️")
    if option == 'Keyword':
        st.info('Keyword is ' + word)
    else:
        st.info('Hashtag is ' + word)
    st.info('Starting Date is ' + str(start))
    st.info('End Date is ' + str(end))
    st.info("Number of Tweets " + str(tweet_c))
    st_lottie(lottie_coding, height=175, key='coding')


# DOWNLOAD AS CSV
@st.cache_data()  # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):
    return df.to_csv().encode('utf-8')


if not tweets_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = convert_df(tweets_df)  # CSV
        c = st.download_button(label="Download data as CSV", data=csv, file_name='Twitter_data.csv', mime='text/csv', )
    with col2:  # JSON
        json_string = tweets_df.to_json(orient='records')
        j = st.download_button(label="Download data as JSON", file_name="Twitter_data.json", mime="application/json",
                               data=json_string, )

    with col3:  # SHOW
        y = st.button('Show Tweets', key=2)

if c:
    st.success("The Scraped Data is Downloaded as .CSV file:", icon="✅")
if j:
    st.success("The Scraped Data is Downloaded as .JSON file", icon="✅")
if y:  # DISPLAY
    st.balloons()
    st.success("Tweets Scraped Successfully:", icon="✅")
    st.write(tweets_df)
