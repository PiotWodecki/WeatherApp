from collections import namedtuple
import time
import geocoder
from os import startfile
from sklearn.metrics import explained_variance_score, \
    mean_absolute_error, \
    median_absolute_error
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

import os
# import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
#this unused libraries are neccessary to use statsmodel.api :(
import numpy as np
import scipy as sci
import patsy as pt
import statsmodels.api as sm
# import statsmodels.tools.tools.add_constant as
#from statsmodels.api import add_constant
#from statsmodel import sm


def create_df_from_json(json):
    dates = []
    dates2 = []
    temps = []
    for x in json['daily']:
        dates.append(datetime.utcfromtimestamp(int(x['dt'])).strftime('%d/%m/%Y'))
    for x in dates:
        for y in range(4):
            dates2.append((datetime.strptime(x, '%d/%m/%Y') + timedelta(hours=y*6)))

    for index, date in enumerate(dates2):
        dates2[index] =datetime.strftime(date, '%d/%m/%Y %H:%M')

    for index, day in enumerate(json['daily']):
        temps.append(day['temp']['night'] - 273.15)
        temps.append(day['temp']['morn'] - 273.15)
        temps.append(day['temp']['day'] - 273.15)
        temps.append(day['temp']['eve'] - 273.15)

    df = pd.DataFrame(
        {'Dates': dates2,
        'Temperatures': temps})
    df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y %H:%M')

    return df


def create_df_to_ml_from_json(json):
    pass


def create_df_from_statistical_data(all_days_data):
    print(all_days_data)
    records = []
    features = ["date", "meantemp", "meanpressure", "meanhumidity", "meanprecipitation", "meanclouds",
                "maxtemp", "mintemp", "maxpressure", "minpressure", "maxhumidity", "minhumidity",
                "maxprecipitation", "minprecipitation", "maxclouds", "minclouds"]
    DailySummary = namedtuple("DailySummary", features)

    for index, elem in enumerate(all_days_data):
        records.append(DailySummary(
            date=datetime(datetime.today().year - 1, elem['month'], elem['day']),
            meantemp=elem['temp']['mean'],
            mintemp=elem['temp']['average_min'],
            maxtemp=elem['temp']['average_max'],
            meanpressure=elem['pressure']['mean'],
            minpressure=elem['pressure']['min'],
            maxpressure=elem['pressure']['max'],
            meanhumidity=elem['humidity']['mean'],
            minhumidity=elem['humidity']['min'],
            maxhumidity=elem['humidity']['max'],
            meanprecipitation=elem['precipitation']['mean'],
            minprecipitation=elem['precipitation']['min'],
            maxprecipitation=elem['precipitation']['max'],
            meanclouds=elem['clouds']['mean'],
            minclouds=elem['clouds']['min'],
            maxclouds=elem['clouds']['max']
        ))

    df = pd.DataFrame(records, columns=features).set_index('date')
    df = df.drop(['minclouds', 'minprecipitation'], axis=1)
    # cleaning dataset
    df = df.dropna()

    return df


def show_correlations(df, col='meantemp'):
    #correlations
    return df.corr()[[col]].sort_values(col)


def create_backward_elimination(df, dependent_variable='meantemp'):
    y = df[dependent_variable]
    X = df.loc[:, df.columns != dependent_variable]
    X = sm.add_constant(X, has_constant='add')
    alpha = 0.05 # p value
    model = sm.OLS(y, X).fit() #o rdinary least square model

    # backward elimination for Warszawa city - did not find
    # automate process and did not have time to make it singlehanded
    X = X.drop(['maxtemp', 'mintemp'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxhumidity_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxtemp_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['mintemp_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxprecipitation_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['mintemp_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanprecipitation_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanpressure_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanhumidity_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['minpressure_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxprecipitation_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxprecipitation_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['minpressure_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanprecipitation_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanclouds_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanpressure_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['mintemp_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['minhumidity_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanclouds_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxclouds_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxclouds_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxclouds_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['minhumidity_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanprecipitation_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxhumidity_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['minpressure_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxtemp_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['minhumidity_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanhumidity_1'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxpressure_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxpressure_2'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxhumidity_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['maxtemp_3'], axis=1)
    model = sm.OLS(y, X).fit()
    X = X.drop(['meanhumidity_3'], axis=1)
    model = sm.OLS(y, X).fit()

    model_summary = model.summary()

    #const variable was only temporary
    X = X.drop('const', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

    regressor = LinearRegression()

    # fit the build the model by fitting the regressor to the training data
    regressor.fit(X_train, y_train)

    # make a prediction set using the test set
    prediction = regressor.predict(X_test)

    # Evaluate the prediction accuracy of the model
    from sklearn.metrics import mean_absolute_error, median_absolute_error
    score = "The Explained Variance: %.2f" % regressor.score(X_test, y_test)
    mean_abs_error = "The Mean Absolute Error: %.2f degrees celsius" % mean_absolute_error(y_test, prediction)
    median_abs_error = "The Median Absolute Error: %.2f degrees celsius" % median_absolute_error(y_test, prediction)
    params = str(model.params)

    return model_summary, score, mean_abs_error, median_abs_error, params


# method to create columns for n days back
def derive_nth_day_feature(df, features, n):
    rows = df.shape[0]
    for feature in features:
        if feature != 'date':
            for N in range(1, n+1):
                nth_prior_measurements = [None]*N + [df[feature][i-N] for i in range(N, rows)]
                col_name = "{}_{}".format(feature, N)
                df[col_name] = nth_prior_measurements

    return df


def cast_df_to_numeric(df):
    df = df.apply(pd.to_numeric, errors='coerce')
    return df


def handle_df_for_dnn_regressor(df):
    # it is not done - my data is too small for training neural network
    # in my computer it is endlessly
    df = df.drop(['mintemp', 'maxtemp'], axis=1)
    X = df[[col for col in df.columns if col != 'meantemp']]
    y = df['meantemp']

    X_train, X_tmp, y_train, y_tmp = train_test_split(X, y, test_size=0.2, random_state=23)
    # take the remaining 20% of data in X_tmp, y_tmp and split them evenly
    X_test, X_val, y_test, y_val = train_test_split(X_tmp, y_tmp, test_size=0.5, random_state=23)

    X_train.shape, X_test.shape, X_val.shape
    print("Training instances   {}, Training features   {}".format(X_train.shape[0], X_train.shape[1]))
    print("Validation instances {}, Validation features {}".format(X_val.shape[0], X_val.shape[1]))
    print("Testing instances    {}, Testing features    {}".format(X_test.shape[0], X_test.shape[1]))

    feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]

    regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                          hidden_units=[50, 50],
                                          model_dir='tf_wx_model')

    evaluations = []
    STEPS = 200

    for i in range(100):
        regressor.train(input_fn=wx_input_fn(X_train, y=y_train), steps=STEPS)
        evaluations.append(regressor.evaluate(input_fn=wx_input_fn(X_val,
                                                                   y_val,
                                                                   num_epochs=1,
                                                                   shuffle=False)))


    # manually set the parameters of the figure to and appropriate size
    plt.rcParams['figure.figsize'] = [14, 10]

    loss_values = [ev['loss'] for ev in evaluations]
    training_steps = [ev['global_step'] for ev in evaluations]

    # plot of loosing over time
    plt.scatter(x=training_steps, y=loss_values)
    plt.xlabel('Training steps (Epochs = steps / 2)')
    plt.ylabel('Loss (SSE)')
    plt.show()
    plt.savefig('ml_training.png')

    pred = regressor.predict(input_fn=wx_input_fn(X_test,
                                                  num_epochs=1,
                                                  shuffle=False))
    predictions = np.array([p['predictions'][0] for p in pred])

    print("The Explained Variance: %.2f" % explained_variance_score(
        y_test, predictions))
    print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(
        y_test, predictions))
    print("The Median Absolute Error: %.2f degrees Celcius" % median_absolute_error(
        y_test, predictions))


def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=150):
    X = X.reset_index(drop=True)
    y = y.reset_index(drop=True)
    return tf.compat.v1.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)


def handle_col_to_remove(df):
    # removing actual data as it was split on columns for example meanpressure_1, meanpressure_2, meanpressure_3
    # digit represent amount of days in past
    to_remove = ['meanpressure', 'meanhumidity', 'meanprecipitation',
                 'meanclouds', 'maxpressure', 'minpressure',
                 'maxhumidity', 'minhumidity', 'maxprecipitation', 'maxclouds']

    # make a list of columns to keep
    to_keep = [col for col in df.columns if col not in to_remove]

    # select only the columns in to_keep and assign to df
    df = df[to_keep]
    cast_df_to_numeric(df)
    df = df.dropna()
    cast_df_to_numeric(df)

    return df


def create_file_with_ols(city, corrs, data):
    base_filename = 'OLS.txt'
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, base_filename), 'w') as infile:
        infile.write("Ordinary least square model for {}\n\n".format(city))
        infile.write("Correlations: \n")
        corrs.to_csv(infile, header=True, index=True, sep=' ', mode='w')
        infile.write("\nModel summary\n\n")
        infile.write(str(data[0]))
        infile.write("\n")
        infile.write(str(data[1]))
        infile.write("\n")
        infile.write(str(data[2]))
        infile.write("\n")
        infile.write(str(data[3]))
        infile.write("\nParams\n")
        infile.write(str(data[4]))


def open_notepad():
    base_filename = 'OLS.txt'
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    startfile(os.path.join(cur_dir, base_filename))


def calculate_date_to_unix(days_to_substract):
    start_date = datetime.today().replace(microsecond=0, second=0, minute=0) - timedelta(days=days_to_substract)
    start_date_unix = int(float(str(time.mktime(start_date.timetuple()))))
    return start_date_unix


def get_location():
    g = geocoder.ip('me')
    city = g.geojson['features'][0]['properties']['city']
    if city:
        return city



