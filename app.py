import streamlit as st
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0b1020, #151b35);
    color: #f8fafc;
}

/* Main content width */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #f8fafc !important;
}

/* Input boxes and dropdowns */
.stTextInput input {
    background-color: #202944;
    color: white;
    border: 1px solid #475569;
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #202944;
    color: white;
    border-radius: 10px;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border: 1px solid #c4b5fd;
    color: white;
    transform: translateY(-2px);
}

/* Post output area */
.stTextArea textarea {
    background-color: #111827;
    color: #f8fafc;
    border: 1px solid #6366f1;
    border-radius: 10px;
    line-height: 1.6;
}

/* Success and error messages */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
import os
import streamlit.components.v1 as components
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI LinkedIn Post Generator", page_icon="🚀")

st.markdown("""
<div style="
    text-align: center;
    padding: 25px 15px;
    border: 1px solid #374151;
    border-radius: 18px;
    background: linear-gradient(135deg, #1e293b, #312e81);
    margin-bottom: 25px;
">
    <div style="font-size: 42px;">🚀</div>
    <h1 style="margin: 8px 0; color: white;">
        AI LinkedIn Post Generator
    </h1>
    <p style="color: #cbd5e1; font-size: 17px;">
        Create engaging posts in seconds with AI
    </p>
    <p style="color: #a5b4fc;">
        ✨ Choose your language • Set your tone • Generate your post
    </p>
</div>
""", unsafe_allow_html=True)


topic = st.text_input(
    "Apna topic likho",
    placeholder="AI tools for students"
)

col1, col2, col3 = st.columns(3)

with col1:
    language = st.selectbox(
        "🌐 Post ki language",
        ["Hinglish", "Hindi", "English"]
    )

with col2:
    tone = st.selectbox(
        "🎨 Post ka tone",
        ["Professional", "Friendly", "Motivational"]
    )

with col3:
    length = st.selectbox(
        "✍️ Post ki length",
        ["Short", "Medium", "Long"]
    )

if st.button("Post Banao"):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not topic.strip():
        st.warning("Pehle topic likho!")
    elif not api_key:
        st.error("API key .env file mein add karo.")
    else:
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )

            with st.spinner("Post ban rahi hai..."):
                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=[
                        {
                            "role": "user",
                            "content": (
                                f"Write an engaging LinkedIn post about {topic}. "
f"Write in {language} language. "
f"Use a {tone} tone. "
f"Make the post {length} length. "
"Use emojis, bullet points, and 3 relevant hashtags. "
"Return only the finished LinkedIn post."
                            )
                        }
                    ]
                )

            post = response.choices[0].message.content or ""

            st.success("Post taiyar hai!")
            st.text_area(
    "✨ Tumhari LinkedIn Post",
    post,
    height=350,
    help="Yahan se apni post copy ya edit kar sakte ho."
)

            safe_post = (
                post.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )

            components.html(
                f"""
                <button onclick="copyPost()"
                    style="background:#1769ff;color:white;
                    padding:10px 18px;border:0;border-radius:8px;
                    cursor:pointer;font-size:16px;">
                    📋 Copy Post
                </button>
                <span id="status" style="margin-left:10px;"></span>
                <textarea id="postText" style="position:absolute;left:-9999px;">
                </textarea>
                <script>
                const post = {__import__('json').dumps(post)};
                async function copyPost() {{
                    try {{
                        await navigator.clipboard.writeText(post);
                        document.getElementById("status").innerText =
                            "Copied!";
                    }} catch (e) {{
                        const area = document.getElementById("postText");
                        area.value = post;
                        area.style.position = "static";
                        area.select();
                        document.getElementById("status").innerText =
                            "Text select ho gaya hai; Ctrl+C dabao.";
                    }}
                }}
                </script>
                """,
                height=55
            )
            
            st.download_button(
                label="📥 Download Post",
                data=post,
                file_name="linkedin_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")