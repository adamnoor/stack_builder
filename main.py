from view_homepage import run_program


def start_main(run_type):
    if run_type == "test":
        pass
    elif run_type == "production":
        run_program()
    else:
        print("Something went wrong!")


if __name__ == '__main__':
    start_main("production")
