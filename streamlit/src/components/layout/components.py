import streamlit as st


def show_empty_container(height: int = 100) -> st.container:
    """
    Display empty container to hide UI elements below while thinking

    Parameters
    ----------
    height : int
        Height of the container (number of lines)

    Returns
    -------
    st.container
        Container with large vertical space
    """
    empty_placeholder = st.empty()
    with empty_placeholder.container():
        st.markdown("<br>" * height, unsafe_allow_html=True)
    return empty_placeholder