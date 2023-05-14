# owasp-wstg-mapper

## Install dependencies

```bash
pip install -r requirements.txt
```

## How to Use

### Show help

```bash
python3 main.py -h
```

### Filter target

```bash
python3 main.py -f export.xml -u 192.168.1.4
```

### Custom output name

```bash
python3 main.py -f export.xml -o threat_model_target.xlsx
```

### Set level output

| Level      | Description |
| ----------- | ----------- |
| 1      |  Without Enumeration Test Case (WSTG-INFO and WSTG-CONF)      |
| 2 (default)  | All Test Case        |

```bash
python3 main.py -f export.xml -l 1
```

## Todo List
- [X] Deploy juice shop
- [X] Akses fitur juice shop
- [X] Export burp
- [X] Parsing hasil export burp
- [X] Standardisasi daftar pengujian dan ciri-cirinya
- [X] Mapping pengujian
- [X] Urutkan berdasarkan kebanyakan severity (source : )
	- [X] High - Critical (3) , Medium - High (2), Low - Medium (1)
- [X] Bikin report dalam excel

## Idea
- [X] Custom output name
- [X] Level, only exploitation or include enumeration process
- [X] Research about regex (wstg.json)
- [ ] File check
	- [ ] If exist overwrite it?
	- [ ] If xml/input file doesn't exist, output error
- [ ] Excel
	- [ ] URL/IP
	- [ ] Date
	- [ ] Lock column
	- [ ] Freeze column
- [ ] Custom test case (add level / choose ID test case)
- [ ] Custom target (filter test case)
	- [ ] web
	- [ ] infrastructure
- [ ] Custom header check (filter header)
- [ ] Custom check on req header/req response/resp header/resp body
- [ ] Two type (different parsing mechanism)
	- [X] Simple, row per endpoint in one test case 
	- [ ] Detail, each endpoint with many test case 
- [ ] Filter from burp export
	- [ ] Host
	- [ ] Endpoint

## Issue
- [ ] Make filter more precision, "invalid" should not match with "id" parameter 
- [X] set design excel (row height)
- [ ] Some test case doesn't need list endpoint such as Information Gathering,Configuration and Deployment Management Testing
- [X] Duplicate/redundant endpoint
- [X] Add exception for files in json files
- [ ] Try catch on data that has blank response

## Features
- TBU

## Excel Report

### Kolom
- Test Case ID (with severity color)
- Test Name
- Objectives
- Endpoint
- Result
- Screenshot
- Notes

## Testing

### Specification
- OWASP Juice Shop v14.5.1
- Burpsuite Community Edition v2023.3.5
- Python v3.10.0
- Firefox v112.0.2

### Run Juice Shop on Docker

```bash
# Download latest juice shop image
docker pull --platform linux/amd64 bkimminich/juice-shop

# Run the image on port 3000
docker run -d -p 3000:3000 --platform linux/amd64 bkimminich/juice-shop

# Access the juice shop
http://localhost:3000
```

### Work Flow
- Run burpsuite
- Access features available on Juice Shop
- Extract the HTTP/HTTPS history on burp
- Run mapper.py
- Open excel report
- Do penetration testing and use excel report as tracker and reference

