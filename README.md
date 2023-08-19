# **Analysis of the market value of footballers from the top 6 European leagues.**

The purpose of the study is to collect data using the web scraping technique, combine several data sets into one, analyse the data and then attempt to build a model to predict the market value of players from the transfermarkt portal based on statistics proposed by the developers of the FIFA game and match statistics from the who_scored.


The project was made using **Python**. 
The **pandas** library was used for most of the tasks, also **numpy** was often involved.
Web scraping was done using the **selenium** library. 
For graphing, the **matplotlib** and **seaborn** libraries were used.
For modelling, **statsmodels** and **scikit-learn** were used.




## Web scraping and merging data sets

[**Link to the code**](https://github.com/AdamZ0112358/values-fifa/blob/main/webscrapping/webscrapping7.py)

The first objective was to collect information on football players from the top 6 European leagues:
- Premier league - English league
- La liga - Spanish league
- Serie A - Italian league
- Bundesliga - German league
- League 1 - French league
- Liga NOS - Portuguese league


The webscrapping folder contains code that was used to retrieve data from 3 websites:
- https://www.transfermarkt.pl/
- https://sofifa.com/
- https://www.whoscored.com/

The data in the webscrapping file was also pre-cleaned and processed. The biggest challenge proved to be merging the three data sets. In each set, the players and teams have slightly different names, which caused a lot of work. Various keys were tested with varying results, but it was eventually possible to prepare a data set for analysis.

The folder also contains the data files that were created during the process.

## Explanatory Data Analysis

[**Link to the code**](https://colab.research.google.com/drive/1dDi4OKwWJC1_9fBX0YBACgTDA-9Wxx_J?usp=sharing)

During EDA, the dataset was carefully analysed. The value of the footballers was changed to a logarithmic value due to the distribution of the data and outliers.

In this step, the usefulness of some variables could be observed, some variables were immediately discarded. For other variables, data completion was carried out.

The variables were shown in graphs. It was checked how strongly they were related to the value of the footballers using Pearson's correlation coefficient. In this step, new variables were also created based on existing variables.

## Predictive models

[**Link to the code**](https://colab.research.google.com/drive/1CNSFzgcQUZ_RpNqBXxnPQ6U4_Bf5L4K_?usp=sharing)

Four models were used for prediction. In each model, feature selection was carried out. The predictive value of the models is compared in the table below.

| model	 | adj_r2_train	 |  rmse_train	 | adj_r2_test	 | rmse_test	 |
| --- | --- | --- | --- | --- |
|	Linear Regression |	0.6040 |	1.0041 |	0.5544 |	1.0362 |
|	Multiple Linear Regression |	0.8068 |	0.6999 |	0.7346 |	0.8091 |
|	Decision Tree |	0.8493 |	0.6189 |	0.7914 |	0.7395 |
|	Random Forest |	0.8998 |	0.5046 |	0.8368 |	0.6537 |

As you can see, the random forest has the best results with Adjusted R-squared on the training data of 0.8998 and on the test data 0.8368 suggests a strong ability to explain the variance in the training and test data. 
Root Mean Squared Error is the lowest in Random Forest model. This indicates that it has the smallest average difference between predicted values and actual values on the training and test dataset compared to other models.

