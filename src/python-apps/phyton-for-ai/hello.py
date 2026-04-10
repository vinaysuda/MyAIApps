def check_weather(temperature):
    if temperature >= 25:
        return "Its hot!!!"
    else:
        return "Its cool!!!"


def greet(f_name, age):
    return f"My name is {f_name} and my age is {age}."


def mutliple_returns(num1, num2):
    addition_result = num1 + num2
    minus_result = num1 - num2
    multiply_result = num1 * num2
    return addition_result, minus_result, multiply_result


print(greet("Pranay", 36))
print(check_weather(temperature=15))

(result_add, result_sub, result_multiply) = mutliple_returns(20, 10)

print(
    f"Multiple returns result is, Add: {result_add}, Sub: {result_sub}, Multiply: {result_multiply}"
)
