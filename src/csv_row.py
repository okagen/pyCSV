# -*- coding: utf-8 -*-
"""
csvファイルをDataFrameにconvertしたデータに対して、row（行）を編集するmodule
"""

import pandas
import constants as const
import math
import random

"""
機能   :  指定した行を削除する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   削除する行番号
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   行削除後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvrow_deleteRow(source, rowNumber):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # 行削除後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                    # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [rowNumber]が[int]のデータ型以外の場合
        if type(rowNumber) is not int:
           raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # rowNumberがsourceの範囲を超えていた
        if (rowNumber < 1 or source.shape[0] < rowNumber - 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_ROW_NUMBER, rowNumber)
            return

        # rowNumber=1の場合Errorとする
        if (rowNumber == 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_DELETE_HEADER_ROW
            return

        # 1行目を削除したい場合[2]が渡されるので、-2する
        source.drop(source.index[rowNumber-2], inplace=True)
        source.set_axis(0, range(source.shape[0]))
        countRows = source.shape[0]+1
        countColumns = source.shape[1]
        newData = source

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  rowNumbers(list)で指定した複数の行を削除する
引数   :
            DataFrame   :   DataFrame形式のデータ
            list        :   削除する行番号のlist
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   行削除後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvrow_deleteRows(source, rowNumbers):
    result = const.RESULT_COMPLETE  # ステータス
    msg = const.MSG_COMPLETE        # メッセージ
    newData = pandas.DataFrame()    # 行削除後のDataFrame形式のデータ
    countRows = 0                   # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [rowNumbers]が[list]のデータ型以外の場合
        # rowNumbersがNULL
        if (type(rowNumbers) is not list) or (not len(rowNumbers)):
            raise Exception

        # [rowNumbers] 内の要素が[int]のデータ型以外の場合
        if not all(type(item) is int for item in rowNumbers):
            raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        #指定されたrowNumbersがsourceの範囲を超えていた
        if(min(rowNumbers) < 1 or source.shape[0] < max(rowNumbers)-1 ):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_LIST.format(const.NAME_ROW_NUMBER, const.NAME_ROW_NUMBERS, rowNumbers)
            return

        # rowNumbersに「1」が含まれていた場合Errorとする
        if 1 in rowNumbers:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_DELETE_HEADER_ROW
            return

        # 2行目を削除したい場合[2]が渡される。DataFrame上は0行目なので、-2する
        rowNumbers[:] = [x - 2 for x in rowNumbers]
        source.drop(source.index[rowNumbers], inplace=True)
        source.set_axis(0, range(source.shape[0]))

        if source.shape[0] == 0 :
            countRows = 1
            countColumns = source.shape[1]
            newData = pandas.DataFrame(columns=[source.columns])
        else:
            countRows = source.shape[0]+1
            countColumns = source.shape[1]
            newData = source

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  samplingRatioに従って、sourceの中から要素をsamplingする
          samplingする際は、重複しない疑似乱数を用いたランダンプサンプリングを行う
引数   :
            DataFrame   :   DataFrame形式のデータ
            float       :   samplingの割合 (e.g.: 10%の場合-.1、1%の場合0.01)
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            DataFrame   :   sampling後のDataFrame形式のデータ
            int         :   header有で、csvファイルにしたときのデータの行数
            int         :   csvファイルにしたときのデータの列数
"""
def csvrow_sampling(source, samplingRatio):
    result = const.RESULT_COMPLETE      # ステータス
    msg = const.MSG_COMPLETE            # メッセージ
    newData = pandas.DataFrame()        # sampling後のDataFrame形式のデータ
    countRows = 0                       # header有で、csvファイルにしたときのデータの行数
    countColumns = 0                    # csvファイルにしたときのデータの列数

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame: 
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [samplingRatio]が[float]のデータ型以外の場合
        if type(samplingRatio) is not float:
            raise Exception

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # 指定されたsamplingRatioが0≦samplingRatio≦1の範囲外だった場合
        if (samplingRatio <= 0 or samplingRatio >= 1):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE_SAMPLING.format(samplingRatio)
            return
        
        # サンプリング数を計算
        numberOfSamples = math.ceil(source.shape[0] * samplingRatio)
        
        # サンプリング対象Indexを取得
        tgtIndex = random.sample(range(1, source.shape[0]), numberOfSamples)
        
        # サンプリング
        newData = source.iloc[tgtIndex]

        countRows = newData.shape[0]+1
        countColumns = newData.shape[1]

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, newData, countRows, countColumns

"""
機能   :  source(DataFrame)の中の、指定した列(targetColumnNumber)を検索し、keyと一致する行の番号を全てを取得する
引数   :
            DataFrame   :   DataFrame形式のデータ
            int         :   検索する対象の列番号
            string      :   検索する値
戻り値  :
            int         :   ステータス
            string      :   メッセージ
            list        :   一致した行番号のlist
"""
def csvrow_matchRowNumbers(source, targetColumnNumber, key):
    result = const.RESULT_COMPLETE  # ステータス
    msg = const.MSG_COMPLETE        # メッセージ
    rowNumbers = []                 # 一致した行番号のlist

    try:
        # sourceのformatが不正
        if type(source) is not pandas.core.frame.DataFrame:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_INVALID_FORMAT_SOURCE
            return

        # [targetColumnNumber]が[int]のデータ型以外の場合
        if type(targetColumnNumber) is not int:
            raise Exception

        # [key]が[string]のデータ型以外の場合
        if type(key) is not str:
            raise Exception
        key = key.strip()

        # sourceがNULL
        if not source.shape[0]:
            result = const.RESULT_ERR
            msg = const.MSG_ERR_EMPTY_SOURCE
            return

        # targetColumnNumberがsourceの範囲を超えていた
        if (targetColumnNumber < 1 or targetColumnNumber > source.shape[1]):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_OUT_OF_RANGE.format(const.NAME_TARGET_COLUMN_NUMBER, targetColumnNumber)
            return

        source.set_axis(0, range(source.shape[0]))
        recordIndexes = source[source.iloc[:, targetColumnNumber-1] == key].index + 1
        # keyと一致する列が一つもなかった
        if (len(recordIndexes) == 0):
            result = const.RESULT_ERR
            msg = const.MSG_ERR_KEY_NOT_FOUND.format(key, targetColumnNumber)
            return
        else:
            # 処理が問題なく完了した
            rowNumbers = recordIndexes.tolist()

    # 予期しなかったError
    except Exception:
        result = const.RESULT_ERR_UNEXPECTED
        msg = const.MSG_ERR_UNEXPECTED

    finally:
        return result, msg, rowNumbers

if __name__=='__main__':
    result, msg, data_actual, countRows, countColumns = csvrow_deleteRow(source, 2)

