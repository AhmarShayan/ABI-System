import pandas as pd
import numpy as np
from pydantic import BaseModel,Field,model_validator
from core.llm_config import llm
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate



class CleaningFormat(BaseModel):                                                
  clean_exp:str=Field(description="Single line explanation of the process")     
  clean_code:str=Field(description="Code that is performing the process")  




def data_cleaner(df):
  data_preview=df.head(20).to_markdown(index=False)
  parser2=PydanticOutputParser(pydantic_object=CleaningFormat)
  instructions2=PromptTemplate(
    template="""
    You are a data cleaning expert. Based on the dataset preview below, write Python code that performs the following:

    - Fills missing values (numerical and categorical)
    - Drops duplicates
    - Fixes inconsistent data types if needed

    Very Important:
    - Do not use `inplace=True`
    - Do not use chained assignments like `df['col'].method(..., inplace=True)`
    - Use `.ffill()` or `.bfill()` instead of `.fillna(method='ffill')`
    - Use assignment like `df['col'] = df['col'].ffill()` or `df['col'] = df['col'].fillna(value)`

    Only return the cleaning code that uses the dataframe `df` and no explanations. Also return a short explanation separately.

    {format_instructions}

    Dataset preview:
    {data_preview}
    """
    ,input_variables=["data_preview"], partial_variables={"format_instructions": parser2.get_format_instructions()})
  
  instructions_and_llm_2=instructions2 | llm

  output_2=instructions_and_llm_2.invoke({"data_preview":data_preview})
  
  parsed_output_2=parser2.invoke(output_2)
    
  main_code=parsed_output_2.clean_code
 
  exec_env_2={"df":df,"pd":pd}

  exec(main_code,exec_env_2)

  updated_df=exec_env_2["df"]

  if "clean_dataframe" in exec_env_2:
    updated_df = exec_env_2["clean_dataframe"](exec_env_2["df"])
  else:
    updated_df = exec_env_2["df"]

  return updated_df