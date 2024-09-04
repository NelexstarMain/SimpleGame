def decorator():
    class New:
        def non() -> None:
            print("Non-static method")
    return New


@decorator
class Test:
    def __init__(self) -> None:
        pass    

test = Test()
test.non()  # Output: Non-static method
