import os
import asyncio
import streamlit as st
from app.agent import run_github_agent

st.set_page_config(page_title="GitHub MCP Agent", page_icon="🐙")

st.title("🐙 GitHub MCP Agent")

with st.sidebar:
    openai_key = st.text_input("OpenAI API Key", type="password")
    github_token = st.text_input("GitHub Token", type="password")

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key

    if github_token:
        os.environ["GITHUB_TOKEN"] = github_token

repo = st.text_input(
    "Repository",
    value="Shubhamsaboo/awesome-llm-apps"
)

query = st.text_area("Query")

if st.button("Run Query"):

    if repo not in query:
        query = f"{query} in {repo}"

    with st.spinner("Analyzing repository..."):
        result = asyncio.run(run_github_agent(query))

    st.markdown(result)