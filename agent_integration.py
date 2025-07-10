import pandas as pd
from cleaning_agent import data_cleaner
from answering_agent import data_answerer


class Agents:
  def __init__(self,raw_data,query,answer="Hello"):
    self.raw_data=raw_data
    self.ready_data=None
    self.query=query
    self.answer=answer
    self.data_cleaned=False

  def clean_data(self):
    if not self.data_cleaned:
      self.ready_data=data_cleaner(self.raw_data)
      self.data_cleaned=True

  def get_cleaned_data(self):
    if not self.data_cleaned:
      self.clean_data()
    return self.ready_data


  def answer_query(self):
    if self.ready_data is None:
        self.clean_data()
    result = data_answerer(self.ready_data, self.query)
    self.answer = result
    return self.answer