# 🏎️ F1 2023 Season Analysis

![F1 2023 Season](https://github.com/user-attachments/assets/7cd75147-6bb1-4d65-85ad-0e0324fb30f1)

## 📜 Project Overview

This project focuses on using data sourced from APIs enriched with web scraping to obtain information on the 2023 F1 season. The main data source is the Ergast API, with additional scraping from Wikipedia to enrich circuit information and the official F1 website to gather data on the "Driver of the Day" results.

The Ergast API provides a vast amount of historical data for all F1 seasons, including drivers, constructors, lap times, and complete race results.

Important note: Sprint races have not been considered in the current version of the project.

### Specific Objectives
- **Data Extraction**: Extract information using the mentioned API and websites.
- **Data Cleaning**: Clean and structure the data appropriately.
- **Database Storage**: Create an SQL database to store the collected data in a structured format.
- **Data Analysis**: Conduct various analyses using Python, Pandas, and data visualization:
  - **Championship Results**: Analyze the drivers' and constructors' championship results.
  - **Wins and Podium Distribution**: Study which drivers secured the most podiums and victories.
  - **Positions Gained/Lost**: Identify which drivers gained or lost the most positions during races compared to their starting positions.
  - **Driver of the Day**: Study which drivers were most often awarded by the fans.
  - **Analysis of Specific Driver Results**: Examine the temporal performance evolution of specific drivers like Fernando Alonso throughout the season.

## 💻 Project Structure
```plaintext
Proyecto5-AnalisisF1
├── data/                               # Folder for storing generated datasets
├── notebooks/                          # Jupyter Notebooks for different phases of the project
│   ├── 01-extract.ipynb                # Notebook for data extraction
│   ├── 02-database.ipynb               # Notebook for database creation and data management
│   ├── 03-eda.ipynb                    # Notebook for exploratory data analysis
│   ├── 04-visuals.ipynb                # Notebook for generating visualizations
├── src/                                # Source code for project-specific functions
│   ├── support_db.py                   # Python helper functions for database operations
│   ├── support_extraction.py           # Python functions for data extraction processes
│   ├── support_queries.py              # Python functions for handling and executing SQL queries
├── .gitignore                          # Git ignore file for specifying files to exclude from Git
├── README.md                           # Project description and documentation
├── requirements.txt                    # List of project dependencies
```

## 🔧 Installation and Requirements

This project was developed using **Python 3.12**. To set up the project environment, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/SupernovaIa/Proyecto5-F1-Analysis
   ```

2. Navigate to the project directory:
   ```bash
   cd Proyecto5-F1-Analysis
   ```

3. Install the required libraries:
   The following libraries are needed for this project:

   - [**Matplotlib** (v3.9.2)](https://matplotlib.org/stable/contents.html): For data visualization and plotting.
   - [**Seaborn** (v0.13.2)](https://seaborn.pydata.org/): For statistical data visualization and enhanced Matplotlib plots.
   - [**Pandas** (v2.2.3)](https://pandas.pydata.org/pandas-docs/stable/): For data manipulation and analysis, providing powerful data structures.
   - [**psycopg2** (v2.9.10)](https://www.psycopg.org/docs/): To interact with PostgreSQL databases efficiently.
   - [**Beautiful Soup** (v4.12.3)](https://beautiful-soup-4.readthedocs.io/en/latest/): For parsing HTML and extracting data from web pages.
   - [**Requests** (v2.32.3)](https://docs.python-requests.org/en/latest/): For making HTTP requests to interact with web resources.
   - [**Selenium** (v4.26.1)](https://www.selenium.dev/documentation/): For automating web browser interactions and web scraping.
   - [**tqdm** (v4.66.4)](https://tqdm.github.io/): For creating progress bars to monitor the progress of loops and processes.

   To install all dependencies, run:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Notebooks:
   Once the environment is set up, you can execute the Jupyter Notebooks in the specified order to perform data scraping, load data into SQL, and generate visual analyses.

## 📊 Results and Conclusions

The analysis of the 2023 F1 season led to the following insights:

- **`Max Verstappen`'s dominance**: `Max Verstappen`, along with `Red Bull`, dominated the 2023 season impressively, with the Dutch driver winning 19 out of 22 races.

- **`Aston Martin`'s decline**: The team from Silverstone started the season very strong but soon struggled, resulting in more inconsistent performances.

- **`McLaren`'s rise**: In contrast to `Aston Martin`, `McLaren` showed the most significant improvement over the season. Starting from round 9 and particularly after round 14, they managed to climb up to fourth place in the constructors' standings, setting a solid foundation for the next season.

- **Driver of the Day**: `Lando Norris` was the most frequently awarded Driver of the Day, receiving this recognition five times. His popularity, combined with his standout performances and `McLaren`'s resurgence, placed him at the top of this category.

## 🔄 Next Steps

- **Adding Sprint Races**: The next key step is to include sprint races in the analysis, as they contribute points that can affect overall results.
- **Expanding the analysis to specific drivers and races**: Conduct analyses for more specific drivers and races to cover the entire grid and calendar.
- **Analyzing more seasons**: Extend the analysis to include more historical or future seasons.

## 🤝 Contributions
Contributions to this project are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request when you're ready.

If you have suggestions or improvements, feel free to open an issue.

## ✍️ Author
- **Javier Carreira** - Lead Developer - [GitHub](https://github.com/SupernovaIa)

Thanks to **Hack(io)** for the opportunity to work on this project.