import bls

df = pd.read_excel('cesseriespub.xlsx',
    sheet_name='CES_Pub_NAICS_17',
    header=1,
    index_col=0)

result = pd.DataFrame()

end = 0
while(end < df.shape[0])
    series = ['CES{}01'.format(i.replace('-',''))
        for i in df[start : start+50].index.values]
    print(series)
    start+=51
    end = start
