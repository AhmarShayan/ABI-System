import pandas as pd
import numpy as np
from core.llm_config import llm
from pydantic import BaseModel,Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

class CodeFormat(BaseModel):
    code_exp:str=Field(description="High level explanation of what insights the queries aim to provide")
    code:str=Field(description="Multiple SQL queries thatv extract valuable insights from the data")

def generate_sql(db_table,engine):
    query = f"SELECT TOP 20 * FROM {db_table}"
    db_table_frame = pd.read_sql(query, engine)

    data_preview = db_table_frame.to_markdown(index=False)

    parser=PydanticOutputParser(pydantic_object=CodeFormat)
    instructions=PromptTemplate(
        template="""
    You are a highly skilled SQL data analyst.

    The user has provided a preview of a dataframe to give context:

    {data_preview}

    The full SQL table has been loaded into a dataframe with the help of pandas.
    Assume the dataframe is named `df`.

    This dataframe has been converted into a Microsoft SQL Server table named {db_table}.

    You must now write **at least 5 different SQL queries** that generate valuable insights from the data.

    - Use **Microsoft SQL Server (T-SQL)** syntax only.
    - Do **NOT** use backticks (\\`) — use **square brackets** [ ] for identifiers if needed.
    - Do **NOT** use `LIMIT` — use `TOP N` and `FETCH NEXT` if needed.
    - Use `ORDER BY`, `GROUP BY`, `JOIN`, `WHERE`, and other SQL Server-compliant clauses appropriately.
    - Focus on deriving business or operational insights from the data, such as:
        - Best performing categories or groups
        - Trends over time (if date fields exist)
        - Outliers or anomalies
        - Summary statistics

    {format_instructions}
""",input_variables=["data_preview","db_table"],partial_variables={"format_instructions":parser.get_format_instructions()})
    
    instructions_and_llm=instructions | llm

    print("Invoking LLM")

    output=instructions_and_llm.invoke({"data_preview":data_preview,"db_table":db_table})

    print("LLM invoked")

    parsed_output=parser.invoke(output)

    print("Ouput Generated")

    final_code=parsed_output.code

    

    return final_code