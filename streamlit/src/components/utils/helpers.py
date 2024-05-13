import streamlit as st

def prepare_text_for_display(text: str) -> str:
    # currently just removes simple inline math mode latex
    return remove_inline_math_mode(text=text)


def remove_inline_math_mode(text: str) -> str:
    """
    Removes "inline math mode" delimiter; keeps "math mode" delimiter

    This function replaces "$" with the symbol equivalent for st.markdown() display.
    Keeps "$$" for displaying latex blocks

    Parameters
    ----------
    text : list
        text to prepare for display

    Returns
    -------
    str
        prepared string
    """
    # Replace all dollar signs first and then revert $$ replacements for LaTeX blocks
    safe_text = text.replace("$", "&#36;")
    return safe_text.replace("&#36;&#36;", "$$")

def reset_session_state(page_name: str) -> None:
    """
    Reset st.session_state variables

    Parameters
    ----------
    page_name : str
        Name of the current UI page
    """

    st.session_state.setdefault("last_page", "None")

    st.session_state["current_page"] = page_name
    if st.session_state["current_page"] != st.session_state["last_page"]:
        for key in st.session_state.keys():
            if key not in [
                "authenticated",
                "access_token",
                "css_code",
                "user_id",
                "user_cognito_groups",
                "selected_prompt",
                "vector_indices",
            ]:
                del st.session_state[key]

    st.session_state["last_page"] = page_name

def clear_results() -> None:
    """
    Clear model response, retriever response, and chat history
    """
    st.session_state["query"] = ""
    if "messages_chatbot" in st.session_state:  # corresponds to chat tab
        st.session_state["messages_human"] = [st.session_state["messages_human"][0]]
        st.session_state["messages_chatbot"] = [st.session_state["messages_chatbot"][0]]
        st.session_state["message_idx"] = 0