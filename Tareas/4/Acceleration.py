from sympy import Symbol
import math as m


x = Symbol('x', real=True)


def bisection(function_intervals, tol, n_max=100):
    f1 = function_intervals[0]
    a = function_intervals[1]
    b = function_intervals[2]
    l_bis = list()
    l0 = abs(b - a)
    i = 0
    while abs(b - a) >= l0*tol and i < n_max:
        x1 = (b + a)/2
        l_bis.append(x1)
        if abs(f1(x1)) <= tol:
            break
        if f1(x1)*f1(a) < 0:
            b = x1
        else:
            a = x1

        i += 1

    return l_bis, [f1, a, b]


def aitken(method, tol, *args, symbolic=False):
    p1 = list()
    q1 = list()
    f1 = args[0]
    calculate_q = True
    nums, args = method(args, tol, n_max=4)
    p1 += nums
    q1.append(p1[0] - ((p1[1] - p1[0])**2/((p1[2] - p1[1]) - (p1[1] - p1[0]))))
    if (not symbolic and abs(f1(q1[0])) <= tol) or (symbolic and abs(f1.subs(x, q1[0]).evalf()) <= tol):
        return q1
    q1.append(p1[1] - ((p1[2] - p1[1]) ** 2 / ((p1[3] - p1[2]) - (p1[2] - p1[1]))))

    i = 1
    while True:
        if calculate_q:
            if (not symbolic and abs(f1(q1[i])) <= tol) or (symbolic and abs(f1.subs(x, q1[i]).evalf()) <= tol) \
                    or abs(q1[i] - q1[i - 1]) <= tol:
                calculate_q = False
            else:
                i += 1
                nums, args = method(args, tol, n_max=1)
                if nums[0] == p1[-1]:
                    nums.pop(0)
                p1 += nums
                q1.append(p1[i] - (p1[i+1] - p1[i])**2/((p1[i+2] - p1[i+1]) - (p1[i+1] - p1[i])))
        else:
            nums, args = method(args, tol)
            if nums[0] == p1[-1]:
                nums.pop(0)
            p1 += nums
            break

    return p1, q1


def print_lists(list1, list2, str_list1="List1", str_list2="List2",
                name_file="List.txt", title="Comparison", decimals=5):

    def round_str(er, decimals1):
        er_str = list(str(er).split("e"))

        er_str[0] = str(round(float(er_str[0]), decimals1))
        if len(er_str) > 1:
            return er_str[0] + "e" + er_str[1]
        else:
            return er_str[0]

    # Create file
    file = open(name_file, "w+")
    max_len = max([len(list1), len(list2)])

    # Printing initial table
    spaces = " "*(decimals + 9)
    l_sp = len(spaces)
    file.write(title + "\n")
    file.write("i" + spaces + str_list1 + spaces + str_list2
               + spaces + "Error1" + spaces + "Error2")

    for i in range(max_len):
        # Make sure same spaces to i.
        spaces_i = " "*(l_sp + 1 - len(str(i)))
        file.write("\n")

        # Calculating number of list1
        if i < len(list1):
            num1 = round_str(list1[i], decimals)
            if i != 0:
                er1 = round_str(abs(list1[i] - list1[i-1]), 4)
            else:
                er1 = ""
        else:
            num1 = " "*(decimals + 2)
            er1 = ""

        # Calculating number of list 2
        if i < len(list2):
            num2 = round_str(list2[i], decimals)
            if i != 0:
                er2 = round_str(abs(list2[i] - list2[i-1]), 4)
            else:
                er2 = ""
        else:
            num2 = " "*(decimals + 2)
            er2 = ""

        spaces12 = " "*(l_sp + 5 - len(str(num1)))
        spaces1er = " "*(l_sp + 5 - len(str(num2)))
        spaces_er1er2 = " "*(l_sp + 6 - len(str(er1)))
        file.write(str(i) + spaces_i + num1 + spaces12 + num2
                   + spaces1er + str(er1) + spaces_er1er2 + str(er2))
    file.close()


def newton(function_initial, tol, n_max=100):
    f1 = function_initial[0]
    x0 = function_initial[1]
    f1d = f1.diff(x)
    xs = [x0]

    f1di = f1d.subs(x, x0).evalf()
    if f1di == 0:
        return xs, [f1, x0]

    xs.append(x0 - f1.subs(x, x0).evalf()/f1di)
    j = 2
    while abs(xs[-1] - xs[-2]) >= tol and j < n_max:
        if abs(xs[-1]) <= tol:
            break
        f1di = f1d.subs(x, xs[-1]).evalf()
        if f1di == 0:
            return xs, [f1, xs[-1]]
        xs.append(xs[-1] - f1.subs(x, xs[-1])/f1di)
        j += 1
    return xs, [f1, xs[-1]]


def steffensen(tol, *args):
    return aitken(newton, tol, *args, symbolic=True)


def secant(f1, x0=0.0, x1=1.0, tol=1e-15, n_max=1e5):
    fx0 = f1(x0)
    if abs(fx0) <= tol:
        return [x0]
    fx1 = f1(x1)
    cont = 1
    den = fx1 - fx0

    # Calculate first value
    x2 = x1 - fx1 * (x1 - x0) / den
    xs = [x1, x2]
    while abs(x2 - x1) > tol and abs(fx1) > tol and den != 0 and cont < n_max:
        # Shift variables
        x0 = x1
        fx0 = fx1
        x1 = x2
        fx1 = f1(x2)
        den = fx1 - fx0
        cont += 1

        # Calculate next iteration
        x2 = x1 - fx1*(x1 - x0)/den
        xs.append(x2)

    return xs


def muller(f1, x0=0.0, x1=1.0, x2=2.0, tol=1e-15, n_max=1e5):
    fx0 = f1(x0)
    if abs(fx0) <= tol:
        return [x0]
    fx1 = f1(x1)
    if abs(fx1) <= tol:
        return [x1]
    fx2 = f1(x2)
    if abs(fx2) <= tol:
        return [x2]

    # Calculating x3
    cont = 1
    xs = [x2]
    h1 = x1 - x0
    h2 = x2 - x1
    d1 = (fx1 - fx0) / h1
    d2 = (fx2 - fx1) / h2
    a = (d2 - d1) / (h2 + h1)
    b = d2 + (h2 * a)
    d = m.sqrt(abs(b ** 2 - 4 * (fx2 * a)))
    if abs(b - d) < abs(b + d):
        e = b + d
    else:
        e = b - d
    x3 = x2 - (2 * fx2) / e
    xs.append(x3)

    while abs(x3 - x2) > tol and abs(fx2) >= tol and cont < n_max:
        # Shifting variables for next iteration
        x0 = x1
        fx0 = fx1
        x1 = x2
        fx1 = fx2
        x2 = x3
        fx2 = f1(x3)
        cont += 1

        # Calculating next value
        h1 = x1 - x0
        h2 = x2 - x1

        d1 = (fx1 - fx0) / h1
        d2 = (fx2 - fx1) / h2

        a = (d2 - d1) / (h2 + h1)
        b = d2 + (h2 * a)
        if b**2 > 4*fx2*a:
            d = m.sqrt(b ** 2 - 4 * (fx2 * a))
        else:
            d = 0
        if abs(b - d) < abs(b + d):
            e = b + d
        else:
            e = b - d

        x3 = x2 - (2 * fx2) / e
        xs.append(x3)

    return xs


def g(x1):
    return x1**3 - 3*x1 + 2


def f(x1):
    return m.exp(3*x1 - 12) + x1*m.cos(3*x1) - x1**2 + 4


h = x**3 - 3*x + 2


p = secant(g, x0=2.2, x1=2.1, tol=1e-5)
q = muller(g, x0=2.2, x1=2.1, x2=2.0, tol=1e-5)
print_lists(p, q, str_list1="Seca.", str_list2="Mull.", name_file="Muller.txt", title="Secant vs Muller",
            decimals=8)

p, q = steffensen(1e-5, h, 2)
print_lists(p, q, str_list1="Newt.", str_list2="Stef.", name_file="Steffensen.txt", title="Newton vs Steffensen",
            decimals=8)

p, q = aitken(bisection, 1e-5, f, 2, 3)
print_lists(p, q, str_list1="Bise.", str_list2="Aitk.", name_file="Aitken.txt", title="Bisection vs Aitken",
            decimals=8)
