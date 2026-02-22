from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint
import streamlit as st


def build_chain(vector_store):

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    prompt = PromptTemplate(
        template="""
You are a helpful AI assistant.
Answer only from the provided transcript context.
If the context is not sufficient, just say you don't know.

{context}
Question: {question}
""",
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    hf_token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        huggingfacehub_api_token=hf_token,
        task="text-generation",
        temperature=0.2,
        max_new_tokens=512,
    )

    parser = StrOutputParser()

    main_chain = parallel_chain | prompt | llm | parser

    return main_chain


