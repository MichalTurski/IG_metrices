from os import listdir
from os.path import isfile, join
import pandas as pd

from MAE_parser import MAE_parser


def df_from_dir(dir_path):
    mae_parser = MAE_parser()
    xml_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    xml_files.sort()
    dfs_list = []
    for file_id, file in enumerate(xml_files):
        df = mae_parser.parse_file(join(dir_path, file))
        df['file_id'] = file_id
        dfs_list.append(df)
    return pd.concat(dfs_list, sort=False)


def main():
    gold_df = df_from_dir("gold_anots")
    print(gold_df.columns)
    app_df = df_from_dir("app_anots")
    print(app_df.head())


if __name__ == '__main__':
    main()
