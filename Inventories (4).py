import pandas as pd
manf = pd.read_csv('ManufacturerList (2).csv', header=None)
manf.columns = ["ID","ManufacturerName", "ItemType","DamagedIndicator"]
prices_df = pd.read_csv('PriceList(1) (1).csv', header=None)
prices_df.columns = ['ID', 'ItemPrice']
servicing_df = pd.read_csv('ServiceDatesList (1).csv', header=None)
servicing_df.columns = ['ID', 'ServiceDate']
def merge_dfs(df1, df2, df3):
    merge1 = pd.merge(df1, df2, on=df1.columns[0], how='left')
    merge2 = pd.merge(merge1, df3, on=merge1.columns[0], how='left')
    return merge2
new_df = merge_dfs(manf, prices_df, servicing_df)
new_df = new_df[['ID', 'ManufacturerName', 'ItemType', 'ItemPrice', 'ServiceDate', 'DamagedIndicator']]
new_df.loc[new_df.DamagedIndicator.isnull(), 'DamagedIndicator'] = "NotDamaged"
new_df = new_df.sort_values(by=['ManufacturerName'], ascending = True)
new_df.to_csv('FullInventory.csv', index=False)

item_types = new_df['ItemType'].unique()
def get_item_inventory_list(all_items):
    for i, num in enumerate(item_types):
        item_df = all_items[all_items.iloc[:, 2] == num]
        item_df = item_df.sort_values(by=['ID'], ascending=True)
        item_df = item_df.drop(item_df.columns[2], axis=1)
        item_df.to_csv(str(num)+'Inventory.csv', index=False)
    return item_df
get_item_inventory_list(new_df)

new_df['ServiceDate'] = pd.to_datetime(new_df['ServiceDate'])
dates = new_df['ServiceDate'].unique()
def get_past_service_dates(all_dates):
    all_dates_list = list()
    for i, num in enumerate(dates):
        past_date = all_dates[all_dates.iloc[:, 4] > pd.to_datetime("now")]
        all_dates_list.append(past_date)
    past_service_date_df = pd.concat(all_dates_list)
    return past_date
past_service = get_past_service_dates(new_df)
past_service_df = past_service.sort_values(by='ServiceDate', ascending=False)
past_service_df.to_csv('PastServiceDateInventory.csv', index=False)

damaged_items = new_df[new_df['DamagedIndicator'] == "damaged"]
damaged_items = damaged_items.drop(columns=['DamagedIndicator'], axis=1)
damaged_items = damaged_items.sort_values(by='ItemPrice', ascending=True)
damaged_items.to_csv('DamagedInventory.csv', index=False)