import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from pandas import DataFrame


def probability_P0(N, n, lambda_, mu_):
    ro = []
    ro.append(1)
    for k in range(1, N + 1):
        if k == 1:
            ro.append((N * lambda_) / mu_)
        elif k <= n and k != 1:
            ro.append(((N - k) * lambda_ * ro[k - 1]) / (k * mu_))
        else:
            ro.append(((N - k) * lambda_ * ro[k - 1]) / (n * mu_))

    P_0 = 1 / sum(ro)

    probability_list_final = []
    # probability_list_final.append(P_0)
    probability_list_final += list(map(lambda x: x * P_0, ro))
    return P_0, probability_list_final, ro


def probability_PQ(N, n, lambda_, mu_, P0):
    _, PQ, ro = probability_P0(N, n, lambda_, mu_)
    probability_list_final = []
    for i in range(0, len(P0)):
        probability_list_final.append(abs(1 - P0[i] * sum(ro)))
    return probability_list_final


def EM(N, n, lambda_, mu_):
    pr_list = probability_P0(N, n, lambda_, mu_)[1]
    sum_ = 0
    for x in range(N + 1):
        sum_ += (N - x) * pr_list[x]
    return N - sum_


def EN(N, n, lambda_, mu_):
    pr_list = probability_P0(N, n, lambda_, mu_)[1]
    print(pr_list)
    sum_ = 0
    for x in range(1, N):
        if x <= n:
            sum_ += x * pr_list[x]
        else:
            sum_ += n * pr_list[x]
    return sum_


def EQ(N, n, lambda_, mu_, pr_list):
    pr_list = probability_P0(N, n, lambda_, mu_)[1]
    sum_ = 0
    count = 1
    if n > N:
       n = N
    for i in range(n, N):
        sum_ += count * pr_list[i]
        count += 1
    return sum_


def load(EN, n):
    if n == 0:
        return EN[n]
    else:
        return EN[n] / (n + 1)


if __name__ == '__main__':
    N = int(input('Введите кол-во станков: '))
    Tc = int(input('Введите среднее время между наладками: '))
    Ts = int(input('Введите среднее время наладок: '))
    n = int(input('Введите кол-во наладчиков: '))
    print(f'Кол-во станков - {N}, среднее время между наладками - {Tc}, среднее время наладок - {Ts}')

    lambda_ = 1 / Tc
    mu_ = 1 / Ts
    print(f'Лямбда - {lambda_}, мю - {mu_}')

    probobilities_list_P0 = [probability_P0(N, x, lambda_, mu_)[0] for x in range(1, N + 1)]
    print(f'P0: {probobilities_list_P0}')
    probobilities_list_PQ = probability_PQ(N, n, lambda_, mu_, probobilities_list_P0)
    print(f'PQ: {probobilities_list_PQ}')
    EM_list = [EM(N, x, lambda_, mu_) for x in range(1, N + 1)]
    print(f'EM: {EM_list}')
    EN_list = [EN(N, x, lambda_, mu_) for x in range(1, N + 1)]
    print(f'EN: {EN_list}')
    EQ_list = [EQ(N, x, lambda_, mu_, probobilities_list_PQ) for x in range(1, N + 1)]
    print(f'EQ: {EQ_list}')
    load_list = [load(EN_list, x) for x in range(0, N)]
    print(f'Load: {load_list}')

    fig, axs = plt.subplots(3, 2, figsize=(12, 8), sharex=True)
    fig.suptitle('Домашняя работа №1 (Задание 2)', fontsize=16)

    axs[0, 0].plot([x for x in range(0, n)], probobilities_list_PQ[:n], '-', label='P ожидания обслуживания')
    axs[0, 0].set_xlabel('наладчики', fontsize=10, labelpad=-3)
    axs[0, 0].set_title('P ожидания обслуживания', fontsize=10, color='red', pad=17)
    axs[0, 0].grid(True)

    axs[0, 1].plot([x for x in range(1, n + 1)], EM_list[:n], '--', label='M простаивающих станков')
    axs[0, 1].set_xlabel('наладчики', fontsize=10, labelpad=-3)
    axs[0, 1].set_title('Мm простаивающих станков', fontsize=10, color='red', pad=17)
    axs[0, 1].grid(True)

    axs[1, 0].plot([x for x in range(1, n + 1)], EN_list[:n], '*', label='М занятых наладчиков')
    axs[1, 0].set_xlabel('наладчики', fontsize=10, labelpad=-3)
    axs[1, 0].set_title('Мn занятых наладчиков', fontsize=10, color='red')
    axs[1, 0].grid(True)

    axs[1, 1].plot([x for x in range(1, n + 1)], EQ_list[:n], '^', label='M ожидающих обслуживания')
    axs[1, 1].set_xlabel('наладчики', fontsize=10, labelpad=-3)
    axs[1, 1].set_title('Mq ожидающих обслуживания', fontsize=10, color='red')
    axs[1, 1].grid(True)

    axs[2, 0].plot([x for x in range(1, n + 1)], load_list[:n], '-', label='Коэффициент загрузки')
    axs[2, 0].set_xlabel('наладчики', fontsize=10, labelpad=-3)
    axs[2, 0].set_title('Коэффициент загрузки', fontsize=10, color='red')
    axs[2, 0].grid(True)

    axs[2, 1].plot([x for x in range(1, n + 1)], probobilities_list_P0[:n], '-', label='P ожидания обслуживания')
    axs[2, 1].set_xlabel('наладчики', fontsize=10, labelpad=-3)
    axs[2, 1].set_title('P0', fontsize=10, color='red', pad=17)
    axs[2, 1].grid(True)

    plt.subplots_adjust(wspace=0.5,
                        hspace=2)
    plt.tight_layout()
    plt.show()
    df = DataFrame(columns=['Pq', 'Mm', 'Mn', 'Mq', 'Load', 'P0'])
    df['Pq'] = probobilities_list_PQ[:n]
    df['Mm'] = EM_list[:n]
    df['Mn'] = EN_list[:n]
    df['Mq'] = EQ_list[:n]
    df['Load'] = load_list[:n]
    df['P0'] = probobilities_list_P0[:n]
    df.to_excel('ДЗ1 (Задание 2).xlsx')
