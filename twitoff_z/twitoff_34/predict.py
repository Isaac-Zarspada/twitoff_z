from .models import User
from sklearn.linear_model import LogisticRegression
import numpy as np
from .twitter import vectorize_tweet


def  predict_user(user0_username, user1_username, hypo_tweet_text):
    '''determines which user (user1 or user0) 
    is more likely to say a given tweet(hypo_tweet_text)'''

    # query the two user's word embedding
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # get the word embeddings of the tweets of both users 0 and 1
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # creating x matric for training logistic regression model
    vects = np.vstack([user0_vects, user1_vects])
    
    # create np array to indicate which user
    # is believed to be the author of word embedding

    labels = np.concatenate([np.zeros(len(user0.tweets)),
                             np.ones(len(user1.tweets))])

    log_r = LogisticRegression()
    # train logistic regression
    log_r.fit(vects, labels)

    # retrieving word embeddings for the indicated tweet
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    prediction = log_r.predict([hypo_tweet_vect])

    return prediction[0]


