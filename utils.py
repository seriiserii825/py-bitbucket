def pretty_print(value, error=False):
    if error:
        print("[red]===============================")
        print(value)
        print("[red]===============================")
    else:
        print("[blue]===============================")
        print(value)
        print("[blue]===============================")
