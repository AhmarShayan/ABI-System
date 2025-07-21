from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import re

def execute_query(db,multi_query_sql):
    raw_queries = re.split(r"--\s*Query\s*\d+:.*\n", multi_query_sql)
    queries=[q.strip() for q in raw_queries if q.strip()]

    tool=QuerySQLDataBaseTool(db=db)
    results=[]

    for i,query in enumerate(queries,start=1):
        print(f"Running the query {i}")

        try:
            result=tool.invoke(query)
            results.append({f"result {i}":result})
        except Exception as e:
            results.append({f"For result {i}":f"Got error {e}"})

    return results
