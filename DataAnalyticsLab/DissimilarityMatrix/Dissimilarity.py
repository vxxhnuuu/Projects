import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import pairwise_distances

#Read the dataset
df = pd.read_csv('DataAnalyticsLab\DissimilarityMatrix\Dis.csv')

#Seperate nominal and numeric attributes
nominal_attributes = df.select_dtypes(include = ['object'])
numeric_attributes = df.select_dtypes(include = ['number'])

#Encode nominal attributes
encoder = OneHotEncoder()
nominal_data_encoder = encoder.fit_transform(nominal_attributes).toarray()

#Create Dissimilarity matrix
numeric_dissimilarity_matrix = pairwise_distances(numeric_attributes , metric = 'euclidean')
nominal_dissimilarity_matrix = pairwise_distances(nominal_data_encoder , metric = 'jaccard')

print("\nDissimilarity between numeric attributes")
print(pd.DataFrame(numeric_dissimilarity_matrix))
print("\nDissimilarity between nominal attributes")
print(pd.DataFrame(nominal_dissimilarity_matrix))