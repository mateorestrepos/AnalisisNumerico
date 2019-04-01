from sympy import Symbol
from sympy import sin


# Variables necessary to the program to work
x = Symbol('x', real=True)
d2 = "d2"
s = "s"
SUP = str.maketrans("4567890", "⁴⁵⁶⁷⁸⁹⁰")

# Parameters
# Parameters for newton modified
f_modified = x**3 - x**2 - x + 1 + (sin(x-1))**2
initial_conditions_modified = 0.5
tolerance_modified = 10**-5

# Parameters for newton
initial_conditions = -0.5
tolerance = 10**-5


def newton(f1, x0, tol):
    f1d = f1.diff(x)
    xs = [x0]

    f1di = f1d.subs(x, x0).evalf()
    if f1di == 0:
        return xs, d2

    xs.append(x0 - f1.subs(x, x0).evalf()/f1di)
    while abs(xs[-1] - xs[-2]) > tol:
        if abs(xs[-1]) <= tol:
            break
        f1di = f1d.subs(x, xs[-1]).evalf()
        if f1di == 0:
            return xs, d2
        xs.append(xs[-1] - f1.subs(x, xs[-1])/f1di)
    return xs, s


def newton_modified(f1, x0, tol):
    return newton(f1/f1.diff(x), x0, tol)


def print_list(l, f1):
    i = 0
    ant = 0
    for elem in l:
        print("Iteration " + str(i))
        fn = f1.subs(x, elem).evalf()
        print("f(" + str(elem) + ") = " + str(fn))
        if i != 1:
            print("With a precision of: " + str(abs(elem - ant)))

        print("-------------------------------------")
        ant = elem
        i += 1


def ui(f1, x0, tol, x0_newton, tol_newton):
    ans = input("Want to check multiplicity for a certain value? [y/n]")
    if ans == "y":
        xr = float(input("Insert value: "))

        f_temp = f1
        m = 0
        fd = "f"
        while f_temp.subs(x, xr).evalf() == 0:
            ft_sub = f_temp.subs(x, xr)
            print(fd + "(" + str(xr) + ") = " + str(ft_sub.evalf()))
            f_temp = f_temp.diff(x)
            m += 1
            if m <= 3:
                fd += "'"
            else:
                fd = ("f" + str(m)).translate(SUP)

        ft_sub = f_temp.subs(x, xr)
        print(fd + "(" + str(xr) + ") = " + str(ft_sub.evalf()))
        print("It has a multiplicity " + str(m) + " because, every derivative before is 0 except for"
                                                  " the " + str(m) + "th derivative.")

        input("(press enter to continue)")
    print("\n")
    ans = input("Want to check if there is a simple root in a interval?[y/n]")
    if ans == "y":
        a = float(input("Insert the start of the interval: "))
        b = float(input("Insert the last value of the interval: "))

        print("\nRemember to check and remark that f, f' are continuous in the given interval.")
        print("Let's see if there is a sign change in the interval.")

        fa = f1.subs(x, a).evalf()
        fb = f1.subs(x, b).evalf()
        print("\nf(" + str(a) + ") = " + str(fa))
        print("f(" + str(b) + ") = " + str(fb))

        if fa*fb < 0:
            print("\nIt is seen that f(a) and f(b) change sign. To show that this root is"
                  " unique, let's see that f'(x) doesn't change sign. Therefore: ")

            fd = f1.diff(x)
            fda = fd.subs(x, a).evalf()
            fdb = fd.subs(x, b).evalf()
            print("\nf'(" + str(a) + ") = " + str(fda))
            print("f'(" + str(b) + ") = " + str(fdb))

            if fda*fdb > 0:
                print("\nIt is seen that f'(a) and f'(b) doesn't change sign. Therefore, there is a"
                      " unique root in [" + str(a) + ", " + str(b) + "].")
            else:
                print("\nAs f'(a) and f'(b) change sign, there isn't evidence to say there is a unique"
                      " root in the interval.")
        else:
            print("\nAs f(a) and f(b) doesn't change sign, there isn't evidence to say there is a"
                  " unique root in the interval.")

        input("(press enter to continue)")

    ans = int(input("\nWant to apply modified newton (1), newton (2) or both (3)?"))
    if ans == 1:
        print("\nNewton modified: ")
        nums, success = newton_modified(f1, x0, tol)
        print_list(nums, f1)
        last = nums[-1]
        if success == d2:
            print("It failed because f'(" + str(last) + ")**2 - f(" + str(last)
                  + ")f''(" + str(last) + ") became 0.")
    elif ans == 2:
        print("\nNewton: ")
        nums, success = newton(f1, x0_newton, tol_newton)
        last = nums[-1]
        print_list(nums, f1)
        if success == d2:
            print("It failed because f'(" + str(last) + ") became 0.")
    else:
        print("\nNewton modified: ")
        nums, success = newton_modified(f1, x0, tol)
        print_list(nums, f1)
        last = nums[-1]
        if success == d2:
            print("It failed because f'(" + str(last) + ")**2 - f(" + str(last)
                  + ")f''(" + str(last) + ") became 0.")
        input("(press enter to continue)")

        print("\nNewton: ")
        nums, success = newton(f1, x0_newton, tol_newton)
        last = nums[-1]
        print_list(nums, f1)
        if success == d2:
            print("It failed because f'(" + str(last) + ") became 0.")


ui(f_modified, initial_conditions_modified, tolerance_modified, initial_conditions, tolerance)
