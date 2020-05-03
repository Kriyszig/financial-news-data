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

If you have cloned the dataset at a particular `<path_to_dataset>`, you can run the program as follows pointing to the location of the dataset

```bash
python3 main.py <path_to_dataset> # Replace <path_to_dataset> with the absolute path to the ReutersNews106521 folder
# For example
python3 main.py /home/user/financial-news-dataset/ReutersNews106521
```

Please note, the file generation may take ~~upto 20 minutes~~. DataFrame generation now takes less than 10 seconds.
Saving the DataFrame to gzipped parquet file takes less than a minute after optimizing memory allocation.

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

### Copyright

IT has come to my notice that due to the Copyright issue with the news article, the [original repository](https://github.com/philipperemy/financial-news-dataset) by [Philippe Rémy](https://github.com/philipperemy) has taken down the dataset. That being said, the repository was forked 46 times and some of these forks still contain the Reuters dataset. To avoid copyright infringement, the `parquet` branch containing the Dataset as a gzip parquet file has been removed. Due to the massive improvement in the build time, it is feasible for anyone to generate the dataset themselves even with a less powerful machine.
