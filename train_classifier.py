import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Load data
data_dict = pickle.load(open('./data.pickle', 'rb'))

# Convert data and labels to numpy arrays
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Assume each sample corresponds to one hand, and we need to account for two hands
# If two hands are to be detected, we will modify this part in future steps

# Split the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Initialize the RandomForest model
model = RandomForestClassifier()

# Train the model with training data
model.fit(x_train, y_train)

# Predict labels on the test data
y_predict = model.predict(x_test)

# Calculate accuracy
score = accuracy_score(y_predict, y_test)

# Output accuracy score
print(f'{score * 100:.2f}% of samples were classified correctly!')

# Save the trained model using pickle
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)



