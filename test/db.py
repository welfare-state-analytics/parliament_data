import unittest
import pandas as pd
import yaml

class Test(unittest.TestCase):

    # Test that each column in the MP DB contains at least 95% valid values
    def test_mp_db(self):
        lower_limit = 0.95
        
        mp_db = pd.read_csv("db/mp/members_of_parliament.csv")

        total = len(mp_db)
        mp_db_columns = mp_db.columns
        print("Columns:", ", ".join(list(mp_db_columns)))
        mp_db_columns = dict(name=1.0,
                            party=0.95,
                            district=0.95,
                            chamber=0.95,
                            id=1.0)
        print("Test:", ", ".join(list(mp_db_columns)))
        for column, percentage in mp_db_columns.items():
            column_count = len(mp_db[mp_db[column].isnull()])
            valid_ratio = 1. - (column_count / total)
            print(column, valid_ratio)
            self.assertGreaterEqual(valid_ratio, percentage)

    def test_not_decreased(self):
        mp_db = pd.read_csv("db/mp/members_of_parliament.csv")
        data = None
        dpath = "test/mpstats.yml"
        with open(dpath, 'r') as stream:
            data = yaml.safe_load(stream)

        data_out = {}
        for column, number in data.items():
            column_count = len(mp_db[mp_db[column].notnull()])
            data_out[column] = column_count
            self.assertGreaterEqual(column_count, number)

        with open(dpath, 'w') as outfile:
            yaml.dump(data_out, outfile, default_flow_style=False)

if __name__ == '__main__':
    unittest.main()
