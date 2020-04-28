import os
import sys
import pandas as pd
from functools import reduce
from typing import Union

def validator(file_path: str) -> Union[list, bool]:
  with open(file_path, 'r') as f:
    lines: list = f.readlines()
    # The file doesn't contain any information
    # and hence need not be processed
    if(len(lines) < 4):
      return False
    # The file may contain useful headline
    # but no elaborate description
    elif(len(lines) == 4):
      if(len(lines[0].strip('\n').strip()) > 2):
        return lines
      else:
        # If there is no headline in first line
        # there is no need to process it
        return False
    else:
      return lines if reduce(lambda  a, b: a + b, map(lambda x: 1 if x.startswith('--') else 0, lines[0:4])) == 4 and reduce(lambda a, b: a + b, map(lambda x: len(x.strip('\n').strip()), lines[4:7])) == 0 else False

def parserecord(data: list) -> list:
  result = []
  # Parsing the metadata
  # This constitutes the first 4 lines
  # -- Headline
  # -- Journalists
  # -- Data
  # -- Link
  for i, ele in enumerate(data[0:4]):
    clean_ele = ele.lstrip('- ').rstrip(' \n')
    if(i == 1):
      # Multiple journalists are mentioned in the form
      # -- By X, Y and Z
      authors = clean_ele.lstrip(' By').split('and')
      if(len(authors) > 1):
        authors.extend(authors[0].split(','))
        authors.pop(0)
      result.append([i.strip() for i in authors])
    else:
      result.append(clean_ele)

  # Parsing the article body
  content: str = ''
  if(len(data) > 4):
    for i in data[4:]:
      content += i.rstrip('\n').strip()
  result.append(content)

  return result

def constructdf(dataset_path) -> pd.DataFrame:
  files = os.listdir(dataset_path)
  cnt_empty = 0
  final_df = pd.DataFrame()

  for i in files:
    if(i.endswith('.DS_Store')):
      continue
    nested_files = os.listdir(dataset_path + '/' + i)
    for j in nested_files:
      if(j.endswith('.gz') or j.endswith('.DS') or j.endswith('.vscode')):
        continue

      return_code: Union[list, bool] = validator(dataset_path + '/' + i + '/' + j)
      if(return_code == False):
        continue
      else:
        parsedrecord = parserecord(return_code)
        final_df = pd.concat([final_df, pd.DataFrame([parsedrecord])], ignore_index = True)

  return final_df

# Debug
# Check if the validator works correctly by
# going through the entire dataset
if(__name__ == '__main__'):

  dataset_path: str = 'financial-news-dataset/ReutersNews106521'
  if(len(sys.argv) > 1):
    dataset_path = sys.argv[1];

  if(not os.path.exists(dataset_path)):
    if(os.path.exists('ReutersNews106521')):
      dataset_path = 'ReutersNews106521'
    else:
      raise Exception("Invalid dataset path!\nDataset Path: {}".format(dataset_path))

  files = os.listdir(dataset_path)
  cnt_empty = 0
  print('Validating unstructured data....')
  for i in files:
    if(i.endswith('.DS_Store')):
      continue
    nested_files = os.listdir(dataset_path + '/' + i)
    for j in nested_files:
      if(j.endswith('.gz') or j.endswith('.DS') or j.endswith('.vscode')):
        continue

      return_code: Union[list, bool] = validator(dataset_path + '/' + i + '/' + j)
      if(return_code == False):
        cnt_empty += 1
      else:
        parsedrecordlen = len(parserecord(return_code))
        # Each record should have 5 columns
        # No more, no less
        # Headline, authors, date, link, body
        if(parsedrecordlen != 5):
          raise Exception("ParserError\nRecord parsing expects list of length 5 but found {} at {}/{}/{}".format(parsedrecordlen, dataset_path, i, j))

  if(cnt_empty != 25):
    raise Exception("ValidatorError\nEmpty record count off. Expected 25 but found {}".format(cnt_empty))

  print('Constructing DataFrame for the financial data....')
  financialdf = constructdf(dataset_path)
  print('Finished constructing DataFrame of shape: ', financialdf.shape)

  print('Renaming columns....')
  financialdf.columns = ['Headline', 'Journalists', 'Date', 'Link', 'Article']
  print('Saving the DataFrame as a gzipped parquet....')
  financialdf.to_parquet('financial_data.parquet.gzip',compression='gzip')