from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import random

app = Flask(__name__)

# CSV 파일 읽기
movies_df = pd.read_csv('movies.csv', encoding='utf-8')
clusters_df = pd.read_csv('clusters.csv', encoding='utf-8')

# TMDB API 키
api_key = '754f5471c658e0258303c4355dc672dc'

def get_movie_info_from_tmdb(movie_title):
    """TMDB에서 영화 정보를 검색하여 반환"""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=ko-KR&query={movie_title}"
    response = requests.get(url).json()
    if response['results']:
        return response['results'][0]
    return None


# 영화 추천 함수
def get_recommendations(movie_title, num_recommendations=5):
    movie = movies_df[movies_df['title'].str.contains(movie_title, case=False, na=False)]
    if movie.empty:
        return None, None, None

    movie_index = movie.iloc[0]['index']
    cluster_number = clusters_df[clusters_df['movie_indices'].str.contains(str(movie_index), na=False)]['cluster_number'].iloc[0]

    movie_indices = clusters_df[clusters_df['cluster_number'] == cluster_number]['movie_indices'].iloc[0]
    movie_indices = [int(idx.strip()) for idx in movie_indices.split(',') if idx.strip().isdigit()]

    recommendations = movies_df[movies_df['index'].isin(movie_indices)]
    if len(recommendations) > num_recommendations:
        recommendations = recommendations.sample(n=num_recommendations)

    movie_info = movie.iloc[0].to_dict()
    movie_info['poster_path'] = get_movie_info_from_tmdb(movie_info['title'])['poster_path'] if get_movie_info_from_tmdb(movie_info['title']) else None
    return movie_info, cluster_number, recommendations

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    movie_title = request.form['movie_title']
    movie_info, cluster_number, recommendations = get_recommendations(movie_title)

    if movie_info is None:
        return render_template('results.html', error="아쉽지만, 해당 영화를 찾을 수 없습니다..")

    # TMDB API를 통해 추가 정보 및 포스터 가져오기
    def get_movie_data(movie_title):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=ko-KR&query={movie_title}"
        response = requests.get(url)
        data = response.json()
        return data['results'][0] if data['results'] else None

    results = []
    for _, row in recommendations.iterrows():
        movie_data = get_movie_data(row['title'])
        if movie_data:
            results.append({
                'title': movie_data['title'],
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data['poster_path'] else None
            })

    return render_template('results.html', movie_title=movie_title, movie_info=movie_info, cluster_number=cluster_number, recommendations=results)

if __name__ == '__main__':
    app.run(debug=True)
