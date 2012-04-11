import sys
import csv
import numpy as np
import math
import matplotlib.pyplot as plt

IMG_DIR = 'images/'
FUNCTIONS = ['linear', 'exp', 'log', 'loglog']
#FUNCTIONS = ['log']
SHOW_ALL_GRAPHS = False

def fit_function(fun, data_set, xs, ys):
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
  lin_pred = [line(x) for x in lin_xs]
  if fun == "exp":
    pred = [math.exp(line(x)) for x in lin_xs]
  else:
    pred = lin_pred
  sq_error = [(pred[i] - lin_ys[i])**2 for i in range(0, len(lin_ys))]
  mean_sq_error = sum(sq_error) / len(sq_error)

  print "xs",xs
  print "ys",ys
  print "lin_xs", lin_xs
  print "lin_ys", lin_ys
  print "pred", pred

  if SHOW_ALL_GRAPHS:
    fig_num = FUNCTIONS.index(fun)
    fig_name = "{0}{1}-{2}.png".format(IMG_DIR, data_set, fun)
    plt.figure(fig_num)
    plt.plot(xs, ys, 'ro')
    plt.plot(xs, pred, 'bx')
    #plt.plot(lin_xs, lin_ys)
    #plt.plot(lin_xs, lin_pred, 'r')
    plt.savefig(fig_name)   
    plt.title("{0}: {1} fit".format(data_set, fun))
    plt.show()

  return {'coeffs': coeffs, 'err': mean_sq_error}


if __name__ == '__main__':

  for arg in sys.argv[1:]:
    if arg == '--graphall' or arg == '-G':
      SHOW_ALL_GRAPHS = True

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
    regression_dict[fun] = fit_function(fun, data_set, xs, ys)
    err = regression_dict[fun]['err']
    if best_fun == None or err < least_err:
      best_fun = fun
      least_err = err

  print best_fun, regression_dict[best_fun]
