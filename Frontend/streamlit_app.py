import streamlit as st

# Placeholder data for trending topics (mock data, since backend isn't ready)
TRENDING_TOPICS = [
    'Global Warming Awareness',
    'Space Exploration 2025',
    'Artificial Intelligence in Medicine',
    'Sports Event in 2025',
    'Python vs JavaScript Debate',
    'Stock Market Trends for 2025',
    'Metaverse: The Future of Socializing',
    'Electric Cars: The New Revolution',
]

# Function to simulate chatbot responses based on topic
def get_bot_response(topic, user_input):
    # Placeholder response logic
    if 'AI' in topic:
        return "Artificial Intelligence is revolutionizing various sectors like healthcare, finance, and more."
    elif 'Space' in topic:
        return "Space exploration in 2025 will focus on Mars missions and satellite technology advancements."
    elif 'Stock' in topic:
        return "The stock market in 2025 is expected to be volatile, with AI-driven trading strategies becoming more popular."
    else:
        return f"Here's some information about {topic}. You can ask me more specific questions!"

# Streamlit User Interface
st.title('Chatbot: Trending Topics on Twitter')

# Display a dropdown list of trending topics
st.subheader('Select a Trending Topic:')
selected_topic = st.selectbox("Choose a topic", TRENDING_TOPICS)

# Display a text input box for user interaction with the chatbot
st.subheader(f"Chat about '{selected_topic}'")

# User input
user_input = st.text_input("Ask a question or make a comment:")

# If user has provided input, generate a response
if user_input:
    bot_response = get_bot_response(selected_topic, user_input)
    st.write(f"Bot: {bot_response}")

# Placeholder information (for when backend is connected)
st.write("This is a simple chatbot interface. Once the backend is ready, you can chat with real-time trending topics from Twitter!")
