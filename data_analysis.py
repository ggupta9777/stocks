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

	def avgByType(self, fund_type):
		A = self.returnsByType(fund_type)
		avg = np.nanmean(A, axis=1)
		std = np.nanstd(A, axis=1)
		ind = np.where(np.isfinite(avg))
		avg = avg[ind]
		std = std[ind]
		funds = self.fundsByType(fund_type)[0][ind]
		ind_out = np.argsort(avg)
		avg = avg[ind_out]
		std = std[ind_out]
		funds = funds[ind_out]
		return avg, std, funds

	def stdByType(self, fund_type):
		# returns: std deviation, fund names, indices to sort by standard deviation
		A = self.returnsByType(fund_type)
		std = np.nanstd(A, axis=1)
                ind_out = np.argsort(std)
                ind = np.where(np.isfinite(std))
                std = std[ind]
                std = np.sort(std)
                l = len(std)
                ind_out = ind_out[:l]

		return std[ind], self.fundsByType(fund_type)[0][ind_out], ind_out



if __name__ == "__main__":
	
	mutual_funds = MF ("moneycontrol.xlsx")
	mutual_funds.initialize()
	fund_type = 'diverse_equity'
	A = mutual_funds.returnsByType(fund_type)
	avg, std, fund_avg = mutual_funds.avgByType(fund_type)
	# std, fund_std, ind_std = mutual_funds.stdByType(fund_type)
	n_best = min(20, min(len(avg), len(std)))
	
	x_avg = np.arange(n_best)
	plt.figure(1, facecolor='white')
	plt.xticks(x_avg, fund_avg[-n_best:], rotation=30)
	plt_avg, = plt.plot(x_avg, avg[-n_best:])
	plt_std, = plt.plot(x_avg, std[-n_best:])
	plt.scatter(x_avg, avg[-n_best:])
	plt.subplots_adjust(bottom=0.25)	
	plt.legend([plt_avg, plt_std], ['average return', 'std deviation'])
	plt.title('top performing ' + fund_type + ' funds (3-5 yrs)')
	plt.xlabel('fund type')
	plt.ylabel('% return')	

	# plt.figure(2)
	# x_std = np.arange(n_best)
        # plt.xticks(x_std, fund_std[:n_best], rotation=30)
        # plt.plot(x_std, std[:n_best])
        # plt.scatter(x_std, std[:n_best])
        # plt.subplots_adjust(bottom=0.20)
        # plt.title('std deviation')


# plt.plot(np.arange(0, len(A[:, 0])), np.array(avg[2]))
	plt.show()
