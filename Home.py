import streamlit as st
import pandas as pd
import pickle
import numpy as np 

# Load the pickle file containing book data
with open('Book2.pkl', 'rb') as file:
    books_data = pickle.load(file)
with open('popular_books.pkl', 'rb') as file:
    popular_books = pickle.load(file)
with open('pt.pkl', 'rb') as file:
    pt = pickle.load(file)
with open('similarity_scores.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)

# Function to recommend books
def recommend_books(input_title):
    # Find books that partially match the input title
    matching_books = books_data[books_data['Book-Title'].str.contains(input_title, case=False)]
    index = np.where(pt.index == input_title)[0][0]

    # Calculate similarity scores between the input book and other books
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    # Create a list to store recommended books
    recommended_books = []

    for i, score in similar_items:
        # Get the book title, author, and image URL from 'books_data'
        title = pt.index[i]
        author = books_data.loc[books_data['Book-Title'] == title, 'Book-Author'].iloc[0]
        image_url = books_data.loc[books_data['Book-Title'] == title, 'Image-URL-M'].iloc[0]

        # Append book details to the 'recommended_books' list
        recommended_books.append((title, author, image_url))

    return recommended_books

# Streamlit app
def main():
    st.title('Book Recommendation App')

    # Input field for book title
    input_title = st.text_input('Enter a book title:')
    
    # Recommend button
    if st.button('Recommend'):
        if input_title:
            recommended_books = recommend_books(input_title)
            display_recommendations(recommended_books)

import pandas as pd

def display_recommendations(recommended_books):
    if not recommended_books:
        st.warning("No recommendations found for the given book.")
        return

    st.header("Recommended Books:")

    # Use CSS to style the image size and layout
    st.markdown(
        """
        <style>
        .book-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom: 10px;
        }
        .book-image {
            flex: 0.3;
            max-width: 100px;
            max-height: 150px;
            object-fit: cover;
            margin-right: 10px;
        }
        .book-details {
            flex: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for book_info in recommended_books:
        book = book_info  # Each book_info is a list representing the book details
        st.markdown(f'<div class="book-container">', unsafe_allow_html=True)
        st.image(book[2], use_column_width=False, caption=book[0], output_format='JPEG')
        st.markdown('<div class="book-details">', unsafe_allow_html=True)
        st.write(f"**Title:** {book[0]}")
        st.write(f"**Author:** {book[1]}")
        st.markdown('</div></div>', unsafe_allow_html=True)
        st.markdown("---")

if __name__ == '__main__':
    main()
