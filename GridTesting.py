# MelbourneHousingPrediction
# Python v3.6 (not compatible with 2.7)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV
from datetime import datetime

if __name__ == '__main__':

    # Load up the data if needed: https://www.kaggle.com/anthonypino/melbourne-housing-market?
    # Set directory path to the location of this csv (local or ~/Downloads if you downloaded from kaggle)
    df = pd.read_csv('Melbourne_housing_FULL.csv')


    # Drop the statistically insignificant columns, columns whose data are better evaluated through other columns,
    # or columns with significant missing values
    del df['Address']
    del df['Method']
    del df['SellerG']
    del df['Date']
    del df['Postcode']
    del df['Lattitude']
    del df['Longtitude']
    del df['Regionname']
    del df['Propertycount']


    # If any row is missing any data, drop it
    # It is important that this is done after the previous step of removing insignificant columns
    # If converting to Python2: df.drop(labels=None, axis=0, index=None, columns=None, level=None, inplace=False, errors='ignore')
    df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)


    # Create features_df which will serve as our independent variables array
    # Evaluate the following columns as numerical data through one-hot encoding with Pandas
    features_df = pd.get_dummies(df, columns=['Suburb', 'CouncilArea', 'Type'])


    # We're deleting this column from features_df because it will serve as our dependent variable, y
    del features_df['Price']


    # Create a list of the columns for checking potential variables post one-hot, print if you need
    # cols = features_df.columns.tolist()
    # prop = 'property_to_value'
    # print("property_to_value = [")
    # for item in cols:
    #     print("\t0, " + "#" +item)
    # print("]")

    # Create X and y
    X = features_df.as_matrix()
    y = df['Price'].as_matrix()


    # Split the dataset (70/30)
    startTimeS = datetime.now()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state = 0)
    print ("\nSplit Time Taken:", datetime.now() - startTimeS)


    # Select algorithm (gradient boosting) and configure hyperparamaters
    startTime = datetime.now()
    model = ensemble.GradientBoostingRegressor()
    param_grid = {
        'n_estimators': [300, 600, 1000],
        'max_depth': [7, 9, 11],
        'min_samples_split': [3, 4, 5],
        'min_samples_leaf': [5, 6, 7],
        'learning_rate': [.01, .02, .6, .7],
        'max_features': [.8, .9],
        'loss': ['ls', 'lad', 'huber']
    }
    #Run with four CPUs in parallel
    gs_cv = GridSearchCV(model, param_grid, n_jobs=12)
    print ("Model Creation Time Taken:", datetime.now() - startTime)

    # Implement fit function on training data generated by train_test_split
    startTime1 = datetime.now()
    gs_cv.fit(X_train, y_train)
    print ("Model Fit Time Taken:", datetime.now() - startTime1)


    #Print optimal parameters chosen
    print("\n" + gs_cv.best_params_ + "\n")


    # Export training model as pickle file
    startTime2 = datetime.now()
    joblib.dump(model, 'house_trained_model_grid.pkl')
    print ("Export Time Taken:", datetime.now() - startTime2)
    print ("\n" + "-" * 50 + "\n")


    # Time to evaluate the results and see if our algorithm and hyperparamaters are sufficient
    startTime3 = datetime.now()
    mse = mean_absolute_error(y_train, gs_cv.predict(X_train))
    print ("Training - Mean Abs Error: %.2f" % mse)
    print ("Training Time taken:", datetime.now() - startTime3)

    startTime3 = datetime.now()
    mse1 = mean_absolute_error(y_test, gs_cv.predict(X_test))
    print ("\nTesting - Mean Abs Error: %.2f" % mse1)
    print ("Testing Time taken:", datetime.now() - startTime3)
    print ("\n")
