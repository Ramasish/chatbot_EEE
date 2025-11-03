import streamlit as st
from orchestrator import orchestrate
from PIL import Image
import base64
import io

# Set page config
st.set_page_config(
    page_title="Power System Analysis Chatbot",
    page_icon="⚡",
    layout="centered"
)

# Add title and description
st.title("⚡ Power System Analysis Chatbot")
st.markdown("""
This chatbot can help you with:
- Power Flow Analysis
- Bus Voltage Calculations
- System Loss Analysis
- General Power System Questions
- Image Analysis (Upload images to ask questions about them)
""")

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def format_conversation_history(messages, max_messages=6):
    """Convert Streamlit message format to Groq API format. Returns last max_messages."""
    if not messages:
        return []
    
    # Take last max_messages
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
    
    formatted_history = []
    for msg in recent_messages:
        role = msg["role"]
        content = msg["content"]
        
        # Handle different content formats
        if isinstance(content, dict):
            # Message with image
            if "text" in content and "image" in content:
                # For history, we'll store the text only (images are only for current query)
                formatted_history.append({
                    "role": role,
                    "content": content["text"]
                })
            elif "text" in content:
                formatted_history.append({
                    "role": role,
                    "content": content["text"]
                })
        else:
            # Plain text message
            formatted_history.append({
                "role": role,
                "content": content
            })
    
    return formatted_history

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict):
            # Handle messages with images
            if "text" in message["content"]:
                st.markdown(message["content"]["text"])
            if "image" in message["content"]:
                st.image(message["content"]["image"], caption="Uploaded Image", use_column_width=True)
        else:
            st.markdown(message["content"])

# Image upload section
with st.expander("📷 Upload Image (Optional)", expanded=False):
    uploaded_image = st.file_uploader(
        "Choose an image to analyze",
        type=["jpg", "jpeg", "png", "gif", "bmp", "webp"],
        help="Upload an image to ask questions about it"
    )
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Preview", use_column_width=True)
        st.session_state.current_image = image
        st.session_state.current_image_base64 = encode_image_to_base64(image)
    else:
        if "current_image" in st.session_state:
            del st.session_state.current_image
        if "current_image_base64" in st.session_state:
            del st.session_state.current_image_base64

# Chat input
if prompt := st.chat_input("Ask your question here..."):
    # Prepare message content
    user_message_content = prompt
    user_message_for_history = {"role": "user", "content": prompt}
    
    # Check if there's an image
    image_base64 = None
    if "current_image" in st.session_state:
        image_base64 = st.session_state.current_image_base64
        # Display user message with image
        with st.chat_message("user"):
            st.markdown(prompt)
            st.image(st.session_state.current_image, caption="Uploaded Image", use_column_width=True)
        # Add image to message history
        user_message_for_history = {
            "role": "user",
            "content": {
                "text": prompt,
                "image": st.session_state.current_image
            }
        }
    else:
        # Display user message without image
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Add user message to history
    st.session_state.messages.append(user_message_for_history)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Get last 6 messages (excluding current user message) for context
            conversation_history = format_conversation_history(st.session_state.messages[:-1], max_messages=6)
            response = orchestrate(prompt, image_base64=image_base64, conversation_history=conversation_history)
            st.markdown(response)
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear image after use (optional - comment out if you want to keep image for multiple queries)
    # if "current_image" in st.session_state:
    #     del st.session_state.current_image
    #     del st.session_state.current_image_base64

# Add sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This chatbot uses advanced AI to help with power system analysis tasks. It can:
    
    1. Solve power flow problems
    2. Calculate system losses
    3. Answer general power system questions
    4. Provide web search results for broader topics
    5. Analyze images (upload images to ask questions about them)
    
    Simply type your question in the chat input and get instant responses!
    
    **Image Analysis**: Upload an image using the expandable section above to ask questions about it. Perfect for analyzing power system diagrams, circuit schematics, or any technical images!
    """)
    
    # Add citation
    st.markdown("---")
    st.markdown("Made with ❤️ by Power Systems Team")