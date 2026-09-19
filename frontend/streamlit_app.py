import os
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st


# Configuration
def get_api_url() -> str:
    try:
        url = st.secrets.get('API_URL')
    except Exception:
        url = None
    return url or os.environ.get('API_URL') or 'http://localhost:8001'


API_URL = get_api_url()

st.set_page_config(page_title="Planner", layout="wide")
st.markdown('# Minimal B&W Planner')


# --- API helpers -----------------------------------------------------------


@st.cache_data(ttl=30)
def fetch_notes(api_url: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Fetch notes from the backend.

    Returns (notes, error_message). On success, error_message is None.
    """
    try:
        resp = requests.get(f"{api_url}/notes", timeout=5)
    except requests.exceptions.RequestException as e:
        return [], f"Failed to fetch notes: {e}"

    if not resp.ok:
        return [], f"Failed to fetch notes (status {resp.status_code})"

    text = resp.text.strip()
    if not text:
        return [], 'API returned empty response for notes'

    try:
        data = resp.json()
    except ValueError:
        excerpt = resp.text.strip()[:200]
        return [], f'API returned invalid JSON for notes: {excerpt}'

    if isinstance(data, list):
        return data, None
    if isinstance(data, dict) and 'notes' in data and isinstance(data['notes'], list):
        return data['notes'], None

    return [], 'API returned unexpected JSON structure for notes'


def add_note(api_url: str, title: str, body: str) -> Optional[str]:
    """Add a note. Returns None on success or an error message on failure."""
    payload = {"title": title, "body": body}
    try:
        resp = requests.post(f"{api_url}/notes", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        return f"Failed to add note: {e}"

    if resp.ok:
        # Attempt to clear cached data so new note appears immediately.
        try:
            st.cache_data.clear()
        except Exception:
            pass
        return None

    text = resp.text.strip()
    return f"Failed to add note (status {resp.status_code}): {text[:200]}"


# --- UI --------------------------------------------------------------------

nav = st.sidebar.radio('Go to', ['Notes', 'Schedule', 'Trackers', 'About'])


if nav == 'Notes':
    st.header('Notes')

    with st.form('add_note'):
        title = st.text_input('Title')
        body = st.text_area('Body')
        submit = st.form_submit_button('Add Note')

    if submit:
        if not title.strip():
            st.error('Title is required')
        else:
            with st.spinner('Adding note...'):
                err = add_note(API_URL, title.strip(), body.strip())
            if err:
                st.error(err)
            else:
                st.success('Note added')

    with st.spinner('Loading notes...'):
        notes,fetch_err = fetch_notes(API_URL)
        st.info(notes)

    if fetch_err:
        st.error(fetch_err)
    else:
        if notes:
            for n in notes:
                st.subheader(n.get('title', ''))
                st.write(n.get('body', ''))
        else:
            st.info('No notes yet')


elif nav == 'Schedule':
    st.header('Schedule')
    st.write('Schedule UI will go here')


elif nav == 'Trackers':
    st.header('Trackers')
    st.write('Trackers UI will go here')


else:
    st.header('About')
    st.write('Black-and-white planner using Streamlit + FastAPI + Postgres')
