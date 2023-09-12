# Trading Bot

The ML model was created using a Keras implementation of a LSTM, and is designed to predict tick-by-tick prices of the SPX index.

# ENVIRONMENT: 

Make sure to create a new virtual environment to install necessary packages. After activating your virtual environment, run the following to download all necessary packages:

`$ pip freeze > requirements.txt`

# ABOUT:

The process of creating the model can be found in data/model/train_model.ipynb. To alter the model's parameters and perform tests on the model, create a copy of this notebook and make your changes. Make sure to save the model that you train as an h5 file to ensure you don't lose any progress. 

Current models are stored in /model. v1_model.h5 predicts 12 timesteps, while v2_model.h5 predicts 900 timesteps.

To predict further, retrain the model with more timesteps, or use rolling forecasting - use the model's own predictions as input for subsequent predictions. 

The data used to train and test the model is not included in this repo, because it is far too large to add. The data used is tick data from SPX, all received within the last few months to a year (as of 9/8/23).The specific data I used was pulled from SierraChart, and v1 was trained on 22 million rows of this data.

The file data/get_IB_data.py is intended to pull data from the Interactive Brokers API, format and process 
that data to a form that our ML model can understand, and then have the model make predictions. Currently, this file
is not hooked up to live data, and is used to run tests on the model's performance.

Various data processing methods are stored in /misc.

# IMPORTANT:

In order to run the Interactive Brokers API, you must have IB Trader Workstation installed and running on your
local machine. Make sure the app is configured (in settings) to properly respond to API calls. 

The model and all related programs were created and run from a remote server - in order to connect your local TWS port to the remote server, create a ssh tunnel by doing the following:

Run the following command on a local terminal:

`$ ssh -R 7497:localhost:7497 relaymile@76.185.2.134 -q -C -N`

Where 
- 7497 is the Trader Workstation API's port (configured in settings)
- relaymile is your username on the remote server
- 76.185.2.134 is the IP of your remote server

Once you run this command, you will be prompted to enter the password for your user. Once you correctly enter your password, the terminal will hang. Leave it running while you work with the Trader Workstation. Now, your remote server should be able to communicate with your locally hosted IB Trader Workstation. 
