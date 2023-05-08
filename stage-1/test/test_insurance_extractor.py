from pathlib import Path
import pytest
import yaml
import pandas as pd
from src.insurance_extractor import (
    find_by_age_range,
    save_df_to_yaml,
    save_df_to_table)


@pytest.fixture(scope='module')
def customers():
    return pd.read_csv('test/dev-latest-customers.txt')


@pytest.fixture(scope='function')
def output_file():
    file_name = 'output.txt'
    yield file_name
    file = Path(file_name)
    if file.is_file():
        file.unlink()


def test_find_by_age_range_returns_all_9_rows(customers):
    rows = find_by_age_range(customers, 0, 100)
    assert len(rows) == 9
    assert list(rows.columns) == ['name', 'phone', 'email']


def test_find_by_age_range_returns_2_rows_given_age_range_40_to_59(customers):
    rows = find_by_age_range(customers, 40, 59)
    expected_rows = [
        ['Macey Bernard', '(0118) 830 5233', 'arcu.iaculis.enim@outlook.edu'],
        ['Otto Hunter', '0908 260 7332', 'aliquam.tincidunt@hotmail.ca']
    ]

    assert 2 == len(rows)
    for i in range(len(expected_rows)):
        assert list(rows.iloc[i, :]) == expected_rows[i]


def test_find_by_age_range_returns_no_rows_given_negative_age_range(customers):
    rows = find_by_age_range(customers, -10, -1)
    assert len(rows) == 0


def test_find_by_age_range_returns_no_rows_given_invalid_range(customers):
    rows = find_by_age_range(customers, 59, 40)
    assert len(rows) == 0


def test_save_df_to_yaml_raises_error_given_invalid_df():
    with pytest.raises(TypeError, match='Invalid dataframe'):
        save_df_to_yaml([], 'root', 'file_name.txt')


def test_save_df_to_yaml_raises_error_given_invalid_root_name(customers):
    with pytest.raises(ValueError, match='Root name must be non-empty string'):
        save_df_to_yaml(customers, '', 'file_name.txt')


def test_save_df_to_yaml_saves_df_properly(customers, output_file):
    expected_customers_dict = customers.to_dict(orient='records')
    root_name = 'customers_to_check'
    save_df_to_yaml(customers, root_name, output_file)
    with open(output_file, 'r') as file:
        data_dict = yaml.safe_load(file)
    assert expected_customers_dict == data_dict[root_name]


def test_save_df_to_table_raises_error_given_invalid_df():
    with pytest.raises(TypeError, match='Invalid dataframe'):
        save_df_to_table([], 'file_name.txt')


def test_save_df_to_table_saves_df_properly(customers, output_file):
    column_names = ['name', 'address', 'phone', 'email']
    save_df_to_table(customers, output_file)
    with open(output_file, 'r') as file:
        data_dict = pd.read_table(file, sep='|',
                                  index_col=1)
    data_dict = data_dict.rename(
        str.strip, axis=1).iloc[1:][column_names].applymap(str.strip)
    data_dict.reset_index(drop=True, inplace=True)
    assert customers[column_names].equals(data_dict[column_names])