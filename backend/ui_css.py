def inject_css(st):
    st.markdown(
        """
        <style>
        /* Layout */
        .block-container { padding-top: 1.2rem; max-width: 1100px; }

        /* Chat bubbles */
        .chat-row { display:flex; gap:12px; margin: 10px 0; }
        .chat-avatar { width:34px; height:34px; border-radius:50%;
                       display:flex; align-items:center; justify-content:center;
                       background:#f2f2f2; font-weight:700; }
        .chat-bubble { padding:12px 14px; border-radius:14px; width:100%;
                       border:1px solid #eee; background:#fafafa; }
        .user .chat-avatar { background:#eaf2ff; }
        .user .chat-bubble { background:#eef6ff; border-color:#dbeafe; }
        .assistant .chat-avatar { background:#eaffef; }
        .assistant .chat-bubble { background:#f2fff6; border-color:#dcfce7; }

        /* Buttons */
        div.stButton > button { border-radius: 10px; padding: 0.6rem 1rem; }

        /* Sidebar */
        section[data-testid="stSidebar"] { border-right: 1px solid #eee; }
        </style>
        """,
        unsafe_allow_html=True,
    )
