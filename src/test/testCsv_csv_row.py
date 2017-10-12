# -*- coding: utf-8 -*-
"""
Unit test for csv_row.py
"""

import unittest
import time
import pandas
import random
import math
from pandas.util.testing import assert_frame_equal
from csv_row import csvrow_deleteRow
from csv_row import csvrow_deleteRows
from csv_row import csvrow_sampling
from csv_row import csvrow_matchRowNumbers
from csv_file import csvfl_csvToDataFrame
from csv_file import csvfl_dataFrameToCsv

dataPath = r".\data\sample_large_data.csv"
dataDir =  r".\data"

class TestCsvFile(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #  csv_fileとの連携テスト
    def testCsv_csvrow_combined_test(self):
        result, msg, source, countRows, countColumns = csvfl_csvToDataFrame (dataPath, 1)
        
        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, "北海道")
        self.assertEqual((1, "Complete.", 8251),(result, msg, len(rowNumbers)))
        
        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, "愛知県")
        self.assertEqual((1, "Complete.", 7693),(result, msg, len(rowNumbers)))

        #result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.1)
        #self.assertEqual((1, "Complete.", 6, 7),(result, msg, countRows, countColumns))        
 
        #result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "csvrow_combined_test_1.csv")
        #self.assertEqual((1, "Complete.",  "csvrow_combined_test_1.csv"), (result, msg, newName))        
 
        
        #result, msg, newName = csvfl_dataFrameToCsv (data_actual, 1, True, dataDir, "csvcol_combined_test_2.csv")
        #self.assertEqual((1, "Complete.",  "csvcol_combined_test_2.csv"), (result, msg, newName))

    
    # sourceのformatが不正
    def testCsv_csvrow_deleteRow1(self):
        source = [["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 2)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_deleteRow2(self):
        source = pandas.DataFrame()
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 2)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [rowNumber]が[int]のデータ型以外の場合
    def testCsv_csvrow_deleteRow3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, '2')
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumberがsourceの範囲を超えていた（rowNumber　＜　１）
    def testCsv_csvrow_deleteRow4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 0)
        self.assertEqual((0, "Error : The specified rowNumber was out of range. [0]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumberがsourceの範囲を超えていた
    #TODO: rownumber > source's total row
    def testCsv_csvrow_deleteRow5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 3)
        self.assertEqual((0, "Error : The specified rowNumber was out of range. [3]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumber=1の場合Errorとする
    def testCsv_csvrow_deleteRow6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 1)
        self.assertEqual((0, "Error :Cannot delete the header row.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values
    def testCsv_csvrow_deleteRow7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                  ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                  ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                  ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                  ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                  ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                  ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                  ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 2)
        self.assertEqual((1, "Complete.", 5, 9),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values
    # TODO: Delete last row
    def testCsv_csvrow_deleteRow8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"]])
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 6)
        self.assertEqual((1, "Complete.", 5, 9),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

# PG_32
    # sourceのformatが不正
    def testCsv_csvrow_deleteRows1(self):
        source = [["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [1])
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_deleteRows2(self):
        source = pandas.DataFrame()
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [1])
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [rowNumbers]が[list]のデータ型以外の場合
    def testCsv_csvrow_deleteRows3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # rowNumbersがNULL
    def testCsv_csvrow_deleteRows4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [])
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [rowNumbers] 内の要素が[int]のデータ型以外の場合
    def testCsv_csvrow_deleteRows5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, ['2'])
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたrowNumbersがsourceの範囲を超えていた（rowNumbers　＜　1）
    def testCsv_csvrow_deleteRows6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [0,2])
        self.assertEqual((0, "Error : The specified rowNumber in the rowNumbers was out of range. [[0, 2]]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたrowNumbersがsourceの範囲を超えていた
    #TODO: rownumbers > source's total row
    def testCsv_csvrow_deleteRows7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"]])

        data_expected = pandas.DataFrame()
        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [4,5])
        self.assertEqual((0, "Error : The specified rowNumber in the rowNumbers was out of range. [[4, 5]]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # rowNumbersに「1」が含まれていた場合Errorとする
    def testCsv_csvrow_deleteRows8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [1,2])
        self.assertEqual((0, "Error :Cannot delete the header row.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values
    # TODO: delete 1 row
    def testCsv_csvrow_deleteRows9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                          ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                          ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [5])
        self.assertEqual((1, "Complete.", 5, 9),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values
    # TODO: delete many rows
    def testCsv_csvrow_deleteRows10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                          ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                          ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"]])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [2, 3, 6])
        self.assertEqual((1, "Complete.", 3, 9),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values
    # TODO: delete all rows
    def testCsv_csvrow_deleteRows11(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])
        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"]])

        result, msg, data_actual, countRows, countColumns = csvrow_deleteRows(source, [2, 3, 4, 5, 6])
        self.assertEqual((1, "Complete.", 1, 9),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

# PG_33
    # sourceのformatが不正
    def testCsv_csvrow_sampling1(self):
        source = [["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.1)
        self.assertEqual((0, "Error : The source was invalid format.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # sourceがNULL
    def testCsv_csvrow_sampling2(self):
        source = pandas.DataFrame()
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.1)
        self.assertEqual((0, "Error : The source was empty.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 予期しなかったError
    # [samplingRatio]が[float]のデータ型以外の場合
    def testCsv_csvrow_sampling3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 1)
        self.assertEqual((-1, "Error : An unexpected error occurred.", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合（samplingRatio　＜　0）
    def testCsv_csvrow_sampling4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, -0.2)
        self.assertEqual((0, "Error : The samplingRatio must be in range 0 to 1. [-0.2]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合（samplingRatio　＞　1）
    def testCsv_csvrow_sampling5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"]])
        data_expected = pandas.DataFrame()

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 1.1)
        self.assertEqual((0, "Error : The samplingRatio must be in range 0 to 1. [1.1]", 0, 0),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values（samplingRatio　＝　0）
    def testCsv_csvrow_sampling6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        data_expected = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"]])
        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.0)
        self.assertEqual((1, "Complete.", 1, 9),(result, msg, countRows, countColumns))
        assert_frame_equal(data_expected, data_actual)

    # Case: input correct values（samplingRatio　＝　1）
    def testCsv_csvrow_sampling7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 1.0)
        self.assertEqual((1, "Complete.", 6, 9),(result, msg, countRows, countColumns))

    # Case: input correct values(0　＜　samplingRatio　＜　1)
    def testCsv_csvrow_sampling8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, data_actual, countRows, countColumns = csvrow_sampling(source, 0.5)
        self.assertEqual((1, "Complete.", 4, 9),(result, msg, countRows, countColumns))

# PG_34
    # sourceのformatが不正
    def testCsv_csvrow_matchRowNumbers1(self):
        source = [["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                  ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]]

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, "国")
        self.assertEqual((0, "Error : The source was invalid format.", []),(result, msg, rowNumbers))

    # sourceがNULL
    def testCsv_csvrow_matchRowNumbers2(self):
        source = pandas.DataFrame()

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, "国")
        self.assertEqual((0, "Error : The source was empty.", []),(result, msg, rowNumbers))

    # 予期しなかったError
    # [targetColumnNumber]が[int]のデータ型以外の場合
    def testCsv_csvrow_matchRowNumbers3(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, '2', "国")
        self.assertEqual((-1, "Error : An unexpected error occurred.", []),(result, msg, rowNumbers))

    # targetColumnNumberがsourceの範囲を超えていた（targetColumnNumber　＜　１）
    def testCsv_csvrow_matchRowNumbers4(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 0, "国")
        self.assertEqual((0, "Error : The specified targetColumnNumber was out of range. [0]", []),(result, msg, rowNumbers))

    # targetColumnNumberがsourceの範囲を超えていた
    #TODO: rownumbers > source's total row
    def testCsv_csvrow_matchRowNumbers5(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 10, "国")
        self.assertEqual((0, "Error : The specified targetColumnNumber was out of range. [10]", []),(result, msg, rowNumbers))

    # 予期しなかったError
    # [key]が[string]のデータ型以外の場合
    def testCsv_csvrow_matchRowNumbers6(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, 3)
        self.assertEqual((-1, "Error : An unexpected error occurred.", []),(result, msg, rowNumbers))

    # keyと一致する列が一つもなかった
    # TODO: Error key 1 byte, value soure 2 byte
    def testCsv_csvrow_matchRowNumbers7(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-28","番","4","ヤマグチケン","","11111","50","30","23242"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 4, "ﾔﾏｸﾞﾁｹﾝ")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = ﾔﾏｸﾞﾁｹﾝ, targetColumnNumber = 4]", []),(result, msg, rowNumbers))

    # keyと一致する列が一つもなかった
    # TODO: Error key 2 byte, value soure 1 byte
    def testCsv_csvrow_matchRowNumbers8(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 4, "ヤマグチケン")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = ヤマグチケン, targetColumnNumber = 4]", []),(result, msg, rowNumbers))

    # keyと一致する列が一つもなかった
    # TODO: upper and lower values
    def testCsv_csvrow_matchRowNumbers9(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","M","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 4, "m")
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = m, targetColumnNumber = 4]", []),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers10(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 1, '2017-06-27')
        self.assertEqual((1, "Complete.", [4, 5]),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers11(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 9, "10200")
        self.assertEqual((1, "Complete.", [4]),(result, msg, rowNumbers))

    # Case: input correct values
    def testCsv_csvrow_matchRowNumbers12(self):
        source = pandas.DataFrame([["集計日","教科","設問番号","設問種別","マーク値","取込済解答数","当日取込全数","白紙検出数","採点完了件数"],
                                   ["2017-06-25","問","3","親ディレクトリ","","23242","30","10","12100"],
                                   ["2017-06-26","番","2","MMMMMM","","11111","20","20","10800"],
                                   ["2017-06-27","国","3","内の要素","","12893","90","50","10200"],
                                   ["2017-06-27","数","2","ヤマグチケン","","11111","60","30","10400"],
                                   ["2017-06-28","番","4","ﾔﾏｸﾞﾁｹﾝ","","11111","50","30","23242"]])

        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 6, "11111")
        self.assertEqual((1, "Complete.", [3, 5, 6]),(result, msg, rowNumbers))

    # Case: input correct values
    # source's large size (110万行 x 700列)
    def testPerformance(self):
        result_csv, msg_csv, source, countRows_csv, countColumns_csv = csvfl_csvToDataFrame(dataPath, 1)

        # function csvrow_deleteRow
        start = time.time()
        result, msg, data_actual, countRows_actual, countColumns_actual = csvrow_deleteRow(source, 10)
        end = time.time()
        self.assertEqual((1, "Complete.", countRows_csv - 1, countColumns_csv),(result, msg, countRows_actual, countColumns_actual))
        print("Time test function csvrow_deleteRow : " + str(end - start))

        # function csvrow_deleteRows
        rowNumbers = random.sample(range(2, countRows_actual), 100)
        start = time.time()
        result, msg, data_actual, countRows_actual, countColumns_actual = csvrow_deleteRows(source, rowNumbers)
        end = time.time()
        self.assertEqual((1, "Complete.", countRows_csv - 101, countColumns_csv),(result, msg, countRows_actual, countColumns_actual))
        print("Time test function csvrow_deleteRows : " + str(end - start))

        # function csvrow_sampling
        start = time.time()
        countRows_expected = math.ceil((countRows_actual - 1) * 0.1)
        result, msg, data_actual, countRows_actual, countColumns_actual = csvrow_sampling(source, 0.1)
        end = time.time()
        self.assertEqual((1, "Complete.", countRows_expected + 1, countColumns_csv),(result, msg, countRows_actual, countColumns_actual))
        print("Time test function csvrow_sampling : " + str(end - start))

        # function csvrow_matchRowNumbers
        start = time.time()
        result, msg, rowNumbers = csvrow_matchRowNumbers(source, 2, '0')
        end = time.time()
        self.assertEqual((0, "Error : The specified key was not found in the column. [key = 0, targetColumnNumber = 2]"),(result, msg))
        print('Time test function csvrow_matchRowNumbers : ' + str(end - start))

if __name__=='__main__':
    unittest.main()