import sys
import csv
import numpy as np
import math

FUNCTIONS = ['linear', 'exp', 'log', 'loglog']

def fit_function(fun, xs, ys):
  lin_xs = [x for x in xs]
  lin_ys = [y for y in ys]

  #turn it into a linear function to fit
  if fun == 'exp':
    lin_ys = [math.log(y) for y in ys]
  elif fun == 'log':
    lin_xs = [math.log(x) for x in xs]
  elif fun == 'loglog':
    lin_xs = [math.log(-1*math.log(x)) for x in xs]

  np_xs = np.array(lin_xs)
  np_ys = np.array(lin_ys)

  # calculate the regression
  coeffs = np.polyfit(np_xs, np_ys, 1)
  line = np.poly1d(coeffs)

  # calculate mean squared error
  pred = [line(x) for x in lin_xs]
  sq_error = [(pred[i] - lin_ys[i])**2 for i in range(0, len(lin_ys))]
  mean_sq_error = sum(sq_error) / len(sq_error)

  return {'coeffs': coeffs, 'err': mean_sq_error}


if __name__ == '__main__':

  trend_file_name = sys.argv[1]
  print trend_file_name
  trend_file = csv.reader(open(trend_file_name, 'r'));

  xs = []
  ys = []
  data_set = "unknown"

  for row in trend_file:
    if len(row) == 1:
      data_set = row[0]
      continue

    xs.append(float(row[0]))
    ys.append(float(row[1]))

  regression_dict = {}

  best_fun = None
  least_err = 0
  for fun in FUNCTIONS:
    regression_dict[fun] = fit_function(fun, xs, ys)
    err = regression_dict[fun]['err']
    if best_fun == None or err < least_err:
      best_fun = fun
      least_err = err

  print best_fun, regression_dict[best_fun]


