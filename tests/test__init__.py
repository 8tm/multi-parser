import argparse
from unittest.mock import patch

import pytest
from multi_parser import MultiParser


def dummy_executor(arguments: argparse.Namespace) -> None:
    if arguments:
        pass


def dummy_parser_factory() -> argparse.ArgumentParser:
    return argparse.ArgumentParser()


def test_register_existing_parser() -> None:
    multi_parser = MultiParser()
    multi_parser.register_parser('test', dummy_executor, dummy_parser_factory)
    with pytest.raises(ValueError):
        multi_parser.register_parser('test', dummy_executor, dummy_parser_factory)


def test_parse_arguments_with_no_registered_parser() -> None:
    multi_parser = MultiParser()
    with pytest.raises(ValueError):
        multi_parser.parse_arguments(['test'], 'test')


def test_parse_arguments_with_valid_data() -> None:
    def parser_factory() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('--test', action='store_true')
        return parser

    multi_parser = MultiParser()
    multi_parser.register_parser('test', lambda x: None, parser_factory)
    args = multi_parser.parse_arguments(['test', '--test'], 'test')
    assert args.test is True


def test_run_no_args(capsys: pytest.CaptureFixture[str]) -> None:
    with patch('sys.argv', ['script']):
        multi_parser = MultiParser()
        multi_parser.run()
        captured = capsys.readouterr()
        assert "No parser specified. Available parsers are:" in captured.out


def test_run_invalid_parser(capsys: pytest.CaptureFixture[str]) -> None:
    with patch('sys.argv', ['script', 'unknown']):
        multi_parser = MultiParser()
        multi_parser.run()
        captured = capsys.readouterr()
        assert "Invalid or no parser specified. Available parsers are:" in captured.out


def test_run_valid_parser() -> None:
    def parser_factory() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('--test', action='store_true')
        return parser

    def executor(args: argparse.Namespace) -> None:
        assert args.test is True

    with patch('sys.argv', ['script', 'test', '--test']):
        multi_parser = MultiParser()
        multi_parser.register_parser('test', executor, parser_factory)
        multi_parser.run()
