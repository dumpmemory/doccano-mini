import streamlit as st
from langchain.chains import LLMChain

from doccano_mini.components import (
    display_download_button,
    display_usage,
    openai_model_form,
)
from doccano_mini.examples import make_task_free_example
from doccano_mini.prompts import make_task_free_prompt

st.title("Task Free")
st.header("Annotate your data")
num_cols = st.number_input("Set the number of columns", min_value=2, max_value=10)
columns = [st.text_input(f"Column {i}:", value=f"column {i}") for i in range(1, int(num_cols) + 1)]

df = make_task_free_example()
df = df.reindex(columns, axis="columns", fill_value="")
edited_df = st.experimental_data_editor(df, num_rows="dynamic", width=1000)
examples = edited_df.to_dict(orient="records")

prompt = make_task_free_prompt(examples)

prompt.prefix = st.text_area(
    label="Enter task instruction",
    placeholder=f"Predict {columns[-1]} based on {', '.join(columns[:-1])}.",
    height=200,
)

inputs = {column: st.text_input(f"Input for {column}:") for column in columns[:-1]}

st.markdown(f"Your prompt\n```\n{prompt.format(**inputs)}\n```")

llm = openai_model_form()
if st.button("Predict"):
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(**inputs)
    st.text(response)

    chain.save("config.yaml")
    display_download_button()
display_usage()
