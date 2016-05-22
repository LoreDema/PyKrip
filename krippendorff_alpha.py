def nominal_metric(a, b):
    if a is None or b is None:
        return 0
    return a != b


def interval_metric(a, b):
    if a is None or b is None:
        return 0
    return (a-b)**2


def ratio_metric(a, b):
    if a or b:
        return 0
    return ((a-b)/(a+b))**2


def ordinal_metric(a, b, v):
    return (sum(v) - (a + b) / 2)**2


def build_values_by_units_matrix(data, classes_values):
    values_by_units_matrix = []
    for i in classes_values:
        values = []
        for j in range(len(data)):
            values.append(data[j].count(i))
        values_by_units_matrix.append(values)

    return values_by_units_matrix


def krippendorff_alpha(data, classes_values, metric=nominal_metric):
    classes_values = sorted(classes_values)
    t_data = map(list, zip(*data))
    values_by_units_matrix = build_values_by_units_matrix(t_data, classes_values)
    t_values_by_units_matrix = map(list, zip(*values_by_units_matrix))
    np = []
    for i, x in enumerate(values_by_units_matrix):
        npi = 0.
        for j, y in enumerate(x):
            if sum(t_values_by_units_matrix[j]) > 1:
                npi += y
        np.append(npi)

    nup = [float(sum(x)) for x in t_values_by_units_matrix]
    sum1 = 0.
    for u, unit in enumerate(t_values_by_units_matrix):
        sum11 = 0.
        for i, annotation1 in enumerate(unit):
            for j in range(i+1, len(unit)):
                # print annotation1, t_data[u][j], metric(annotation1, t_data[u][j])
                if metric in (ordinal_metric,):
                    sum11 += unit[i] * unit[j] * metric(i, j, range(i, j + 1))
                else:
                    sum11 += unit[i] * unit[j] * metric(i, j)
        try:
            sum1 += sum11 / float(nup[u] - 1)
            # print sum11, '/ (', nup[u], '- 1)'
        except ZeroDivisionError:
            pass

    sum2 = 0.
    for i, npc in enumerate(np):
        for j in range(i+1, len(np)):
            if metric in (ordinal_metric,):
                sum2 += npc * np[j] * metric(i, j, range(i, j + 1))
            else:
                sum2 += npc * np[j] * metric(i, j)
    try:
        return 1 - (sum(np) - 1) * (sum1 / sum2)
    except ZeroDivisionError:
        return 0

if __name__ == '__main__':
    # array = [d.split() for d in data]  # convert to 2D list of string items
    matrix = [
        [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None],
        [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3],
        [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
        [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None]
    ]
    # matrix = [
    #    [1, 2, 3],
    #    [1, 2, 3],
    #    [1, 2, 3]
    # ]
    classes = range(1, 6)
    print 'ordinal', krippendorff_alpha(matrix, classes, metric=ordinal_metric)
    print 'interval', krippendorff_alpha(matrix, classes, metric=interval_metric)
    print 'nominal', krippendorff_alpha(matrix, classes, metric=nominal_metric)
