import requests
import streamlit as st
import time

st.title("Rasa Chatbot Interface")

# Change api url to yours here
url = 'https://huggingface.co/spaces/irfanp056/rasa_bot'

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send user input to Rasa webhook
    payload = {"sender": "user", "message": user_input}
    response = requests.post(url+'/webhooks/rest/webhook', json=payload)
    bot_reply = response.json()

    # Extract assistant response
    if bot_reply !=[]:
        assistant_response = bot_reply[0]["text"]
    # Handle empty api responses
    else:
        assistant_response = 'API request returned with an empty list []. Please continue with a different question'


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Add debug button to display RASA version, Model Name
with st.expander("Debug"):
    if st.button("Show Debug Info"):
        request_ids = ['/status', '/version']
        results = [requests.get(url+request_id).json() for request_id in request_ids]
        st.write(results)
    else:
        st.write("")


    