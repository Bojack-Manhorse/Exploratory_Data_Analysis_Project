# Exploratory Data Analysis - The Manufacturing Process

## Introduction

This is a project on performing Exploratory Data Analysis (EDA) on a dataset from a manufacturing process. We do the following:

- Extract data from an RDS database
- Convert some of the data into more useful types
- Perform null value imputation
- Transform Skewed data
- Remove outliers within the data
- Examine correlations between columns
- Visulation the failure rates and give suggestion on how to avoid them

## Installation

First ensure that python and pip is installed on your machine `https://www.python.org/downloads/`.

To clone the repository, open the terminal in the location you wish to install, and run the following:

```git clone Bojack-Manhorse/Exploratory_Data_Analysis_Project ```

Then navigate into the installed folder:

```cd Exploratory_Data_Analysis_Project ```

Finally install the reuqired python modules:

```pip install -r requirements.txt```

## Setup

Fill out the file `credentials_template.yaml` with the RDS database credentials you wish to extract data from, and rename it `db_creds.yaml`. Then open the file `Project.ipynb` in any program that displays python notebooks (e.g. VSCode). The data analysis is found within the notebook.

## File structure

The file `db_utils.py` contains various classes to performing data extraction and data visualisation. The classes are then imported in `Projects,py`.

## Packages used:

- pandas
- PyYAML
- PyYAML
- scipy
- seaborn
- SQLAlchemy