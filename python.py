print('Hello World test 20231201')
# datetimeモジュールを使用
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
print(repr(now))
# 出力例
#datetime.datetime(2021, 11, 4, 17, 37, 28, 114417, tzinfo=datetime.timezone
#(datetime.timedelta(seconds=32400), 'JST'))
print(now)  # 2021-11-04 17:37:28.114417+09:00

# YYYYMMDDhhmmss形式に書式化
d = now.strftime('%Y%m%d%H%M%S')
print(d)  # 20211104173728

d = f'{now:%Y%m%d%H%M%S}'  # f文字列
d = format(now, '%Y%m%d%H%M%S')  # format関数
d = '{:%Y%m%d%H%M%S}'.format(now)  # 文字列のformatメソッド
print(d)  # 20211104173728

# YYYY/MM/DD hh:mm:ss形式に書式化
d = now.strftime('%Y/%m/%d %H:%M:%S')
print(d)  # 2021/11/04 17:37:28

# MM/DD/YY hh:mm:ss形式に書式化
d = now.strftime('%x %X')
print(d)  # 11/04/21 17:37:28

# 日付のみを書式化
d = now.date().strftime('%Y/%m/%d')
print(d)  # 2021/11/04

# 時刻のみを書式化
t = now.time().strftime('%X')
print(t)  # 17:37:28

# 西暦を2桁に
d = now.strftime('%y/%m/%d %H:%M:%S')
print(d)  # 21/11/04 17:37:28

# 12時間制＋AM／PM表示
d = now.strftime('%Y/%m/%d %I:%M(%p)')
print(d)  # 2021/11/04 05:37(PM)

# 曜日を含む日付
d = now.strftime('%Y年%m月%d日（%a）')
print(d)  # 2021年11月04日（Thu）

d_week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水',
          'Thu': '木', 'Fri': '金', 'Sat': '土'}
key = now.strftime('%a')
w = d_week[key]
d = now.strftime('%Y年%m月%d日') + f'（{w}）' #f'{now:%Y年%m月%d日}（{w}）'
print(d)  # 2021年11月04日（木）

d_week = '日月火水木金土日'  # インデックス0の'日'は使用されない
idx = now.strftime('%u')  # '%u'では月曜日がインデックス'1'となる
w = d_week[int(idx)]
d = now.strftime('%Y年%m月%d日') + f'（{w}）'
print(d)  # 2021年11月04日（木）

# タイムゾーン
d = now.strftime('%X%z(%Z)')
print(d)  # 17:37:28+0900(JST)

# timeモジュールを使用
import time

now = time.localtime()
print(now)
# 出力例
#time.struct_time(tm_year=2021, tm_mon=11, tm_mday=4, tm_hour=19, tm_min=40,
#tm_sec=1, tm_wday=3, tm_yday=308, tm_isdst=0)

d = time.strftime('%Y%m%d%H%M%S', now)  # YYYYMMDDhhmmssに書式化
d = time.strftime('%Y/%m/%d %H:%M:%S', now)  # YYYY/MM/DD hh:mm:ssに書式化
d = time.strftime('%x %X', now)  # MM/DD/YY hh:mm:ssに書式化
d = time.strftime('%y/%m/%d %H:%M:%S', now)  # YY/MM/DD hh:mm:ssに書式化
d = time.strftime('%Y/%m/%d %I:%M(%p)', now)  # 12時間制＋AM／PM表示
d = time.strftime('%Y年%m月%d日（%a）', now)  # 曜日を含む日付

d_week = {'Sun': '日', 'Mon': '月', 'Tue': '火', 'Wed': '水',
          'Thu': '木', 'Fri': '金', 'Sat': '土'}
key = time.strftime('%a', now)
w = d_week[key]
d = time.strftime('%Y年%m月%d日', now) + f'（{w}）'
print(d)  # 2021年11月04日（木）
