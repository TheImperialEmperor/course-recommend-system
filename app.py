from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from markupsafe import escape

app = Flask(__name__)

# Load the preprocessed DataFrames
df_cleaned = pickle.load(open('df_cleaned.pkl', 'rb'))
popular_df = pickle.load(open('popular_df.pkl', 'rb'))
popular_courses = pickle.load(open('popular_courses.pkl', 'rb'))  # Load the popular courses

# Vectorize the course descriptions using TF-IDF (loaded globally for efficiency)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_cleaned['course description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend courses based on keyword
def recommend_courses_by_keyword(keyword, df, num_courses=6):
    relevant_courses = df[df['course_name'].str.contains(keyword, case=False)]
    sorted_courses = relevant_courses.sort_values(by='rating', ascending=False)
    if relevant_courses.empty:
        return None
    return sorted_courses.head(num_courses)[['course_name', 'course url']]

# Function to recommend courses based on course description similarity
def recommend_courses_by_description(course_name, df, cosine_sim, num_courses=6):
    if course_name not in df['course_name'].values:
        return None
    try:
        idx = df[df['course_name'] == course_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:min(len(sim_scores), num_courses + 1)]
        course_indices = [i[0] for i in sim_scores]
        return df.iloc[course_indices][['course_name', 'course url']]
    except IndexError:
        return None

@app.route('/')
def index():
    # Display the most popular courses on the homepage
    return render_template('index.html', courses=popular_df)

@app.route('/recommend', methods=['POST'])
def recommend():
    keyword = escape(request.form.get('keyword'))
    recommended_courses = recommend_courses_by_keyword(keyword, df_cleaned)

    if recommended_courses is None:
        return render_template('error.html', message=f"No courses found for keyword '{keyword}'")
    
    return render_template('recommend.html', keyword=keyword, courses=recommended_courses)

@app.route('/recommend_by_description', methods=['POST'])
def recommend_by_description():
    course_name = escape(request.form.get('course_name'))
    recommended_courses = recommend_courses_by_description(course_name, df_cleaned, cosine_sim)

    if recommended_courses is None:
        return render_template('error.html', message=f"No courses found for '{course_name}'")
    
    return render_template('recommend_description.html', course_name=course_name, courses=recommended_courses)

@app.route('/index_popular')
def index_popular():
    # Display popular courses based on the `popular_courses.pkl` file
    return render_template('index_popular.html', courses=popular_courses)

if __name__ == '__main__':
    app.run(debug=True)
