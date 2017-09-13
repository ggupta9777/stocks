import numpy as np
import csv
import pandas
import matplotlib.pyplot as plt
class MF: 

	def __init__ (self, excel_name):
		self.xls = pandas.ExcelFile(excel_name)


	def initialize (self):
		fund_types = self.xls.sheet_names
		i = 0
		big_data = []
		for fund_type in fund_types:
			sheet = self.xls.parse(i)
			sheet = sheet.convert_objects(convert_numeric=True)
			cols = sheet.columns
			A = []
			for col in cols:
        			b = []
				b.append(col)
				b.append(sheet[col].values)
				A.append(b)
			big_data.append(A)
			i = i + 1
		self.fund_types = [element.encode("ASCII") for element in fund_types]
		self.big_data = big_data


	def dataByType(self, fund_type):
		i = self.fund_types.index(fund_type)
		data = self.big_data[i]
                data = np.array(data)
		return data[1:, 1:]

	def NAVByType(self, fund_type):
                data = self.dataByType(fund_type)
                return data[0, :]

	def assetsByType(self, fund_type):
                data = self.dataByType(fund_type)
                return data[1, :]

	def returnsByType(self, fund_type):
                data = self.dataByType(fund_type)
		data = data[2:, :]
		A = np.array(data[0, 0])
		for i in range (1, len(data)):
			a = np.array(data[i, 0], dtype=float)
			A = np.vstack([A, a.T])
                return A.T

	def fundsByType(self, fund_type):
		i = self.fund_types.index(fund_type)
		data = self.big_data[i]
		data = data[0][1:]
		return data


if __name__ == "__main__":
	
	mutual_funds = MF ("moneycontrol.xlsx")
	mutual_funds.initialize()
	A = mutual_funds.returnsByType('diverse_equity')
	avg = np.nanmean(A, axis=1)
	std = np.nanstd(A, axis=1)
	print avg
	# plt.plot(np.arange(0, len(A[:, 0])), np.array(avg[2]))
	# plt.show()
