import pandas as pd


def export_data(input_data, name):
    writer = pd.ExcelWriter("{0}.xlsx".format(name), engine="xlsxwriter")

    if isinstance(input_data, pd.DataFrame):
        input_data.to_excel(writer, sheet_name="data")

    elif isinstance(input_data, dict):
        df_out = pd.DataFrame.from_dict(input_data)
        df_out.to_excel(writer, sheet_name="data")

    else:
        print("Unknown format for export")

    writer.save()





