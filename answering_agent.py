import pandas as pd
import numpy as np
from pydantic import BaseModel,Field,model_validator
from llm_config import llm
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


class CodeFormat(BaseModel):
  code_exp:str=Field(description="Single line explanation of what the code is doing")
  code:str=Field(description="Code only that is performing data analysis, in pure python")


def data_answerer(df,query):
  exec_env={"df":df,"pd":pd}
  data_preview=df.head(20).to_markdown(index=False)
  parser=PydanticOutputParser(pydantic_object=CodeFormat)
  instructions=PromptTemplate(
    template="""
    You are a Python data analyst. The user has provided a preview of a dataset to give context:

    {data_preview}

    The full dataset is assumed to be loaded into a Pandas DataFrame named `df`.

    Based on the user's question below, write Python code to perform the requested analysis using `df`. Do NOT hardcode any values from the preview.

    Assign the final result to a variable called `answer`. Do not print it.

    User question:
    {query}

    {format_instructions}
    """,input_variables=["query","data_preview"], partial_variables={"format_instructions": parser.get_format_instructions()})
  
  instructions_and_llm=instructions | llm

  output=instructions_and_llm.invoke({"data_preview":data_preview,"query":query})

  parsed_output=parser.invoke(output)

  final_code=parsed_output.code

  exec(final_code, exec_env)
  
  return exec_env.get("answer")
  