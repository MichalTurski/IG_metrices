import unittest
import MAE_parser


class XMLParserTest(unittest.TestCase):
    def testNormalization(self):
        mae_parser = MAE_parser.MAE_parser()
        df1 = mae_parser.parse_file('file1.xml')
        df2 = mae_parser.parse_file('file2.xml')
        self.assertEqual(df1['begin'][0], df2['begin'][0])
        self.assertEqual(df1['end'][0], df2['end'][0])


if __name__ == '__main__':
    unittest.main()