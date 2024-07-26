import pandas as pd
import numpy as np
from preprocessing import get_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, send_from_directory, jsonify, request
from main import access_token
import logging

app = Flask(__name__, static_folder='public')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def cal_weighted_popularity(release_date):
    try:
        release_date = datetime.strptime(release_date, '%Y-%m-%d')
        time_span = datetime.now() - release_date
        return 1 / (time_span.days + 1)
    except Exception as e:
        logging.error(f"Error calculating weighted popularity: {e}")
        return 0

def normalize(music_df):
    try:
        scaler = MinMaxScaler()
        music_features = music_df[['Danceability', 'Energy', 'Key', 
                                   'Loudness', 'Mode', 'Speechiness', 'Acousticness',
                                   'Instrumentalness', 'Liveness', 'Valence', 'Tempo']].values
        music_features_scaled = scaler.fit_transform(music_features)
        return music_features_scaled
    except Exception as e:
        logging.error(f"Error normalizing data: {e}")
        return np.array([])

def content_based_recommendations(input_song_name, music_df, num_recommendations=5):
    if input_song_name not in music_df['Track Name'].values:
        logging.warning(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
        return pd.DataFrame()

    input_song_index = music_df[music_df['Track Name'] == input_song_name].index[0]

    music_features_scaled = normalize(music_df)
    if music_features_scaled.size == 0:
        return pd.DataFrame()

    similarity_scores = cosine_similarity([music_features_scaled[input_song_index]], music_features_scaled)
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:num_recommendations + 1]

    content_based_recommendations = music_df.iloc[similar_song_indices][['Track Name', 'Artists', 'Album Name', 'Release Date', 'Popularity']]
    return content_based_recommendations

def hybrid_recommendations(input_song_name, playlist_id, num_recommendations=5, alpha=0.5):
    try:
        music_df = get_data(playlist_id, access_token)
        if input_song_name not in music_df['Track Name'].values:
            logging.warning(f"'{input_song_name}' not found in the dataset. Please enter a valid song name.")
            return pd.DataFrame()
        
        content_based_rec = content_based_recommendations(input_song_name, music_df, num_recommendations)
        if content_based_rec.empty:
            return pd.DataFrame()

        popularity_score = music_df.loc[music_df['Track Name'] == input_song_name, 'Popularity'].values[0]
        weighted_popularity_score = popularity_score * cal_weighted_popularity(music_df.loc[music_df['Track Name'] == input_song_name, 'Release Date'].values[0])

        hybrid_recommendations = content_based_rec.append({
            'Track Name': input_song_name,
            'Artists': music_df.loc[music_df['Track Name'] == input_song_name, 'Artists'].values[0],
            'Album Name': music_df.loc[music_df['Track Name'] == input_song_name, 'Album Name'].values[0],
            'Release Date': music_df.loc[music_df['Track Name'] == input_song_name, 'Release Date'].values[0],
            'Popularity': weighted_popularity_score
        }, ignore_index=True)

        hybrid_recommendations = hybrid_recommendations.sort_values(by='Popularity', ascending=False)
        hybrid_recommendations = hybrid_recommendations[hybrid_recommendations['Track Name'] != input_song_name]

        return hybrid_recommendations

    except Exception as e:
        logging.error(f"Error generating hybrid recommendations: {e}")
        return pd.DataFrame()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        song_name = data.get('song_name')
        playlist_id = data.get('spotify_id')
        num_recommendations = data.get('num_recommendations', 5)

        recommendations = hybrid_recommendations(song_name, playlist_id, num_recommendations)
        if recommendations.empty:
            return jsonify({"error": "No recommendations found"}), 400

        return recommendations.to_json(orient='records')

    except Exception as e:
        logging.error(f"Error in recommend endpoint: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
