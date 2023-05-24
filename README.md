# OSTG Mapper
**OSTGMapper** (Open Security Testing Guide Mapper). An automated security testing guide mapper based on pattern. Built to reduce time of manually mapping possible security tests for web applications. Currently support :
- OWASP WSTG Test case. 

## Requirements

- libmagic
```bash
# mac
brew install libmagic

```

- python modules
```bash
pip install -r requirements.txt
```

### Installation
```bash
git clone https://github.com/kos0ng/owasp-wstg-mapper.git
```

## Usage

- Show help

```bash
python3 main.py -h
```

- Filter target

```bash
python3 main.py -i example/export.xml -u 192.168.1.4
```

- Set output name

```bash
python3 main.py -i example/export.xml -o threat_model_target.xlsx
```

- Set level of mapper
```bash
python3 main.py -i example/export.xml -l 1
```
| Type      | Description |
| ----------- | ----------- |
| 0 (default)     |  All test case  |
| 1   | Common test case |
| [0-9]   | Custom test case based on preference |


- Set report type
```bash
python3 main.py -i example/export.xml -t 2
```

| Type      | Description |
| ----------- | ----------- |
| 1 (default)     |  Simple  |
| 2   | Detail |



## Report Type (excel)

### Simple
| Column      | Description |
| ----------- | ----------- |
| ID      | Identifier of test case |
| Test Name   |  Test case name  |
| Objectives   | Objective of test case |
| Endpoint  | List of endpoint that possible to be tested |
| Result  | Result of testing, it can be PASSED/VULN/NOT APPLICABLE |
| Screenshot  | Screenshot as proof of testing |
| Notes  | Additional notes if there is something unusual |

### Detail
| Column      | Description |
| ----------- | ----------- |
| No      | Numbering |
| Endpoint   |  Target URL/endpoint  |
| Test Cases   | List of possible test case |
| Result  | Result of testing, it can be PASSED/VULN/NOT APPLICABLE |
| Screenshot  | Screenshot as proof of testing |
| Notes  | Additional notes if there is something unusual |

## Features
- Can be used with burp community edition (free)
- Filter URL/Endpoint
- Adjustable list of test case
- Adjustable pattern
- Flexible report type
- Included possible severity on each test case
- Universal report file (excel)
- Easy-to-fill report
- Support json and text request
- Possible to exclude files url (blacklist)
- Can check reflected value on response

## Example Worflow

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

### Testing Phase
- Run burpsuite
- Access features available on Juice Shop (target)
- Extract the HTTP/HTTPS history on burp
- Run mapper.py
- Open excel report
- Do penetration testing and use excel report as tracker and reference

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
- [X] Custom test case (add level / choose ID test case)
- [X] Add custom level

## Issue
- [X] Make filter more precision, "invalid" should not match with "id" parameter , regex ?id= , &id=
- [X] set design excel (row height)
- [X] Some test case doesn't need list endpoint such as Information Gathering,Configuration and Deployment Management Testing (regex : *)
- [X] Duplicate/redundant endpoint
- [X] Add exception for files in json files
- [X] Add parsing mime type for file access
- [X] Try catch on data that has blank response and request
- [X] Remove files from detail mapper
- [X] Check reflected
- [X] Move overwrite first 
- [X] Ensure level in format level[0-9]
- [X] Ensure level in list wstg id




