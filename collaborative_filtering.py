import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds



def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.UserId == (userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'ArticleId', right_on = 'ArticleId').
                     sort_values(['TimeSpent'], ascending=False)
                 )

    print('User {0} has already read {1} articles.'.format(userID, user_full.shape[0]))
    print('Recommending the highest {0} predicted ratings articles not already read.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['ArticleId'].isin(user_full['ArticleId'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'ArticleId',
               right_on = 'ArticleId').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations




dfNews = pd.read_csv('scrappedNews.csv',encoding = "ISO-8859-1")
dfUser = pd.read_csv('UserProfileData2.csv')

R_df = dfUser.pivot_table(index = 'UserId', columns ='ArticleId', values = 'TimeSpent').fillna(0)

R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)


U, sigma, Vt = svds(R_demeaned, k = 7)
sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)


already_rated, predictions = recommend_movies(preds_df, 2, dfNews, dfUser, 10)

print("predicted Articles \n",predictions)
