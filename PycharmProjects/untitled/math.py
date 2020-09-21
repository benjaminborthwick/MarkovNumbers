for a in range(0, 10):
    for b in range(0, 10):
        for c in range(0, 10):
            product = (a * 100 + b * 10 + c) * (b * 100 + c * 10 + a) * (c * 100 + a * 10 + b)
            if str(product)[-1] == "6":
                print(product)
                two = 0
                three = 0
                four = 0
                five = 0
                six = 0
                eight = 0
                for digit in str(product):
                    if digit == "2":
                        two += 1
                    elif digit == "3":
                        three += 1
                    elif digit == "4":
                        four += 1
                    elif digit == "5":
                        five += 1
                    elif digit == "6":
                        six += 1
                    elif digit == "8":
                        eight += 1
                if two == 3 and three == 2 and four == 1 and five == 1 and six == 1 and eight == 1:
                    answer = [product, a, b, c]
print("Answer:", answer)
