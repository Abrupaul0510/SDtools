
# SD Tools
Scripts for SD-Agent

## Installation

1. Clone/Download this repository to your local machine.

2. Navigate to the project directory in your terminal.


3. Install the required modules using the requirements.txt file:

```bash
pip install -r requirements.txt
```

4. Edit the config.py file.

Here are the configuration needed:

```bash
bothost = ''

log_sheet = ''

sd_id = ''

excel_path = ""

dingtalk_token = ""

gsheet_token_path = ""

dt_token_for_wfc = ""
```

5. To run the SD Tools, simply execute the tools.py file:

```bash
python tools.py
```


6. Choose script to run:

```bash
Please choose script to run:
1. Hourly
2. Check Closed Tickets
3. Owned Ticket Status
4. Run Ticket Monitor
5. My Handled Tickets
Enter your choice (1/2/3/4/5):
```

If you encounter any issues, you can contact me at Dingtalk. Thanks