"""Shubham Agawane - 2019"""
def lstm_prediction(se, stock_symbol):
	import pandas as pd
	import numpy as np

	def fetch_stock_data(se, stock_symbol):
		"""fetch stock data"""
		from pandas_datareader import data as pdr
		import yfinance as yf
		yf.pdr_override()
		if se == 'NSE': stock_symbol += ".NS" 
		return pdr.get_data_yahoo(stock_symbol, period="5y")


	"""LSTM model development"""
	from sklearn.preprocessing import MinMaxScaler
	from keras.models import Sequential
	from keras.layers import Dense, Dropout, LSTM

	og_df = fetch_stock_data(se, stock_symbol)
	todataframe = og_df.reset_index(inplace=False)

	#to print the info of the http://127.0.0.1:8000/OG dataset
	print("\n<----------------------Info of the OG dataset---------------------->")
	print(todataframe.info())
	print("<-------------------------------------------------------------------->\n")

	#dataframe creation
	seriesdata = todataframe.sort_index(ascending=True, axis=0)
	new_seriesdata = pd.DataFrame(index=range(0,len(todataframe)),columns=['Date','Close'])
	for i in range(0,len(seriesdata)):
	    new_seriesdata['Date'][i] = seriesdata['Date'][i]
	    new_seriesdata['Close'][i] = seriesdata['Close'][i]
	#setting the index again
	new_seriesdata.index = new_seriesdata.Date
	new_seriesdata.drop('Date', axis=1, inplace=True)
	#creating train and test sets this comprises the entire data’s present in the dataset
	myseriesdataset = new_seriesdata.values
	totrain = myseriesdataset
	#converting dataset into x_train and y_train
	scalerdata = MinMaxScaler(feature_range=(0, 1))
	scale_data = scalerdata.fit_transform(myseriesdataset)
	x_totrain, y_totrain = [], []
	length_of_totrain=len(totrain)
	for i in range(60,length_of_totrain):
	    x_totrain.append(scale_data[i-60:i,0])
	    y_totrain.append(scale_data[i,0])
	x_totrain, y_totrain = np.array(x_totrain), np.array(y_totrain)
	x_totrain = np.reshape(x_totrain, (x_totrain.shape[0],x_totrain.shape[1],1))
	#LSTM neural network
	lstm_model = Sequential()
	lstm_model.add(LSTM(units=50, return_sequences=True, input_shape=(x_totrain.shape[1],1)))
	lstm_model.add(LSTM(units=50))
	lstm_model.add(Dense(1))
	lstm_model.compile(loss='mean_squared_error', optimizer='adadelta')
	lstm_model.fit(x_totrain, y_totrain, epochs=3, batch_size=1, verbose=2)
	#predicting next data stock price
	myinputs = new_seriesdata[len(new_seriesdata) - (100) - 60:].values
	myinputs = myinputs.reshape(-1,1)
	myinputs  = scalerdata.transform(myinputs)
	tostore_test_result = []
	for i in range(60,myinputs.shape[0]):
	    tostore_test_result.append(myinputs[i-60:i,0])
	tostore_test_result = np.array(tostore_test_result)
	tostore_test_result = np.reshape(tostore_test_result,(tostore_test_result.shape[0],tostore_test_result.shape[1],1))
	myclosing_priceresult = lstm_model.predict(tostore_test_result)
	myclosing_priceresult = scalerdata.inverse_transform(myclosing_priceresult)


	#Combining og and predicted dataset for end result.
	datelist = pd.date_range(pd.datetime.now().date(), periods=101)[1:]
	predicted_df = pd.DataFrame(myclosing_priceresult, columns=['Close'], index=datelist)
	result_df = pd.concat([og_df, predicted_df])[['Close']]
	result_df = result_df.reset_index(inplace=False)
	result_df.columns = ['Date', 'Close']

	#to print the info of the END RESULT dataset
	print("\n<----------------------Info of the RESULT dataset---------------------->")
	print(result_df.info())
	print("<------------------------------------------------------------------------>\n")
	# import matplotlib.pyplot as plt

	# plt.plot(result_df['Close'])

	# plt.show()

	def get_json(df):
	    """ Small function to serialise DataFrame dates as 'YYYY-MM-DD' in JSON """
	    import json
	    import datetime
	    def convert_timestamp(item_date_object):
	        if isinstance(item_date_object, (datetime.date, datetime.datetime)):
	            return item_date_object.strftime("%Y-%m-%d")
	    
	    dict_ = df.to_dict(orient='records')

	    return json.dumps(dict_, default=convert_timestamp)

	return get_json(result_df)