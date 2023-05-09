# owasp-wstg-mapper

## Install dependencies

```bash
pip install -r requirements.txt
```

## How to Use

### Show help

```bash
python3 mapper.py -h
```

### Filter target

```bash
python3 mapper.py -f export.xml -u 192.168.1.4
```

### Custom output name

```bash
python3 main.py -f export.xml -o threat_model_target.xlsx
```

## Todo List
- [X] Deploy juice shop
- [X] Akses fitur juice shop
- [X] Export burp
- [X] Parsing hasil export burp
- [ ] Standardisasi daftar pengujian dan ciri-cirinya
- [X] Mapping pengujian
- [ ] Urutkan berdasarkan kebanyakan severity
	- [ ] High - Critical (3) , Medium - High (2), Low - Medium (1)
- [X] Bikin report dalam excel

## Idea
- [ ] Check only suspicious header and body (filter header)
- [ ] Research about regex
- [ ] Basic search valid , not "invalid" match with "id"
- [ ] Custom output name
- [ ] Two type (different parsing mechanism)
	- [X] Simple , row per endpoint in one test case, 
	- [ ] Normal
- [ ] Level, only exploitation or include enumeration process
- [ ] Write all test case in excel or no?
- [ ] Category, web, infra?
- [ ] set design excel (row height)
- [ ] Some test case doesn't need list endpoint such as Information Gathering,Configuration and Deployment Management Testing

## Features
- Filter based on host
- Filter based on endpoint

## Excel Report

### Kolom
- Endpoint
- Severity
- Test Case
- Screenshot
- Result
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

## Question
- [ ] Severity dalam bentuk warna atau kolom?

