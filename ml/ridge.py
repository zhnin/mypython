# @Time    : 2018/6/9 21:39
# @Author  : cap
# @FileName: ridge.py
# @Software: PyCharm Community Edition

import numpy as np
import sklearn.linear_model as sl
import sklearn.metrics as sm
import matplotlib.pyplot as mp
import matplotlib.patches as mc


def read_data(filename):
    x, y = [], []
    data = np.loadtxt(filename, delimiter=',')
    for i in data:
        x.append(i[0])
        y.append(i[1])
    return np.array(x), np.array(y)


def train_model(alpha, x, y):
    model = sl.Ridge(alpha, fit_intercept=True, max_iter=10000)
    model.fit(x, y)
    return model


def pred_model(model, x):
    return model.predict(x)


def eval_model(y, pred_y):
    mae = sm.mean_absolute_error(y, pred_y)
    mse = sm.mean_squared_error(y, pred_y)
    mde = sm.median_absolute_error(y, pred_y)
    evs = sm.explained_variance_score(y, pred_y)
    r2s = sm.r2_score(y, pred_y)
    print(mae, mse, mde, evs, r2s)


def init_chart():
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Ridge Regression', fontsize=20)
    mp.xlabel('x', fontsize=14)
    mp.ylabel('y', fontsize=14)
    mp.tick_params(which='both', top=True, right=True, labelright=True, labelsize=10)
    mp.grid(linestyle=':')


def draw_train(train_x, train_y, pred_train_y1, pred_train_y2):
    mp.plot(train_x, train_y, 's', c='green', label='Training')
    sorted_indices = train_x.T[0].argsort()
    mp.plot(train_x.T[0][sorted_indices], pred_train_y1[sorted_indices], '--',
            c='blue', label='Predicted Training(α= 0)')
    mp.plot(train_x.T[0][sorted_indices], pred_train_y2[sorted_indices], '--',
            c='lightskyblue', label='Predicted Training(α= 150)')
    mp.legend()


def draw_test(test_x, test_y, pred_test_y1, pred_test_y2):
    mp.plot(test_x, test_y, 's', c='orange', label='Testing')
    mp.plot(test_x, pred_test_y1, 'o', c='blue', label='Predicted Test(α=0)')
    for x, pred_y, y in zip(test_x, pred_test_y1, test_y):
        mp.gca().add_patch(mc.Arrow(x, pred_y, 0, y-pred_y, width=0.2, ec='none', fc='pink'))

    mp.plot(test_x, pred_test_y2, 'o', c='red', label='Predicted Test(α= 150)')
    for x, pred_y, y in zip(test_x, pred_test_y2, test_y):
        mp.gca().add_patch(mc.Arrow(x, pred_y, 0, y - pred_y, width=0.2, ec='none', fc='black'))
    mp.legend()


def show_chart():
    # dfd
    mp.show()


def main():
    x, y = read_data('./data/abnormal.txt')
    train_size = int(x.size * 0.8)
    train_x = x[:train_size].reshape(-1, 1)
    train_y = y[:train_size]
    model1 = train_model(0, train_x, train_y)
    model2 = train_model(150, train_x, train_y)
    pred_train_y1 = pred_model(model1, train_x)
    pred_train_y2 = pred_model(model2, train_x)

    test_x = x[train_size:].reshape(-1, 1)
    test_y = y[train_size:]
    pred_test_y1 = pred_model(model1, test_x)
    pred_test_y2 = pred_model(model2, test_x)

    print('α= 0')
    eval_model(test_y, pred_test_y1)
    print('α= 150')
    eval_model(test_y, pred_test_y2)

    init_chart()
    draw_train(train_x, train_y, pred_train_y1, pred_train_y2)
    draw_test(test_x, test_y, pred_test_y1, pred_test_y2)
    show_chart()


if __name__ == '__main__':
    main()
