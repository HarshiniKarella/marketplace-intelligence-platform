# Raw Data

This directory stores the original Olist Brazilian E-Commerce dataset files.

The raw CSV files are intentionally excluded from Git because they are external
source data and should not be modified directly.

## Dataset

[Olist Brazilian E-Commerce Public Dataset](kaggle.com/datasets/olistbr/brazilian-ecommerce/versions/2?resource=download)

Expected files:

- `olist_customers_dataset.csv`
- `olist_geolocation_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`
- `olist_order_reviews_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_products_dataset.csv`
- `olist_sellers_dataset.csv`
- `product_category_name_translation.csv`

After downloading and extracting the dataset, place all nine CSV files in this
directory.

All cleaning and transformation logic will be implemented through reproducible
data pipelines. Raw files must remain unchanged.