from flask import *
import pandas as pd
import numpy as np
import datetime
import sqlite3
import glob
import os
app = Flask(__name__)

#複数行の文字列は'''で囲む

query_list = glob.glob('query/*.txt')

querys = {}
for i in query_list:
    name,txt = os.path.splitext(os.path.basename(i))
    with open(i, "r+",encoding='utf-8') as file:
        querys[name] = file.read()

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
レセプト種別コード real,実施年月日 text,レセプト科区分 real,診療科区分 text, \
医師コード text,病棟コード text,病棟区分 text,入外区分 text, \
施設タイプ text)''')

conn.commit()
conn.close()


				
				
@app.route("/")
def show_tables():
	conn = sqlite3.connect('dpc.db')
	etable = pd.read_sql('select * from etable limit 10',conn)
	dtable = pd.read_sql('select * from dtable limit 10',conn)
	conn.close()
	return render_template('view.html',etable=etable.to_html(classes="mdl-data-table mdl-js-data-table"),
		dtable = dtable.to_html(classes="mdl-data-table mdl-js-data-table"))


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
		conn.close()
		flash('Dファイルデータを登録しました')
		return redirect(url_for('show_tables'))
	elif request.method == 'POST' and request.files['efile']:
		data = request.files['efile']
		df2 = pd.read_csv(data,encoding = 'shift_jisx0213',delimiter = '\t',
			dtype={'行為明細区分情報':str})
		conn = sqlite3.connect('dpc.db')
		df2.to_sql('etable',conn,if_exists='append',index = False) 
		# ↑Replaceはやめよう
		conn.close()
		flash('Dファイルデータを登録しました')
		return redirect(url_for('show_tables'))
	return render_template('view.html')




@app.route("/query",methods=['GET','POST'])
def multi_query():
	if request.method == 'POST' and request.form['trigger'] == 'on':
		conn = sqlite3.connect('dpc.db')
		req_query = request.form['q1']
		query_data = pd.read_sql(querys[req_query],conn)
		conn.close()
		session['temp_csv'] = query_data.to_csv()
		return render_template('query.html',select_query_name = req_query,
			query_data = query_data.to_html(classes="mdl-data-table mdl-js-data-table"),
			query_keys = sorted(querys.keys()))
	else:
		return render_template('query.html',query_keys = sorted(querys.keys()))




@app.route("/csv",methods = ['GET'])
def download_csv():
	csvdata = session.get('temp_csv')
	response = make_response(csvdata)
	cd = 'attachment; filename = output.csv'
	response.headers['Content-Disposition'] = cd
	response.mimetype = 'text/csv'

	return response

#別にユーザーログイン管理などをしないアプリケーションなので、secret keyはお飾りです。
#これが設定されていないとsessionを使ってdef間にデータを渡すことが出来ません(globalを使う手もありますが)
app.secret_key = 'ddd873jf'



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
				flash('Dファイルデータを削除しました')
				return redirect(url_for('show_tables'))
			elif request.form['t1'] == 'etable':
				c.execute('''DELETE FROM etable''')
				conn.commit()
				conn.close()
				flash('EFファイルデータを削除しました')
				return redirect(url_for('show_tables'))
	return redirect(url_for('show_tables'))
			

#このflashは動くんだが、同じメッセージが２箇所で出てしまう…
#先頭に持っていくなり、categoryを設けるなりしないとダメ

@app.route("/board",methods = ['GET'])
def dashboards():
	test = dashData()
	compare_byoto_j = test["compare_byoto"]
	compare_ka_j = test["compare_ka"]
	Percent_ka_j = test["Percent_ka"]
	Percent_byoto_j = test["Percent_byoto"]
	return render_template('board.html',compare_byoto_j = compare_byoto_j,
		compare_ka_j = compare_ka_j,Percent_ka_j = Percent_ka_j,
		Percent_byoto_j = Percent_byoto_j)


#地域包括ケアがあるとバグるみたい。確認。92のせい
def dashData():
	conn = sqlite3.connect('dpc.db')
	compare_byoto = '''WITH dsum AS ( select 病棟コード,sum(行為点数*行為回数) AS DPC総点数 \
						from dtable \
						where データ区分 <> 97 \
						group by 病棟コード), \
						efsum AS( \
						SELECT 病棟コード,SUM(出来高実績点数*行為回数) AS 出来高総点数 \
						FROM etable \
						WHERE データ区分 <> 92 \
						AND データ区分 <> 97 \
						AND 行為明細区分情報 LIKE '__0_________' \
						group by 病棟コード) \
						select distinct 病棟コード, \
						d.DPC総点数,e.出来高総点数,d.DPC総点数-e.出来高総点数 AS 出来高対比 \
						from dsum AS d \
						INNER JOIN efsum AS e \
						USING(病棟コード);'''
	compare_ka = '''WITH dsum AS ( select 診療科区分,sum(行為点数*行為回数) AS DPC総点数 \
						from dtable \
						where データ区分 <> 97 \
						group by 診療科区分), \
						efsum AS( SELECT 診療科区分,SUM(出来高実績点数*行為回数) AS 出来高総点数 \
						FROM etable \
						WHERE データ区分 <> 92 \
						AND データ区分 <> 97 \
						AND 行為明細区分情報 LIKE '__0_________' \
						group by 診療科区分) \
						select distinct 診療科区分, \
						d.DPC総点数,e.出来高総点数,d.DPC総点数-e.出来高総点数 AS 出来高対比 \
						from dsum AS d \
						INNER JOIN efsum AS e \
						USING(診療科区分);'''
	Percent_ka = '''SELECT 診療科区分,sum(行為点数*行為回数) AS DPC総点数 \
                      from dtable \
                      Where データ区分 <> 97 \
                      GROUP BY 診療科区分'''
	Percent_byoto = '''SELECT 病棟コード,sum(行為点数*行為回数) AS DPC総点数 \
                      from dtable \
                      Where データ区分 <> 97 \
                      GROUP BY 病棟コード'''

	board_name = {"compare_byoto":compare_byoto,"compare_ka":compare_ka,
    "Percent_ka":Percent_ka,"Percent_byoto":Percent_byoto}
	board_data = {}
	for i in board_name.keys():
		df = pd.read_sql(board_name[i],conn)
		jsondata = df.to_json(orient='records',force_ascii=False)
		board_data[i] = jsondata
	conn.close()
	return board_data






	
if __name__ == "__main__":
	import webbrowser
	import threading
	import random

	port = 5000 + random.randint(0,999)
	url = 'http://127.0.0.1:%s' % port
	
	threading.Timer(1.45,lambda: webbrowser.open(url)).start()
	app.run(port=port,debug=True)