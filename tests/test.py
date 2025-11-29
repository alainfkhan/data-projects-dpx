from icecream import ic


def main() -> None:
    # url = "https://www.kaggle.com/datasets/sharafatahmed/product-dataset/data?select=Message+Group+-+Product.csv"
    # kaggle_url = "https://www.kaggle.com/datasets/sharafatahmed/product-dataset/data"
    # kaggle_url = "https://www.kaggle.com/datasets/sharafatahmed/product-dataset?select=Message+Group+-+Product.csv"
    kaggle_url = "https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009/code?datasetId=4458&sortBy=dateRun&tab=collaboration&excludeNonAccessedDatasources=false"

    protocol = "https://"
    splits = kaggle_url.removeprefix(protocol).split("/")
    dataset_name_splits = splits[3].split("?")
    dataset_name = dataset_name_splits[0]
    ic(splits)
    ic(dataset_name_splits)
    ic(dataset_name)

    handle: str = f"{splits[2]}/{dataset_name}"
    clean_url: str = f"{protocol}{splits[0]}/{splits[1]}/{handle}"
    ic(handle)
    ic(clean_url)

    pass


if __name__ == "__main__":
    main()
