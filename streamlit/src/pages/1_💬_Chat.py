import streamlit as st
import time
from components.layout.components import show_empty_container
from components.layout.styling import set_page_styling
from components.utils.helpers import reset_session_state, prepare_text_for_display, clear_results

#########################
#     COVER & CONFIG
#########################

# Assistant image URL for the avatar
ASSISTANT_AVATAR = "src/components/images/assistant_icon.png"

# Set up page configuration
st.set_page_config(
    page_title="Chat", 
    page_icon="💬", 
    layout="centered"
)

# page width, form borders, message styling
style_placeholder = st.empty()
with style_placeholder:
    set_page_styling()


#########################
#       CONSTANTS
#########################

# default hello message
HELLO_MESSAGE = "Hi! I am an AI assistant. How can I help you?"

# page name for caching
PAGE_NAME = "chat"

MODELS = [ "Model 1", "Model 2", "Model 3" ]
TEMPERATURE_DEFAULT=0.5


#########################
# SESSION STATE VARIABLES
#########################

reset_session_state(page_name=PAGE_NAME)

st.session_state.setdefault("query", "")
st.session_state.setdefault("messages_human", [{"message": "Hi"}])
st.session_state.setdefault(
    "messages_chatbot", [{"message": HELLO_MESSAGE}]
)
st.session_state.setdefault("message_idx", 0)


#########################
#    HELPER FUNCTIONS
#########################


def show_message(is_user: bool = True, idx: int = 0, include_buttons=False) -> None:  # noqa: C901
    """
    Display message in the UI

    Parameters
    ----------
    is_user : bool
        Is the message from the user?
    idx : int
        Message ID
    """

    # show human message
    if is_user:
        message_human = st.session_state["messages_human"][idx]
        with st.chat_message(name="user"):
            processed_message = prepare_text_for_display(message_human["message"])
            st.markdown(processed_message)

    # show chatbot message
    else:
        message_chatbot = st.session_state["messages_chatbot"][idx]
        response_col, thumbsup_col, thumbsdown_col = st.columns([1, 0.07, 0.07])
        with response_col:
            with st.chat_message(name="assistant", avatar=ASSISTANT_AVATAR):
                # highlight hallucinations
                message = message_chatbot["message"]

                # show LLM answer
                message = prepare_text_for_display(message)
                st.markdown(message, unsafe_allow_html=True)

def run_chat_query() -> None:
    """
    Runs API call to retrieve LLM answer and references
    """

    # update query if None
    st.session_state.setdefault("query", "")

    # display chat history
    if st.session_state["message_idx"] > 0:
        with chat_placeholder:
            for idx in range(1, len(st.session_state["messages_chatbot"])):
                show_message(is_user=True, idx=idx)
                show_message(is_user=False, idx=idx)

    # add user message
    st.session_state["messages_human"].append({"message": st.session_state["query"]})
    with chat_placeholder:
        show_message(is_user=True, idx=len(st.session_state["messages_human"]) - 1)

    # generate the answer
    if st.session_state["query"] != "" and st.session_state["query"].strip() != "":
        with chat_placeholder:
            thinking_placeholder = st.empty()
            vertical_space = show_empty_container()
            with thinking_placeholder.container():
                response_col, _, _ = st.columns([1, 0.07, 0.07])
                with response_col:
                    with st.chat_message(name="assistant", avatar=ASSISTANT_AVATAR):
                        with st.spinner("Thinking..."):
                            time.sleep(1)
                            # Generate dummy response
                            dummy_response = f"You asked: {st.session_state['query']}\nSelected Model: {st.session_state['ai_model']}\nSelected Temperature: {st.session_state['temperature']}"
                            st.session_state["messages_chatbot"].append({"message": dummy_response})
                            st.markdown(dummy_response)

            thinking_placeholder.empty()
            vertical_space.empty()

    # reset containers
    chat_placeholder.container().empty()


#########################
#        SIDEBAR
#########################

# sidebar
with st.sidebar:
    st.header("Chat Configuration")

    ai_model = st.selectbox(
        label="Model:",
        options=MODELS,
        key="ai_model",
    )
    temperature = st.slider(
        label="Temperature:",
        value=TEMPERATURE_DEFAULT,
        min_value=0.0,
        max_value=1.0,
        key="temperature",
    )


#########################
#      MAIN APP PAGE
#########################

# info banner
with st.expander(":bulb: You are interacting with Generative AI enabled system. Expand to show instructions."):
    st.markdown(
        """- This tab allows you to ask questions about your document base in a memory-enabled chat
- Please enter your question in the field below and click **"Send"** or press **"Return"** key
- Select the Model and LLM parameters using the sidebar:
    - Choose one of the available LLMs and inference parameters
- Click **"Clear chat"** to start new conversation with no chat history
"""
    )

# chat history
chat_container = st.empty()
with chat_container.container():
    chat_placeholder = st.container()
with chat_placeholder:
    show_message(is_user=False, idx=0)

# new message field
with st.form("text_input_form", clear_on_submit=True):
    text_input_col, send_button_col = st.columns([0.91, 0.09])
    with text_input_col:
        user_query = st.text_input(
            placeholder='Enter your message and press "Send"',
            label="New message:",
            label_visibility="collapsed",
            key="query",
        )
    with send_button_col:
        form_submit_button = st.form_submit_button("Send")
        if form_submit_button:
            run_chat_query()
            st.session_state["message_idx"] += 1
            chat_container.empty()

# display chat history
if st.session_state["message_idx"] > 0:
    with chat_container.container():
        st.empty()
        placeholder = st.container()
    with placeholder:
        show_message(is_user=False, idx=0)
        for idx in range(1, len(st.session_state["messages_chatbot"])):
            show_message(is_user=True, idx=idx)
            show_message(is_user=False, idx=idx, include_buttons=True)

# button to clear chat history
st.button(":wastebasket: Clear Chat", on_click=clear_results, disabled=len(st.session_state["messages_chatbot"]) == 1)