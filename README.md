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
python3 main.py -i example/export.xml -u 192.168.1.4
```

### Custom output name

```bash
python3 main.py -i example/export.xml -o threat_model_target.xlsx
```

### Set level of mapper

| Type      | Description |
| ----------- | ----------- |
| 0 (default)     |  All test case  |
| 1   | Common test case |

```bash
python3 main.py -i example/export.xml -l 1
```

### Set report type output

| Type      | Description |
| ----------- | ----------- |
| 1 (default)     |  Simple, one test case many endpoint (sample screenshot for each test case)   |
| 2   | Detailed, one endpoint many test case and (screenshot for each testcase on each endpoint )       |

```bash
python3 main.py -i example/export.xml -t 2
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
- [X] Research about regex (wstg.json)
- [X] File check
	- [X] If exist overwrite it?
	- [X] If xml/input file doesn't exist, output error
- [X] Excel
	- [X] URL/IP
	- [X] Date
	- [X] Freeze column
- [X] Two type (different parsing mechanism)
	- [X] Simple, row per endpoint in one test case 
	- [X] Detail, each endpoint with many test case 
- [X] Filter from burp export
	- [X] Host
	- [X] Endpoint
- [ ] Custom test case (add level / choose ID test case)
- [ ] Output exception when ctrl+c

## Issue
- [ ] Make filter more precision, "invalid" should not match with "id" parameter 
- [X] set design excel (row height)
- [X] Some test case doesn't need list endpoint such as Information Gathering,Configuration and Deployment Management Testing (regex : *)
- [X] Duplicate/redundant endpoint
- [X] Add exception for files in json files
- [X] Add parsing mime type for file access
- [X] Try catch on data that has blank response and request

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

