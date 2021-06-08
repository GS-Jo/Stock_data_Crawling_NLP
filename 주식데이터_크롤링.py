import pandas as pd
import requests

dates = pd.date_range("20200520", "20210520")

dfs = []

for date in dates:
    print(date, end=" ")
    date = str(date).split(" ")[0].replace("-", "")
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    params = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT01501",
        "mktId": "ALL",
        "trdDd": date,
        "share": "1",
        "money": "1",
        "csvxls_isNo": "false",
    }
    response = requests.post(url, params)
    datas = response.json()["OutBlock_1"]
    df = pd.DataFrame(datas)
    df["DATE"] = date
    dfs.append(df)
    time.sleep(1)

result_df = pd.concat(dfs)
result_df.reset_index(inplace=True)
result_df.tail()

