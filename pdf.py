import pdfplumber
import pandas

# 指定PDF文件路径
pdf_path = "aee.pdf"

# 打开PDF文件
with pdfplumber.open(pdf_path) as pdf:
    # 获取PDF中的所有页面
    pages = pdf.pages

    for page_number, page in enumerate(pages, start=1):
        # 提取表格数据
        tables = page.extract_tables()

        for table_number, table_data in enumerate(tables, start=1):
            # 将表格数据转换为DataFrame
            df = pandas.DataFrame(table_data[1:], columns=table_data[0])

            # 生成CSV文件名
            csv_filename = f"page_{page_number}_table_{table_number}.csv"

            # 保存DataFrame为CSV文件
            df.to_csv(csv_filename, index=False)

            print(f"Table {table_number} from Page {page_number} saved as CSV: {csv_filename}")
