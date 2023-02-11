def funk(*args, **kwargs):
    print("Liczba przekazanych parametrów *args:", len(args))
    for arg in args:
        print("Args - Wartość:", arg)

    print("Liczba przekazanych parametrów **kwargs:", len(kwargs))
    for key, item in kwargs.items():
        print("Kwargs - ", "Klucz:", key, "Wartość:", item)