import pandas as pd
import pickle

# Load the dataset
data = pd.read_csv("data.csv")
df= data
df.head(5)
df.shape
df.info()
df.isnull().sum()
df.dropna(inplace=True)
# Clean and preprocess the data
df = df[['course_name', 'instructor', 'course url', 'reviews_avg','course description']]
# Extract numerical ratings from 'reviews_avg' column
df['rating'] = df['reviews_avg'].str.extract(r'(\d+\.\d+)')
df['rating'] = df['rating'].astype(float)

# Drop rows with missing values in 'rating' column
df = df.dropna(subset=['rating'])
# Display the first few rows of the preprocessed DataFrame
df.head(5)
# Drop rows with missing values in the 'course_name' and 'reviews_avg' columns
df_cleaned = df.dropna(subset=['course_name', 'reviews_avg','course description'])
# Extract ratings from the 'reviews_avg' column and convert them to numeric
df_cleaned['rating'] = df_cleaned['reviews_avg'].str.extract('(\d+\.\d+)', expand=False).astype(float)

df=df.drop(['reviews_avg'],axis=1)
df_cleaned.head(10)
def recommend_courses_by_keyword(keyword, df, num_courses=5):
    # Filter courses based on whether their name contains the keyword
    relevant_courses = df[df['course_name'].str.contains(keyword, case=False)]

    # Sort relevant courses by ratings in descending order
    sorted_courses = relevant_courses.sort_values(by='rating', ascending=False)

    # Get top courses
    top_courses = sorted_courses.head(num_courses)
    tpc = top_courses[['course_name','course url']]
    return tpc

def get_popular_courses(df, min_ratings=50, n=5):
    # Ensure that 'rating' and 'reviews_count' are numeric
    df['reviews_avg'] = pd.to_numeric(df['reviews_avg'], errors='coerce')
    df['reviews_count'] = pd.to_numeric(df['reviews_count'], errors='coerce')

    # Drop rows where 'rating' or 'reviews_count' is NaN
    df_cleaned = df.dropna(subset=['reviews_avg', 'reviews_count'])
    # Filter courses by minimum reviews count and calculate average ratings
    popular_courses = df.groupby('course_name').agg({
        'reviews_avg': 'mean',
        'reviews_count': 'sum'  # or 'count', depending on what reviews_count represents
    }).reset_index()

    # Filter courses based on minimum ratings
    popular_courses = popular_courses[popular_courses['reviews_count'] >= min_ratings]

    # Sort by average rating in descending order
    popular_courses = popular_courses.sort_values(by='reviews_avg', ascending=False)
    
    return popular_courses.head(n)

# Test the recommendation function with different keywords
keywords = [ 'java']
for keyword in keywords:
    recommended_courses = recommend_courses_by_keyword(keyword, df_cleaned)
    print(f"\nTop courses related to '{keyword}':")
    print(recommended_courses)

popular_courses = get_popular_courses(data)
pickle.dump(df,open('df.pkl','wb'))
data.head(3)
data.dropna(inplace=True)
popular_df = data[['course_name','course url','course description','reviews_avg','reviews_count']]
popular_df['reviews_avg']=popular_df['reviews_avg'].astype(float)
popular_df['reviews_count']=popular_df['reviews_count'].astype(float)
popular_df = data[data['reviews_count']>=20000].sort_values('reviews_avg',ascending=False).head(50)
popular_df2 = data[data['reviews_count']>=500].sort_values('reviews_avg',ascending=False).head(50)
popular_df3 = data[data['reviews_count']>=20000].sort_values('reviews_avg',ascending=False).tail(50)
popular_df
popular_df2
popular_df.shape
pickle.dump(popular_courses, open('popular_courses.pkl', 'wb'))
pickle.dump(popular_df,open('popular_df.pkl','wb'))
pickle.dump(popular_df2,open('popular_df2.pkl','wb'))
pickle.dump(popular_df3,open('popular_df3.pkl','wb'))