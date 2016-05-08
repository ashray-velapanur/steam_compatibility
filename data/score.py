from model.user import User
from model.game import Game
from model.genre import mapping

import logging

BUCKETS = [4.0, 8.0]
BUCKET_SCORES = [10.0, 30.0, 50.0]


def genre_scores(genres):
    genre_scores = {}
    for genre in genres:
        if not genre in genre_scores:
            genre_scores[genre] = 0
        genre_scores[genre] +=1
    return genre_scores

def make_buckets(genre_scores):
    buckets = {}
    for genre, score in genre_scores.iteritems():
        score = float(score)
        if score < BUCKETS[0]:
            buckets[genre] = 1
        elif score >= BUCKETS[0] and score < BUCKETS[1]:
            buckets[genre] = 2
        elif score >= BUCKETS[1]:
            buckets[genre] = 3
    return buckets

def compatibility(genre_scores_1, genre_scores_2):
    user_1_buckets = make_buckets(genre_scores_1)
    user_2_buckets = make_buckets(genre_scores_2)
    compatibility_score = 0.0
    for genre, score in user_1_buckets.iteritems():
        if genre in user_2_buckets:
            if abs(score - user_2_buckets[genre]) == 0:
                compatibility_score += BUCKET_SCORES[2]
            elif abs(score - user_2_buckets[genre]) == 1:
                compatibility_score += BUCKET_SCORES[1]
            elif abs(score - user_2_buckets[genre]) == 2:
                compatibility_score += BUCKET_SCORES[0]
    return compatibility_score 

def score_percentages(genre_scores):
    total = 0.0
    percentages = {}
    for genre, score in genre_scores.iteritems():
        total += float(score)
    for genre, score in genre_scores.iteritems():
        percentages[genre] = 100.0*score/total
    return percentages

def compatibility_percentages(user_genre_scores, friend_genre_scores):
    user_percentages = score_percentages(user_genre_scores)
    friend_percentages = score_percentages(friend_genre_scores)
    common_genres = []
    compatibility_score = 0.0
    for genre in user_percentages.viewkeys() & friend_percentages.viewkeys():
        common_genres.append(genre)
    if len(common_genres) > 0:
        for genre in common_genres:
            compatibility_score += (100.0 - abs(user_percentages[genre] - friend_percentages[genre]))
        compatibility_score = compatibility_score/len(common_genres)            
    return compatibility_score
