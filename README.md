# owasp-wstg-mapper

## Install dependencies

```bash
pip install -r requirements.txt
```

## How to Use

### Show Help

```bash
python3 mapper.py -h
```

### Filter target

```bash
python3 mapper.py -f export.json -u 192.168.1.4
```

### Custom output name

```bash
python3 mapper.py -f export.json -o threat_model_target.xlsx
```

## Todo List
- [ ] Deploy juice shop
- [ ] Akses fitur juice shop
- [ ] Export burp
- [ ] Parsing hasil export burp
- [ ] Standardisasi daftar pengujian dan ciri-cirinya
- [ ] Mapping pengujian
- [ ] Urutkan berdasarkan kebanyakan severity
- [ ] Bikin report dalam excel

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

