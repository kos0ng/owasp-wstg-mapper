# owasp-wstg-mapper

## Install dependencies

```bash
pip install -r requirements.txt
```

## Launch apps

```bash
python3 mapper.py
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

