import functions_one as fun


def preview(funct, data, title = None):
    # If no custom title is provided, use name of the given function
    if not title:
        title = funct.__name__
    print(f"* {title} *")
    print(f"Data: {data}\nResult: {funct(data)}\n\n")


preview(fun.reverse_sentence, "I LOVE YOU MOM")
preview(fun.has_33, [4, 3, 2, 6, 9])
preview(fun.get_unique, [2, 3, 1, 2, 2, 3, 5, 4], "Get unique numbers")
preview(fun.spy_game, [1,0,2,4,0,5,7], "Check if numbers seq contains 007 in order")
preview(fun.filter_prime, [1, 2, 3, 4, 5, 6, 7, 8])
preview(fun.sphere_volume, 12.53, "Compute the volume of a sphere given its radius")