import pandas as pd
import yaml
from tabulate import tabulate
import argparse


def find_by_age_range(customers_df, from_age, to_age):
    """
    Filters the dataframe by age range.

    Args:
        customers_df (Dataframe): The customer dataframe.
        from_age (int): Minimum age (inclusive).
        to_age (int): Maximum age (inclusive).

    Returns:
        Dataframe: The filtered dataframe with columns name, phone and email.
    """
    df = customers_df[
        (customers_df.age >= from_age) &
        (customers_df.age <= to_age)
        ][['name', 'phone', 'email']]
    return df


def save_df_to_table(df, file_name):
    """
    Saves a dataframe in github table format to a file.

    Args:
        df (Dataframe): The dataframe.
        file_name (string): Name of file.

    Returns:
        None

    Raises:
        TypeError: If dataframe is invalid.
    """
    if type(df) != pd.core.frame.DataFrame:
        raise TypeError('Invalid dataframe')
    with open(file_name, 'w') as file:
        headers = list(df.columns)
        table = [list(row) for row in df.to_numpy()]
        file.write(tabulate(table, headers=headers,
                            showindex='always', tablefmt='github'))


def save_df_to_yaml(df, root_name, file_name):
    """
    Saves a dataframe as a YAML file.

    Args:
        df (Dataframe): The dataframe.
        root_name: The root element
        file_name (string): Name of file.

    Returns:
        None

    Raises:
        TypeError: If dataframe is invalid.
        ValueError: If root_name is not a non-empty string
    """
    if type(df) != pd.core.frame.DataFrame:
        raise TypeError('Invalid dataframe')
    if type(root_name) != str or len(root_name) == 0:
        raise ValueError('Root name must be non-empty string')
    with open(file_name, 'w') as file:
        yaml.dump({root_name: df.to_dict(orient='records')},
                  file, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insurance Extractor')
    parser.add_argument('input_file', type=str, help='Path to customer file')
    parser.add_argument('-o', '--output_file', type=str,
                        help='Path to output file')
    parser.add_argument('-f', '--file_format', type=str, default='t',
                        help='Output file format [t: table, y: YAML]')
    args = parser.parse_args()

    customers_df = pd.read_csv(args.input_file)
    filtered_df = find_by_age_range(customers_df, 40, 59)

    if args.output_file:
        match args.file_format:
            case 'y':
                save_df_to_yaml(filtered_df,
                                '''Affected Customers'''
                                f'({len(filtered_df)}/{len(customers_df)})',
                                args.output_file)
            case _:
                save_df_to_table(filtered_df, args.output_file)
    else:
        print(filtered_df.reset_index(drop=True))
