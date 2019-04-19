# loss= sum(|y-yhat|)/n
# direction convergence
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

# --------Date pre-process-------------#
# content = pd.read_csv('E:/train.csv')
# content = content.dropna()
# age_with_fares = content[   (content['Age'] > 22) & (content['Fare'] < 400) & (content['Fare'] > 130)]
# sub_fare = age_with_fares['Fare']
# sub_age = age_with_fares['Age']
#---------------------------------------#

#-----------Regress Model---------------#
def func(age, k, b): return k * age + b

def loss(y, yhat):
    """
    :param y: the real fares
    :param yhat: the estimated fares
    :return: how good is the estimated fares
    """
    return np.mean(np.abs(y - yhat))
    # return np.mean(np.square(y - yhat))
    # return np.mean(np.sqrt(y - yhat))
#--------------------------------------#




losses = []

change_directions = [
    # (k, b)
    (+1, -1), # k increase, b decrease
    (+1, +1),
    (-1, +1),
    (-1, -1)  # k decrease, b decrease
]



best_direction = None


def step(): return random.random()*1


def derivate_k(y, yhat, x):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]

    return np.mean([a * -x_i for a, x_i in zip(abs_values, x)])


def derivate_b(y, yhat):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]
    return np.mean([a * -1 for a in abs_values])


learing_rate = 1e-1

#--------------random choice----------------#
def random_choice (sub_age,sub_fare):
    loop_times=10000
    min_error_rate = float('inf')
    while loop_times > 0:

        k_hat= random.random()*20-10
        b_hat =random.random()*20-10
        estimated_fares = func(sub_age, k_hat, b_hat)
        error_rate = loss(y=sub_fare, yhat=estimated_fares)

        if error_rate < min_error_rate:
            min_error_rate = error_rate
            best_k, best_b = k_hat, b_hat
         #   print('loop == {}'.format(loop_times))
         #   print('f(age) = {} * age + {}, with error rate: {}'.format(best_k, best_b, min_error_rate))
            losses.append(min_error_rate)
        loop_times -= 1

#    result(best_k,best_b)
    loss_show(losses)

    return best_k,best_b
#--------------supervised direction choice----------------#
def supervised_direct_choice(sub_age,sub_fare):
    loop_times = 10000
    direction = random.choice(change_directions)
    min_error_rate = float('inf')
    best_k = random.randint(-10, 10)
    best_b = random.randint(-10, 10)
    while loop_times > 0:
        k_delta_direction, b_delta_direction = direction
        k_delta = k_delta_direction * step()
        b_delta = b_delta_direction * step()

        new_k = best_k + k_delta
        new_b = best_b + b_delta

        estimated_fares = func(sub_age, new_k, new_b)
        error_rate = loss(y=sub_fare, yhat=estimated_fares)

        if error_rate < min_error_rate:
            min_error_rate = error_rate
            best_k, best_b = new_k, new_b
            #best_k, best_b = k_hat, b_hat
            direction = (k_delta_direction, b_delta_direction)
         #   print('loop == {}'.format(loop_times))
            losses.append(min_error_rate)
         #   print('f(age) = {} * age + {}, with error rate: {}'.format(best_k, best_b, min_error_rate))
        else:
            direction = random.choice(list(set(change_directions) - {(k_delta_direction, b_delta_direction)}))
            # print(min_error_rate)
        loop_times-=1
    loss_show(losses)
    return best_k,best_b
#--------------gradient descent----------------#
def gradient_descent_choice(sub_age,sub_fare):
    k_hat = random.random()*20-10
    b_hat = random.random()*20-10
    loop_times = 10000
    losses = []
    learning_rate = 1e-1
    while loop_times>0 :
        k_delta = -1 * learning_rate * derivate_k(sub_fare, func(sub_age, k_hat, b_hat), sub_age)
        b_delta = -1 * learning_rate * derivate_b(sub_fare, func(sub_age, k_hat, b_hat))

        k_hat += k_delta
        b_hat += b_delta
       # print('loop == {}'.format(loop_times))
        error_rate = loss(sub_fare, func(sub_age, k_hat, b_hat))
      #  print('f(age) = {} * age + {}, with error rate: {}'.format(k_hat, b_hat, error_rate))
        losses.append(error_rate)

        loop_times -= 1

    loss_show(losses)
    return k_hat,b_hat


def result(best_k,best_b):
    plt.scatter(sub_age, sub_fare)
    plt.plot(sub_age, func(sub_age, best_k, best_b), c='r')
    #plt.plot(sub_age, func(sub_age, k_hat, b_hat), c='r')
    plt.show()

def loss_show(losses):
    plt.plot(range(len(losses)), losses)
    plt.show()


#random_choice()
#supervised_direct_choice()
#gradient_descent_choice()
