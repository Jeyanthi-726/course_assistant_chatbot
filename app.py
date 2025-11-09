from utils.web_utils import web_search
import streamlit as st
import os
from PyPDF2 import PdfReader
import io
from models.llm import get_chatgroq_model

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model"""
    try:
        # Prepare messages for the model
        formatted_messages = [SystemMessage(content=system_prompt)]
        
        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        # Get response from model
        response = chat_model.invoke(formatted_messages)
        return response.content
    
    except Exception as e:
        return f"Error getting response: {str(e)}"
    
def instructions_page():
    """Instructions and setup page"""
    st.title("The Course Assistant Chatbot")
    st.markdown("Welcome! Follow these instructions to use the chatbot.")
    
    st.markdown("""
## How to Use

1. **Go to the Chat page** (use the sidebar to navigate)
2. **Upload your course PDF** if you want the assistant to reference your materials.
3. **Type your question** in the chat input box.
4. **Choose Explanation**: Select **Concise** for short answers or **Detailed** for in-depth responses.
5. **Clear Chat History**: Use the button at the bottom of the sidebar to start fresh.

## Tips

- **System Prompts**: Customize the AI's personality and behavior.
- **Chat History**: Persists during your session but resets on refresh.

## Troubleshooting

- **Connection Errors**: Verify your internet connection.
- **No Answer **: Ensure your PDF is uploaded correctly or try rephrasing your question.

---

Ready to start chatting? Navigate to the **Chat** page using the sidebar!
""")


# chat_page()
def chat_page():
    """Main chat interface page"""
    st.title("📚 Course Assistant")

    system_prompt = """You are an Course Assistant.
    Use the provided course materials to answer student questions.
    If not available, use web search to find accurate, up-to-date answers."""

    chat_model = get_chatgroq_model()

#     # === Sidebar options ===
    with st.sidebar:
        st.subheader("Choose Explanation")
        response_mode = st.radio( "Answer ",["Concise", "Detailed"])
        st.divider()
        uploaded_file = st.file_uploader("Upload Course File", type=["pdf"])
    
        if uploaded_file:
        # Read bytes directly from memory
            file_bytes = uploaded_file.read()
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # st.write("Extracted text:", text[:500])
            st.session_state["doc_text"] = text
            st.success("PDF uploaded successfully and ready for Q&A!")
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Getting response..."):
                if "doc_text" in st.session_state:
                    context = st.session_state["doc_text"]
                    combined_prompt = f"Document Context:\n{context}\n\nQuestion: {prompt}"
                else:
                    st.info("🔍 No local info found. Searching the web...")
                    context = web_search(prompt)
                    combined_prompt = f"External Info:\n{context}\n\nQuestion: {prompt}"

                if response_mode == "Concise":
                    combined_prompt += "\nPlease give a short and focused answer."
                else:
                    combined_prompt += "\nPlease give a detailed explanation."

                response = get_chat_response(chat_model, st.session_state.messages, combined_prompt)
                st.markdown(response)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    st.set_page_config(
        page_title="Course Assistant ChatBot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    with st.sidebar:
        st.title("Pages")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions"],
            index=0
        )
        
    
    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    if page == "Chat":
        chat_page()

if __name__ == "__main__":
    main()
