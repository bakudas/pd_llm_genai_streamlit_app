import streamlit as st
import pandas as pd

from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

template = """

"""


def main():
    # Configure Streamlit page
    st.set_page_config(page_title="Game Design Companion", layout="wide")

    # Prompt template for generating project ideas
    idea_template = """
        You are a creative assistant. Generate a project idea based on the following details:
        Project Name: {project_name}
        Description: {project_description}
        Mechanics: {project_mechanics}
        Target Audience: {project_target_audience}
    """

    prompt = PromptTemplate(input_variables=["project_name", "project_description", "project_mechanics", "project_target_audience"], template=idea_template)

    # JSON
    llm = ChatOllama(model="llama3.1",
                    format="json",
                    temperature=0.9)

    json_chain = prompt | llm | StrOutputParser()

    projects_data = pd.DataFrame({
        'Project Name': ['Project 1', 'Project 2', 'gold arcade	'],
        'Description': ['This is the first project', 'This is the second project', 'um jogo de golf arcade jogado em uma versão 2d plataforma'],
        'Mechanics': ['Mechanics 1', 'Mechanics 2', 'o jogador joga com a bola como se fosse um jogo de plataforma normal. o personagem é a bola.	'],
        'Target Audience': ['Target Audience 1', 'Target Audience 2', '15 a 30 anos, que gostam de jogo de plataforma e temática de esporte'],
    })

    st.title('Game Design Companion')
    st.write('Welcome to the Game Design Companion! This app is designed to help you design your own game. You can use the tools provided to create your own game, and then play it with your friends. Have fun!')

    st.header('Your Projects')
    st.write('Here are your current projects:')

    st.sidebar.header('Create a New Project')
    project_name = st.sidebar.text_input('Project Name')
    project_description = st.sidebar.text_area('Project Description')
    project_mechanics = st.sidebar.text_input('Project Mechanics')
    project_target_audience = st.sidebar.text_input('Target Audience')

    if st.sidebar.button('Create Project'):
        projects_data.loc[len(projects_data)] = {
            'Project Name': project_name,
            'Description': project_description,
            'Mechanics': project_mechanics,
            'Target Audience': project_target_audience
            }
        st.sidebar.success('Project created successfully!')

    if st.sidebar.button('Generate Random Idea via LLM'):
        response = json_chain.invoke({
            "project_name": "create a random, cool and epic name to the game project",
            "project_description": "create a random, cool and exciting description for the game project",
            "project_mechanics": "create a random, fun and engaging mechanics for the game project",
            "project_target_audience": "create a random target audience for the game project"
        })

        #st.sidebar.text_area('Generated Idea', value=response, height=200)
        st.write(response)

        st.sidebar.success('New project generated successfully!')

        if st.sidebar.button("Create ideas for the game project"):

            st.success('Ideas created successfully!')

    st.table(projects_data)

if __name__ == "__main__":
    main()

