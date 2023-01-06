from plugins.send_to_slack import send_to_slack
from plugins.transform.read_transform import run_transform
import matplotlib.pyplot as plt


def run():
    file_bytes = "automate_report/output/sales_per_month.png"

    # analyze and create graph
    # read and transform data by product
    data_product = run_transform(group_by='product').sort_values('total_price', ascending=False).head(3)
    # read and transform data by month
    data_month = run_transform(group_by='month')

    fig, ax = plt.subplots(2)

    # Membuat grafik Sales by Product
    ax[0].bar(data_product['Product'], data_product['total_price'])
    ax[0].set_xlabel('Product')
    ax[0].set_ylabel('Total Sales (USD)')
    ax[0].set_yticklabels(data_month['total_price'])

    # Membuat grafik Sales by Month
    ax[1].bar(data_month['Order Date'].dt.month.astype(str), data_month['total_price'])
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Total Sales (USD)')
    ax[1].set_yticklabels(data_month['total_price'])

    # Save graph ke image png
    fig.savefig(file_bytes, bbox_inches='tight')

    # send graph to slack channel
    message = "This is the Revenue per product performance"
    channel = "D04HJNQ6M7E"

    send_to_slack.execute(message, channel, file_bytes)

if __name__ == '__main__':
    run()