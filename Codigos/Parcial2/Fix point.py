from sympy import Symbol
from sympy.solvers import solve
from sympy import ln, sqrt, exp

x = Symbol('x', real=True)

# Example solved exam
g0 = sqrt(10/(x+4))
g2 = ln(7*x**2 + 4*x - 2) - 1
g3 = sqrt((exp(x+1) - 4*x + 2)/7)
g4 = (exp(x+1) - 7*x**2 + 2)/4
g1 = g0  # Function to use
interval_initial = 1  # a
interval_final = 2  # b
apr_initial = 1.5  # x0
precision = 7  # 10^-precision
max_iterations = 100  # Max iterations for algorithm

# Exam complicated g
# g2 = x*exp(x) - x**2 - 4*x - 3
# interval_initial = -6
# interval_final = 3
# apr_initial = -5.9
# precision = 5
# func = g2
# max_iterations = 100


def brute_force1(g_test, n, a, b):
    for i in range(1, n):
        x_test = a + i*(b - a)/n
        gx = g_test.subs(x, x_test).evalf()
        if gx.is_real and not a <= gx <= b:
            print("The given function doesn't have the properties needed, as "
                  "g(" + str(x_test) + ") = " + str(gx) + " is not in [" +
                  str(a) + ", " + str(b) + "].")
            return "f"

    return "s"


def brute_force2(g_test, n, a, b):
    for i in range(1, n):
        x_test = a + i*(b - a)/n
        gx = g_test.subs(x, x_test).evalf()
        if gx.is_real and not abs(gx) <= 1:
            print("The given function doesn't have the properties needed, as "
                  "|g'(" + str(x_test) + ")| = " + str(gx) + " is not less than 1.")
            return "f"

    return "s"


def fix_point(g, x0, precision1, a, b, n_max, bf_split=100):
    # -------------- Check if g([a, b]) e [a, b] ----------------
    ga = g.subs(x, a).evalf()
    gb = g.subs(x, b).evalf()
    gd = 0
    gdd = 0
    critics = []
    critics1 = []
    ks = []
    total_critics = []
    total_critics1 = []
    gcs = []
    theorem = True
    bf1 = False
    bf2 = False

    ans = input("Want to check the theorem for " + str(g) + "? [y/n]")

    if ans == "y":
        while True:
            print("\nChecking g([a,b]) in [a, b]")
            if ga.is_real and not a <= ga <= b:
                print("The given function doesn't have the properties needed, as "
                      "g(a) = " + str(ga) + " is not in [" + str(a) + ", " + str(b)
                      + "].")
                theorem = False
                ans = input("Want to continue the algorithm? [y/n]")
                if ans == "n":
                    return
                else:
                    break

            if gb.is_real and not a <= gb <= b:
                print("The given function doesn't have the properties needed, as "
                      "g(b) = " + str(gb) + " is not in [" + str(a) + ", " + str(b)
                      + "].")
                theorem = False
                ans = input("Want to continue the algorithm? [y/n]")
                if ans == "n":
                    return
                else:
                    break

            # See critic points
            print("\n")
            gd = g.diff(x)
            i = 0
            try:
                critics = list(solve(gd, x))
                total_critics = critics.copy()
                stop = False
                for critic in critics:
                    cr = critic
                    if a <= cr <= b:
                        gc = g.subs(x, cr).evalf()
                        gcs.append(gc)
                        if gc.is_real and not a <= gc <= b:
                            print("The given function doesn't have the properties needed, as "
                                  "g(" + str(cr) + ") = " + str(gc) + " isn't in [" + str(a)
                                  + ", " + str(b) + "].")
                            theorem = False
                            ans = input("Want to continue the algorithm? [y/n]")
                            if ans == "n":
                                return
                            else:
                                stop = True
                                break
                    else:
                        critics.pop(i)
                    i += 1
                if stop:
                    break
            except NotImplementedError:
                print("A brute force approach would be taken, as the local maximums and "
                      "minimums for g(x) cannot be found analytically.")
                success = brute_force1(g, bf_split, a, b)
                bf1 = True
                if success == "s":
                    print("With a brute force approach, it couldn't be found a value that "
                          "do not satisfies the properties needed for the function. "
                          "Still, it is not certain that the property is fully achieved.")
                else:
                    theorem = False
                ans = input("Want to still continue with the algorithm? [y/n]")
                if ans == "n":
                    return
                else:
                    break

            # -------------- Check if g'([a, b]) <= 1 ----------------
            print("\nChecking if |g'([a,b])| <=1")
            ks = [abs(gd.subs(x, a).evalf()), abs(gd.subs(x, b).evalf())]
            if ks[0].is_real and not 0 <= ks[0] <= 1:
                print("The given function doesn't have the properties needed, as "
                      "|g'(a)| = " + str(ks[0]) + " is not less tan 1")
                theorem = False
                ans = input("Want to continue the algorithm? [y/n]")
                if ans == "n":
                    return
                else:
                    break

            if ks[1].is_real and not 0 <= ks[1] <= 1:
                print("The given function doesn't have the properties needed, as "
                      "|g'(b)| = " + str(ks[1]) + " is not less tan 1.")
                theorem = False
                ans = input("Want to continue the algorithm? [y/n]")
                if ans == "n":
                    return
                else:
                    break

            # Check critic points of derivative
            print("\n")
            gdd = gd.diff(x)
            i = 0
            try:
                critics1 = solve(gdd, x)
                total_critics1 = critics1.copy()
                stop = False
                for cr in critics1:
                    if a < cr < b:
                        gc = gd.subs(x, cr).evalf()
                        ks.append(abs(gc))
                        if gc.is_real and not abs(gc) <= 1:
                            print("The given function doesn't have the properties needed, as "
                                  "|g'(" + str(cr) + ")| = " + str(gc) + " is not less tan 1.")
                            theorem = False
                            ans = input("Want to continue the algorithm? [y/n]")
                            if ans == "n":
                                return
                            else:
                                stop = True
                                break
                        else:
                            critics1.pop(i)
                        i += 1

                if stop:
                    break
            except NotImplementedError:
                print("A brute force approach would be taken, as the local maximums and"
                      " minimums cannot be found analytically for g'(x).")
                success = brute_force2(gd, bf_split, a, b)
                bf2 = True
                if success == "s":
                    print("With a brute force approach, it couldn't be found a value that "
                          "do not satisfies the properties needed for the function. "
                          "Still, it is not certain that the property is fully achieved.")
                else:
                    theorem = False
                ans = input("Want to still continue with the algorithm? [y/n]")
                if ans == "n":
                    return
            break

        print("\n")
        if theorem:
            k = max(ks)
            print("The theorem converges, with k = " + str(k))
            ans = input("Want to see step by step solution? [y/n]")
            if ans == "y":
                print("\n------------------------")
                print("Condition g([a,b]) in [a, b]: ")
                print("Evaluating in the frontier of the interval.")
                print("g(" + str(a) + ") = " + str(ga) + " is in [" + str(a) + ", " +
                      str(b) + "]")
                print("g(" + str(b) + ") = " + str(gb) + " is in [" + str(a) + ", " +
                      str(b) + "]")

                if not bf1:
                    print("\nSolving g'(x) = " + str(gd) + " = 0 we find: ")
                    if len(critics) > 0:
                        i = 0
                        for cr in critics:
                            print("g(" + str(cr) + ") = " + str(gcs[i]) + " is in [" +
                                  str(a) + ", " + str(b) + "]")
                            i += 1
                    else:
                        if len(total_critics) > 0:
                            print("It has critic points in " + str(total_critics) + " that are not in [a,b].")
                        else:
                            print("There are no critical points for g(x), for x in [a, b]")
                else:
                    print("By brute force it wasn't founded any value that not"
                          " satisfies the property.")

                print("\nTherefore, g([" + str(a) + ", " + str(b) + "]) is in ["
                      + str(a) + ", " + str(b) + "]")

                print("\nCondition |g'((a,b))| <= k < 1:")
                print("Evaluation the frontier in g'(x)")
                print("|g'(" + str(a) + ")| = " + str(ks[0]) + " is less than 1.")
                print("|g'(" + str(b) + ")| = " + str(ks[1]) + " is less than 1.")

                if not bf2:
                    print("\nSolving g''(x) = " + str(gdd) + " = 0 we find:")
                    if len(critics1) > 0:
                        i = 0
                        for cr in critics1:
                            print("|g(" + str(cr) + ")| = " + str(ks[i]) + " is less than 1.")
                            i += 1
                    else:
                        if len(total_critics1) > 0:
                            print("It has critical points in " + str(total_critics1) + " that are not in [a,b].")
                        else:
                            print("There are no critical points for g'(x), for x in [a, b].")
                else:
                    print("By brute force it wasn't founded any value that not"
                          " satisfies the property.")

                print("\nTherefore k is max(|g'(x)|) = " + str(k))
                input("\n(press enter to continue)")

    # -------------- Execute algorithm ----------------
    x_ant = g.subs(x, x0).evalf()
    print("Initial value g(" + str(x0) + ") = " + str(x_ant))
    xd = g.subs(x, x_ant).evalf()
    i = 2
    diverge = False
    while abs(xd - x_ant) >= 10**-precision1 and i <= n_max:
        print("-----------------")
        print("Iteration " + str(i))
        if abs(x_ant) >= 10**308:
            print("The method diverges, as it tends to infinity.")
            diverge = True
            break
        else:
            print("g(" + str(x_ant) + ") = " + str(xd))
            print("Precision: " + str(abs(xd - x_ant)))
            x_ant = xd
            xd = g.subs(x, xd).evalf()
            i += 1

    if not diverge:
        print("\n-----------------")
        if abs(xd - x_ant) <= 10**-precision1:
            print("Solution founded in " + str(i))
            print("Root of function in " + str(xd))
            print("Precision " + str(abs(xd - x_ant)))
        else:
            print("The algorithm reach its maximum iteration without converging to"
                  "the desired precision.")
            print("Root founded in last iteration " + str(xd))
            print("Precision " + str(abs(xd - x_ant)))


fix_point(g1, apr_initial, precision, interval_initial, interval_final, max_iterations)
