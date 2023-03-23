#C. Data quality issues encountered and their handling:

Missing values: We encountered missing values in some columns of the dataset. We detected these missing values by using the dataframe.isnull().sum() function, which provided the count of missing values in each column. To handle the missing values, we used the mean of the respective columns to fill the gaps using dataframe.fillna(dataframe.mean(), inplace=True).

Noisy data: Our dataset contained noisy data, such as outliers, which can impact the accuracy of our analysis and predictions. We detected outliers using the IQR method, where we computed the interquartile range (IQR) for each numerical column and identified data points outside the range [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR] as outliers. To handle outliers, we opted to cap them at the lower and upper bounds of this range, ensuring that they don't distort our analysis while preserving the original data.

Duplicate data: We found duplicate rows in the dataset, which can lead to biased results in our analysis. We detected duplicate rows using the dataframe.duplicated().sum() function, which gave us the count of duplicate rows. To handle duplicate data, we removed the duplicate rows using dataframe.drop_duplicates(inplace=True).

Data integration: In this project, we've assumed that the data comes from a single source (CSV file). However, if we were to integrate data from different sources, we would use the pandas.merge() or pandas.concat() functions to combine the data based on common columns or indices. We would also ensure that the data is consistent across sources by checking for inconsistencies in column names, data types, and value ranges.

Data transformation: We noticed that some columns had varying scales, which could impact the performance of certain machine learning algorithms. To address this issue, we applied min-max scaling to the specified columns, ensuring that the data is on the same scale for analysis and modeling. We also created new features, such as 'price_range', which is the difference between the high and low prices. This new feature might provide more relevant information for our analysis.

By addressing these data quality issues, we improved the reliability and accuracy of our analysis of the dataset.
