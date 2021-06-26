import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from keras.models import Sequential, save_model, load_model
from keras.layers.core import Dense
from sklearn.model_selection import train_test_split
from app.employee import Employee

# Load data
df = pd.read_csv('data/turnover.csv', encoding = "ISO-8859-1")
df = df[df.event == 1]
df.drop(columns=['event'], inplace=True)

enc, scaler, nn = None, None, None

try:
    # Load wwith pickle
    with open('data/preprocessing.pickle', 'rb') as f:
        enc, scaler = pickle.load(f)

    nn = load_model('data/models/saved_model', compile=True)
except:
    # Encode categorical columns
    enc = OneHotEncoder()
    enc.fit(df[['industry', 'profession', 'traffic', 'way']])
    df_enc = np.array(enc.transform(df[['industry', 'profession', 'traffic', 'way']]).toarray())
    df_enc = pd.DataFrame(df_enc, columns=np.concatenate(enc.categories_).ravel())

    # Scale numeric columns
    scaler = StandardScaler()
    scaler.fit(df[['age', 'extraversion', 'independ', 'selfcontrol', 'anxiety', 'novator']])
    df_sca = scaler.transform(df[['age', 'extraversion', 'independ', 'selfcontrol', 'anxiety', 'novator']])
    df_sca = pd.DataFrame(df_sca, columns=['age', 'extraversion', 'independ', 'selfcontrol', 'anxiety', 'novator'])

    # Binarize other columns
    df_gender = df['gender'].apply(lambda x: 1.0 if x=='m' else -1.0)
    df_coach = df['coach'].apply(lambda x: 1.0 if x=='yes' else (-1.0 if x=='no' else 0.0))
    df_head_gender = df['head_gender'].apply(lambda x: 1.0 if x=='m' else -1.0)
    df_greywage = df['greywage'].apply(lambda x: 1.0 if x=='white' else -1.0)
    df_gender = pd.DataFrame(df_gender, columns=['gender'])
    df_coach = pd.DataFrame(df_coach, columns=['coach'])
    df_head_gender = pd.DataFrame(df_head_gender, columns=['head_gender'])
    df_greywage = pd.DataFrame(df_greywage, columns=['greywage'])

    # Remove preprocessed columns
    df = df.drop(columns=['industry', 'profession', 'traffic', 'way', 'age', 'extraversion', 'independ', 'selfcontrol', 'anxiety', 'novator', 'gender', 'coach', 'head_gender', 'greywage'])
    
    # Concat columns
    df = pd.concat([df_gender.reset_index(drop=True), df_sca.reset_index(drop=True), df_coach.reset_index(drop=True), df_head_gender.reset_index(drop=True), df_greywage.reset_index(drop=True), df.reset_index(drop=True), df_enc.reset_index(drop=True)], axis=1)

    # Define x and y
    X = df.drop(columns=['stag'])
    y = df[['stag']]

    # Define training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # Create neural network
    # Layers:
    #     Input Layer: 52 nodes
    #     Hidden Layer: 5 nodes
    #     Hidden Layer: 4 nodes
    #     Output Layer: 1 node
    #     Activation: ReLU
    # Loss: Mean squared logarithmic error
    # Metrics: Mean squared logarithmic error
    nn = Sequential()
    nn.add(Dense(X_train.shape[1], activation='relu', input_shape=(X_train.shape[1],)))
    nn.add(Dense(5, activation='relu'))
    nn.add(Dense(5, activation='relu'))
    nn.add(Dense(1, activation='relu'))
    nn.compile(optimizer='adam', loss='mean_squared_logarithmic_error', metrics=['mean_squared_logarithmic_error'])

    # Train neural network
    nn.fit(X_train, y_train, epochs=100, validation_data=(X_test, y_test))

    # Save with pickle
    with open('data/preprocessing.pickle', 'wb') as f:
        pickle.dump([enc, scaler], f)

    save_model(nn, 'data/models/saved_model')


def predict_stag(employee: Employee):
    # Preprocess inputs
    enc_arr = np.array(enc.transform([[employee.industry, employee.profession, employee.traffic, employee.way]]).toarray())
    sca_arr = scaler.transform([[employee.age, employee.extraversion, employee.independ, employee.selfcontrol, employee.anxiety, employee.novator]])
    gender = 1.0 if employee.gender=='m' else -1.0
    coach = 1.0 if employee.coach=='yes' else (-1.0 if employee.coach=='no' else 0.0)
    head_gender = 1.0 if employee.head_gender=='m' else -1.0
    greywage = 1.0 if employee.greywage=='white' else -1.0

    # Restructure inputs
    inputs = [[gender], sca_arr.flatten(), [coach], [head_gender], [greywage], enc_arr.flatten()]
    inputs = np.array([item for sublist in inputs for item in sublist])
    inputs = np.reshape(inputs, (1, 52))

    # Predict stag
    predicted = nn.predict(inputs)
    return predicted[0][0].item()