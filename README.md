# Reuters Financial Dataset as a structured DataFrame

[Reuters Financial Dataset](https://github.com/Danbo3004/financial-news-dataset) is a large collection of Financial News Article scraped from Reuters website.
Originally used for the paper [Using Structured Events to Predict Stock Price Movement:An Empirical Investigation - Ding et al.(2014)](http://emnlp2014.org/papers/pdf/EMNLP2014148.pdf)
this set of unstructured data is a powerful warehouse of historic Financial Data. This script provides a way of arranging the huge corpus of information into
a [Pandas'](https://pandas.pydata.org/) efficient data structure [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)  

Originally, this repository consisted of badly written Python script which was monolitic and cryptic. This refactor breaks the code down into smaller functions and
comes equipped with a function to create the DataFrame.

### Usage

The build depends on the following libraries:
* pandas
* pyarrow or fastparquet - Pandas optional dependency to read and write DataFrame to parquet format

To generate the parquet file yourself, please run the following commands:

```bash
git clone https://github.com/Kriyszig/financial-news-data.git
cd financial-news-data
git clone https://github.com/duynht/financial-news-dataset.git
python3 main.py
```

Please note, the file generation may take upto 20 minutes.

If you are interested in the prebuilt dataset to save your time, please visit the [parquet branch](https://github.com/Kriyszig/financial-news-data/tree/parquet)  
To do it from command line, run

```bash
git clone --single-branch --branch parquet https://github.com/Kriyszig/financial-news-data.git
cd financial-news-data
```

The `financial-data.parquet.gzip` is the file that contains the dataset. To create a DataFrame out of this file, please use the code snippet below:

```python
import pandas as pd
df = pd.read_parquet('financial_data.parquet.gzip')
```
And you are all set to start manipulating df to suit your needs  

### Dataset

The Dataset has the following columns:

| Columns     | Type                               |
|-------------|------------------------------------|
| Headline    | string                             |
| Journalists | list\<string> (Can be empty)       |
| Date        | Unix Style Date                    |
| Link        | Original Reuters article link      |
| Article     | The complete report (Can be empty) |

**Note**: 
* Journalists can be an empty list if the original dataset had the field empty
* Article can be an empty string in case only the headline was reported in th original dataset

In case you run into any troubles, please feel free to open an issue and I'll look into it as soon as possible.
