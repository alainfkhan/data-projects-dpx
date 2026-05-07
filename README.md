## Navigation

- [Analysis Projects](https://github.com/alainfkhan/data-projects-projects)
- [`DPM`](https://github.com/alainfkhan/data-projects)
  - [`DPX`](https://github.com/alainfkhan/data-projects-dpx) `<-`
  - [`DPP`](https://github.com/alainfkhan/data-projects-projects)
- [Github Profile](https://github.com/alainfkhan)

# Data Project Executor (DPX)

*Source code for the CLI app*

## How it works

### Create a project workspace

Suppose you are scrolling through Kaggle and find a dataset you would like to study.

To create a project workspace:

```shell
dpx init olistbr -u https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce -g static
```

| Code     | Type          | Help                                                 | Value                                                           |
| -------- | ------------- | ---------------------------------------------------- | --------------------------------------------------------------- |
| `dpx`  | CLI tool name | Call the application.                                | -                                                               |
| `init` | Command       | Initialise a project workspace in an existing group. | `olistbr`                                                     |
| `-u`   | Flag          | The url source of the dataset.                       | `https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce` |
| `-g`   | Flag          | The name of the group.                               | `static`                                                      |

This generates a project workspace

- named `olistbr`,
- with the dataset from `https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`,
- in a group: `static`.

`dpx` will generate a new project workspace `olistbr` in `dp-projects/static/`:

```text
data-projects/
├── dpx/                # source code for CLI app
│   └── ...
│
└── dp-projects/        # where the projects live
    ├── .hidden/
    ├── .trash/
    ├── main/
    ├── playground/
    ├── macos/
    └── static/
        └── olistbr/    # new workspace created here
            └── ...

```

The project workspace generated will have structure:

```text
olistbr/
├── data/
│   ├── raw/                                            # the dataset saved here
│   │   ├── olist_customers_dataset.csv                 # -\
│   │   ├── ...                                         #  |- brazilian-ecommerce dataset (9 files)
│   │   └── product_category_name_translation.csv       # -/
│   │
│   ├── interim/
│   ├── processed/
│   │   └── olistbr.xlsx                                # empty file
│   │
│   └── external/                                       # place for other data
│       └── brazilian-ecommerce.json                    # kaggle dataset metadata
│
├── docs/
│   ├── assets/                         # place for images and gifs for README.md
│   └── notes.txt                       # empty file
│
├── notebooks/
│   └── olistbr.ipynb                   # empty notebook
│
├── references/
│   └── sources.txt                     # urls used appended
│
├── reports/
│   └── figures/                        # images produced from results
│
└── README.md                           # report in markdown
```

> [!CAUTION]
>
> - From the current configuration of `dpx` the metadata `.json` file generated from the kaggle API (`brazilian-ecommerce.json`) will have the default name: `dataset-metadata.json`
> - The user would have to manually change the name to avoid overwriting new metadata downloads.

### Download more data to an existing project

Suppose you find a supplementary dataset you would like to add on to your current project.

To download a new dataset:

```shell
dpx dl olistbr -u https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist
```

| Code    | Type          | Help                                        | Value                                                           |
| ------- | ------------- | ------------------------------------------- | --------------------------------------------------------------- |
| `dpx` | CLI tool name | Call the application.                       | -                                                               |
| `dl`  | Command       | Download a dataset to an existing project. | `olistbr`                                                     |
| `-u`  | Flag          | The url source of the dataset.              | `https://www.kaggle.com/datasets/olistbr/market-funnel-olist` |

This adds the new dataset onto the current project.

```txt
olistbr/
├── data/
│   ├── raw/
│   │   ├── olist_customers_dataset.csv                     # -\
│   │   ├── ...                                             #  |- brazilian-ecommerce dataset (9 files)
│   │   ├── product_category_name_translation.csv           # -/
│   │   ├── olist_closed_deals_dataset.csv                  # _
│   │   └── olist_marketing_qualified_leads_dataset.csv     # -\- market-funnel-olist dataset (2 files)
... ...
│   └── external/
│       ├── brazilian-ecommerce.json  
│       └── marketing-funnel-olist.json                    # new metadata saved
...
├── references/
│   └── sources.txt                                        # new url appended
...
```

---

### Common commands

View help:

```shell
dpx --help
```

```txt
 Usage: dpx [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                         │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.  │
│ --help                        Show this message and exit.                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ hello                                                                                                           │
│ gadd          Create a new group.                                                                               │
│ dl            Download a dataset to an existing project.                                                        │
│ dcp           Copies all data in raw to interim in a project.                                                   │
│ dpromote      Copies and converts all csv files in raw to interim.                                              │
│ init          Initialise a project workspace in an existing project group.                                      │
│ ls            List project(s) in group(s).                                                                      │
│ gls           List groups.                                                                                      │
│ dls           List data files in a project.                                                                     │
│ where         Find the project path.                                                                            │
│ sources       View the sources of a project.                                                                    │
│ begin         Begin working on the project by opening an IDE.                                                   │
│ unlock        Unlock project(s).                                                                                │
│ lock                                                                                                            │
│ islocked                                                                                                        │
│ rename        Rename an existing project including all sub files with the same name.                            │
│ add-sources   Appends sources to the sources.txt                                                                │
│ mv            Move a file from one group to another group.                                                      │
│ rm            Delete project(s).                                                                                │
│ grm                                                                                                             │
│ dev                                                                                                             │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

List all projects in all groups:

```shell
dpx ls -a
```

```txt
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ [1] main/     ┃ [7] playground/ ┃ [1] macos/ ┃ [2] static/ ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ datta-finance │ kanchana-btc    │ bogacz-res │ ks-mpq      │
│               │ morse-retail    │            │ olistbr     │
│               │ natrayn-imdb    │            │             │
│               │ neurocipher     │            │             │
│               │ pbi-sample      │            │             │
│               │ raveen-tv       │            │             │
│               │ shahid-yt       │            │             │
└───────────────┴─────────────────┴────────────┴─────────────┘
```

List all datafiles in a project:

```shell
dpx dls morse-retail
```

```txt
                             playground/morse-retail/data/                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [2] raw/                  ┃ [0] interim/ ┃ [1] processed/    ┃ [1] external/         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ business.retailsales2.csv │              │ morse-retail.xlsx │ dataset-metadata.json │
│ business.retailsales.csv  │              │                   │                       │
└───────────────────────────┴──────────────┴───────────────────┴───────────────────────┘
```

Get the data sources of a project:

```shell
dpx sources morse-retail
```

Check if a project is locked:

```shell
dpx islocked morse-retail
```

> [!NOTE]
>
> - `dpx` has a lock feature to discourage moving groups.
> - A project must first be unlocked before it is moved or deleted.

Unlock a project:

```shell
dpx unlock morse-retail
```

Move a project to group `main`:

```shell
dpx mv morse-retail -to main
```

> [!NOTE]
> The project is locked immediately after being moved to another group.

Rename the project name:

```shell
dpx rename morse-retail retail-dataset
```

Find the path of the project:

```shell
dpx where retail-dataset
```

Delete a project:

```shell
dpx unlock retail-dataset;
dpx rm retail-dataset
```

Begin working on a project:

```shell
dpx begin olistbr
```

This opens VScode on the selected project `olistbr` inside the project store.
