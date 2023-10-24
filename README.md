# Curate Tracker Script
The `fetch_registry.py` script fetches monthly curate data from the following registries. 

- [Kleros Token v2.1](https://curate.kleros.io/tcr/100/0xeE1502e29795Ef6C2D60F8D7120596abE3baD990)
- [Kleros ATR (Address Tag Registry) v2](https://curate.kleros.io/tcr/100/0x66260C69d03837016d88c9877e61e08Ef74C59F2)
- [Kleros CDN (Contract Domain Name) v2](https://curate.kleros.io/tcr/100/0x957A53A994860BE4750810131d9c876b2f52d6E1)

# Prerequisite
`git`, `python`, and `pip` installed


# Clone to local
1. `git clone https://github.com/Kouei-Lin/Curate-Tracker`
2. `cd Curate-Tracker`
3. 'cp .env.example .env', modify the registries addresses if migration happens.
4. `pip install -r requirements.txt` to install dependencies.
5. `python3 fetch_registry.py` to run the script.
6. A `fetch_registry.csv` will be generated locally. 
7. Modify **start_date** and **end_date** at **line 99-100** in `fetch_registry.py` to specify the time range.
8. Open `registry_show.ipynb` for further analysis on the csv data.
