from flask import *
import pandas as pd
import numpy as np
import datetime
import sqlite3

app = Flask(__name__)

#複数行の文字列は'''で囲む

q_taihi = '''WITH dsum AS ( select データ識別番号,入院年月日,sum(行為点数*行為回数) AS DPC総点数 \
from dtable \
where データ区分 <> 97 \
group by データ識別番号,入院年月日), \
efsum AS( \
SELECT データ識別番号,入院年月日,SUM(出来高実績点数*行為回数) AS 出来高総点数 \
FROM etable \
WHERE データ区分 <> 92 \
AND データ区分 <> 97 \
AND 行為明細区分情報 LIKE '__0_________' \
group by データ識別番号,入院年月日) \
select distinct d.データ識別番号-10 AS 患者ID,d.入院年月日, \
d.DPC総点数,e.出来高総点数,d.DPC総点数-e.出来高総点数 AS 点数差異 \
from dsum AS d \
INNER JOIN efsum AS e \
USING(データ識別番号,入院年月日)'''

q_entdrug1 = '''select データ識別番号-10 AS ID,診療明細名称,使用量,明細点数・金額,行為回数,実施年月日,病棟コード \
from etable \
Where 実施年月日 = 退院年月日 \
AND 行為明細区分情報 LIKE '0_0_________' \
AND データ区分 BETWEEN 21 AND 23 \
AND 明細点数・金額 > 0 \
AND 行為回数 > 1;'''


q_entdrug2 = '''select データ識別番号-10 AS ID,診療明細名称,使用量,明細点数・金額,行為回数,実施年月日,病棟コード \
from etable \
Where CAST(退院年月日 AS INTEGER) - CAST(実施年月日 AS INTEGER)  = 1 \
AND 行為明細区分情報 LIKE '0_0_________' \
AND データ区分 BETWEEN 21 AND 22 \
AND 明細点数・金額 > 0 \
AND 行為回数 > 1 \
AND 退院年月日 <> '0';'''

q_entdrug3 = '''select データ識別番号-10 AS ID,診療明細名称,使用量,明細点数・金額,行為回数,実施年月日,病棟コード \
from etable \
Where 実施年月日 <> 退院年月日 \
AND 行為明細区分情報 LIKE '1_0_________' \
AND データ区分 BETWEEN 21 AND 23 \
AND 明細点数・金額 > 0;'''


query = {'taihi':q_taihi,'drug1':q_entdrug1,'drug2':q_entdrug2,'drug3':q_entdrug3}
query_name = {'taihi':'DPC出来高対比','drug1':'退院日に出来高になってないもの（２７９になってないぞ）',
				'drug2':'退院日前日の退院処方探し（おそらく退院処方）',
				'drug3':'退院日以前の退院処方'}

conn = sqlite3.connect('dpc.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS dtable(施設番号 integer,データ識別番号 integer,退院年月日 text,入院年月日 text,データ区分 integer,順序番号 integer,点数マスタコード integer,レセ電算処理コード integer,解釈番号 text, \
診療行為名称 text,行為点数 real, 行為薬剤料 real,行為材料料 real,円点区分 integer,行為回数 real,保険者番号 text,レセプト種別コード text,実施年月日 text,レセプト科区分 text,診療科区分 text, \
医師コード text,病棟コード text,病棟区分 text,入外区分 text,施設タイプ text,算定開始日 text,算定終了日 text,算定起算日 text,分類番号 text,医療機関係数 real)''')

c.execute('''CREATE TABLE IF NOT EXISTS etable(施設コード integer,データ識別番号 integer, \
退院年月日 text,入院年月日 text,データ区分 real,順序番号 real,行為明細番号 integer,病院点数マスタコード real, \
レセプト電算コード real,解釈番号 text,診療明細名称 text,使用量 real,基準単位 real,明細点数・金額 real,\
円点区分 integer,出来高実績点数 real,行為明細区分情報 text,行為点数 real,行為薬剤料 real, \
行為材料料 real,行為回数 real,保険者番号 real, \
レセプト種別コード real,実施年月日 text,レセプト科区分 real,診療科区分 real, \
医師コード text,病棟コード real,病棟区分 real,入外区分 text, \
施設タイプ text)''')

conn.commit()
conn.close()


				
				
@app.route("/")
def show_tables():
	conn = sqlite3.connect('dpc.db')
	etable = pd.read_sql('select * from etable limit 10',conn)
	dtable = pd.read_sql('select * from dtable limit 10',conn)
	conn.close()
	return render_template('view.html',etable=etable.to_html(classes='etable'),
		dtable = dtable.to_html(classes='dtable'))


@app.route("/pandas",methods=['GET','POST'])

def read_pandas():
	if request.method == 'POST' and request.files['dfile']:
		data = request.files['dfile']
		df1 = pd.read_csv(data,encoding = 'shift_jisx0213',delimiter = '\t',
			names = ('施設番号','データ識別番号','退院年月日','入院年月日','データ区分'
	,'順序番号','点数マスタコード','レセ電算処理コード','解釈番号','診療行為名称','行為点数'
	,'行為薬剤料','行為材料料','円点区分','行為回数','保険者番号','レセプト種別コード'
	,'実施年月日','レセプト科区分','診療科区分','医師コード','病棟コード','病棟区分','入外区分'
	,'施設タイプ','算定開始日','算定終了日','算定起算日'	,'分類番号','医療機関係数'),header = None)
		conn = sqlite3.connect('dpc.db')
		c = conn.cursor()
		df1.to_sql('dtable',conn,if_exists='append',index = False) 
		c.execute('''UPDATE dtable SET 行為点数 = 行為点数 * 医療機関係数 Where データ区分 = 93''')
		conn.commit()
		filedata = pd.read_sql('select * from dtable limit 20',conn)
		conn.close()
	elif request.method == 'POST' and request.files['efile']:
		data = request.files['efile']
		df2 = pd.read_csv(data,encoding = 'shift_jisx0213',delimiter = '\t',
			dtype={'行為明細区分情報':str})
		conn = sqlite3.connect('dpc.db')
		df2.to_sql('etable',conn,if_exists='append',index = False) 
		# ↑Replaceはやめよう
		filedata = pd.read_sql('select * from etable limit 20',conn)
		conn.close()
	return render_template('view.html',filedata = filedata.to_html(classes='filedata'))




@app.route("/query",methods=['GET','POST'])
def multi_query():
	if request.method == 'POST' and request.form['trigger'] == 'on':
		conn = sqlite3.connect('dpc.db')
		req_query = request.form['q1']
		query_data = pd.read_sql(query[req_query],conn)
		conn.close()
		return render_template('query.html',query_name = query_name[req_query],query_data = query_data.to_html(classes='query_data'))
	else:
		return render_template('query.html')



@app.route("/delete",methods=['GET','POST'])
def delete_data():
	if request.method == 'POST':
		if request.form['d_trigger'] == 'on':
			conn = sqlite3.connect('dpc.db')
			c = conn.cursor()
			if request.form['t1'] == 'dtable':
				c.execute('''DELETE FROM dtable''')
				conn.commit()
				conn.close()
			elif request.form['t1'] == 'etable':
				c.execute('''DELETE FROM etable''')
				conn.commit()
				conn.close()
	return render_template('delete.html')
			



#def dashboards():



	
if __name__ == "__main__":
	import webbrowser
	import threading
	import random

	port = 5000 + random.randint(0,999)
	url = 'http://127.0.0.1:%s' % port
	
	threading.Timer(1.45,lambda: webbrowser.open(url)).start()
	app.run(port=port,debug=False)