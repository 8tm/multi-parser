import argparse
from multi_parser import MultiParser


def first_parser_factory():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--param-1', action='store_true')
    parser.add_argument('--param-2', action='store_true')
    return parser


def second_parser_factory():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--param-2', action='store_true')
    parser.add_argument('--param-3', action='store_true')
    parser.add_argument('--param-5', action='store_true')
    return parser


def first_app_executor(args) -> None:
    print("First app called with arguments:", args)


def second_app_executor(args) -> None:
    print("Second app called with arguments:", args)


def main():
    # Create MultiParser instance
    multi_parser = MultiParser()

    # Add parser for first and second app
    multi_parser.register_parser('first',  first_app_executor,  first_parser_factory)
    multi_parser.register_parser('second', second_app_executor, second_parser_factory)

    # Run script
    multi_parser.run()


if __name__ == "__main__":
    main()
