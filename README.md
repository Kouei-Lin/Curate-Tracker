# Curate Tracker Script
The `fetch_registry.py` script fetches monthly curate data from the following registries. 

- [Kleros Token v2.1](https://curate.kleros.io/tcr/100/0xeE1502e29795Ef6C2D60F8D7120596abE3baD990)
- [Kleros ATR (Address Tag Registry) v2](https://curate.kleros.io/tcr/100/0x66260C69d03837016d88c9877e61e08Ef74C59F2)
- [Kleros CDN (Contract Domain Name) v2](https://curate.kleros.io/tcr/100/0x957A53A994860BE4750810131d9c876b2f52d6E1)

# Prerequisite
`git`, `python`, and `pip` installed


# Clone to local
1. Clone the repository:

    ```bash
    git clone https://github.com/Kouei-Lin/Curate-Tracker
    cd Curate-Tracker
    ```

2. Copy the `.env.example` file and modify the registry addresses if migration happens:

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file to update the registry addresses as needed.

3. Navigate to the script folder:

    ```bash
    cd src
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the script to fetch data:

    ```bash
    python3 fetch_registry.py
    ```

    This will generate a `fetch_registry.csv` file locally.

6. Modify the `start_date` and `end_date` at line 99-100 in `fetch_registry.py` to specify the time range.

7. Open `registry_show.ipynb` for further analysis of the CSV data.

