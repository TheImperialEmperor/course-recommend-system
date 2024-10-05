# Course Recommendation System

This Flask web application provides users with a platform to find popular courses and receive course recommendations based on keyword searches. The app leverages a content-based filtering approach, utilizing preprocessed course data to suggest relevant courses that match user preferences. It also features sections with courses that have high ratings and reviews.

## Features

- **Popular Courses**: Displays the most popular courses, sorted by rating, across different categories.
- **Keyword-based Course Recommendations**: Users can search for courses by entering a keyword, and the app will suggest top-rated courses related to the keyword.
- **Multiple Sections**: The app offers multiple pages displaying different sets of popular courses.

## Installation and Setup

1. Clone this repository to your local machine.
2. Ensure you have Python and the required dependencies installed. You can install the required packages using:

   ```bash
   pip install flask pandas

  Download or prepare the required preprocessed course data as df.pkl, popular_df.pkl, popular_df2.pkl, and popular_df3.pkl and place them in the project directory.

3. Run the Flask application with:

   ```bash
    python app.py
  Access the app in your browser at http://127.0.0.1:5000/.


