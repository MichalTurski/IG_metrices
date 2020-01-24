import os
import xmlschema
import pandas as pd
import re


class MAE_parser:
    def __init__(self):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        self.mae_schema = xmlschema.XMLSchema(os.path.join(curr_path, 'mae_schema.xsd'))

    @staticmethod
    def __category_to_df__(tags_dict, category):
        if category in tags_dict:
            annotations_list = tags_dict[category]
            df = pd.DataFrame(annotations_list)
            df = df.rename(columns={"@id": "id", "@spans": "spans", "@text": "text", "@RodzajAC": "RodzajAC"})
            df['begin'] = df['spans'].apply(lambda x: int(re.split('~|,', x)[0]))
            df['end'] = df['spans'].apply(lambda x: int(re.split('~|,', x)[1]))
            df = df.drop(['spans'], axis=1)
            df['category'] = category
        else:
            df = pd.DataFrame(columns=[])
        return df

    @staticmethod
    def __normalize_spans__(anot_df, text):
        removed_count = 0
        for i, char in enumerate(text):
            if not char.isalnum():
                anot_df['begin'] = anot_df['begin'].apply(lambda val: val - 1 if val + removed_count > i else val)
                anot_df['end'] = anot_df['end'].apply(lambda val: val - 1 if val + removed_count > i else val)
                removed_count += 1
        return anot_df, len(text) - removed_count, removed_count

    def parse_file(self, file_path):
        self.mae_schema.validate(file_path)
        mae_dict = self.mae_schema.to_dict(file_path)
        tags_dict = mae_dict['TAGS']
        anot_dfs_list = [self.__category_to_df__(tags_dict, 'SEPARATOR'),
                         self.__category_to_df__(tags_dict, 'Attribute'), self.__category_to_df__(tags_dict, 'Deontic'),
                         self.__category_to_df__(tags_dict, 'aIm'), self.__category_to_df__(tags_dict, 'oBject'),
                         self.__category_to_df__(tags_dict, 'aCtor'),
                         self.__category_to_df__(tags_dict, 'ActivCondition'),
                         self.__category_to_df__(tags_dict, 'Method')]
        anot_df = pd.concat(anot_dfs_list, sort=False).reset_index(drop=True)
        anot_df.sort_values(by=['begin'], inplace=True)
        anot_df.reset_index(drop=True, inplace=True)
        # print(anot_df['end'].tail())
        anot_df, text_len, removed = self.__normalize_spans__(anot_df, mae_dict['TEXT'])
        # print(anot_df['end'].tail())
        print(f'File {file_path} text length = {text_len}, removed = {removed}.')
        return anot_df
